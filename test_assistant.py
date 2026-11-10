import os
import tempfile
import unittest

os.environ["RAG_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")
from documents import build_index  # noqa: E402
from pseudonymize import pseudonymize  # noqa: E402
from rag import NO_INFO, answer  # noqa: E402

INDEX = build_index()
FAKE = lambda prompt: "réponse simulée"


class Tests(unittest.TestCase):
    def test_finds_right_document(self):
        r = answer("Combien de caractères pour un mot de passe ?", "stagiaire", INDEX, llm=FAKE)
        self.assertEqual(r["sources"][0], "charte_informatique")

    def test_restricted_doc_hidden_from_stagiaire(self):
        r = answer("Quelle est la durée de conservation des candidatures de stage ?", "stagiaire", INDEX, llm=FAKE)
        self.assertNotIn("registre_traitements", r["sources"])

    def test_restricted_doc_visible_to_referent(self):
        r = answer("Quelle est la durée de conservation des candidatures de stage ?", "referent", INDEX, llm=FAKE)
        self.assertIn("registre_traitements", r["sources"])

    def test_model_not_called_when_nothing_found(self):
        called = []
        r = answer("Quel est le menu de la cantine ?", "stagiaire", INDEX, llm=lambda p: called.append(p) or "x")
        self.assertEqual(r["answer"], NO_INFO)
        self.assertEqual(called, [])

    def test_unknown_role_rejected(self):
        with self.assertRaises(ValueError):
            answer("test", "inconnu", INDEX, llm=FAKE)

    def test_restricted_text_never_reaches_prompt(self):
        prompts = []
        answer("Quel est le poste du chef du service informatique ?", "stagiaire", INDEX, llm=lambda p: prompts.append(p) or "x")
        self.assertTrue(all("4501" not in p and "Lambert" not in p for p in prompts))

    def test_prompt_v2_formats_and_keeps_context(self):
        os.environ["RAG_PROMPT"] = "v2"
        try:
            seen = []
            answer("Combien de caractères pour un mot de passe ?", "stagiaire", INDEX, llm=lambda p: seen.append(p) or "x")
        finally:
            del os.environ["RAG_PROMPT"]
        self.assertIn("exemple_doc", seen[0])
        self.assertIn("[charte_informatique]", seen[0])

    def test_pseudonymization(self):
        text, counts = pseudonymize("M. Henri Moreau, né le 14/03/1957, tél. 06 12 34 56 78, vu par le Dr Lefèvre. M. Henri Moreau revient.")
        self.assertNotIn("Moreau", text)
        self.assertNotIn("1957", text)
        self.assertNotIn("06 12", text)
        self.assertEqual(text.count("[PERSONNE_1]"), 2)  # même personne, même jeton
        self.assertIn("[PROFESSIONNEL_1]", text)

    def test_same_person_partial_name(self):
        text, _ = pseudonymize("Mme Sophie Garnier est sortie. Courrier envoyé à Mme Garnier.")
        self.assertEqual(text.count("[PERSONNE_1]"), 2)
        self.assertNotIn("[PERSONNE_2]", text)

    def test_email_keeps_final_dot(self):
        text, _ = pseudonymize("Contact : a.b@exemple.fr. Suite.")
        self.assertIn("[EMAIL]. Suite.", text)

    def test_nir_masked(self):
        text, _ = pseudonymize("NIR 1 57 03 75 116 042 31")
        self.assertIn("[NIR]", text)


if __name__ == "__main__":
    unittest.main()
