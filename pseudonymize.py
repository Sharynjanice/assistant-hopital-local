"""Pseudonymisation de textes (démonstration sur des données FICTIVES).
Limite : approche par règles. Elle ne détecte pas tous les noms (ex. un nom sans titre « M. », « Mme », « Dr »)."""
import re
import sys

TITLE = r"(?:M\.|Mme|Mr|Madame|Monsieur|Dr|Docteur)"
NAME = r"[A-ZÉÈ][A-Za-zéèêëàâîïôöûüç'-]+"
RULES = [
    ("NIR", re.compile(r"\b[12](?:\s?\d{2}){3}\s?\d{3}\s?\d{3}\s?\d{2}\b")),
    ("TEL", re.compile(r"\b0[1-9](?:[ .]?\d{2}){4}\b")),
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("DATE", re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")),
]
PERSON = re.compile(rf"\b({TITLE})\s+({NAME}(?:\s+{NAME})?)")


def pseudonymize(text: str) -> tuple[str, dict]:
    """Retourne (texte pseudonymisé, compteurs). Une même personne reçoit toujours le même jeton."""
    persons: dict[str, str] = {}
    counts: dict[str, int] = {}

    def person(m):
        name = m.group(2)
        kind = "PROFESSIONNEL" if m.group(1) in ("Dr", "Docteur") else "PERSONNE"
        surname = name.split()[-1]
        key = f"{kind}:{name}"
        if key not in persons:
            # « Mme Garnier » après « Mme Sophie Garnier » : même personne, même jeton
            known = next((v for k, v in persons.items() if k.startswith(kind + ":") and k.split()[-1] == surname), None)
            persons[key] = known or f"[{kind}_{len({v for k, v in persons.items() if k.startswith(kind)}) + 1}]"
        counts[kind] = counts.get(kind, 0) + 1
        return persons[key]

    text = PERSON.sub(person, text)
    for label, pattern in RULES:
        text, n = pattern.subn(f"[{label}]", text)
        if n:
            counts[label] = n
    return text, counts


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/notes_patients_fictives.txt"
    out = sys.argv[2] if len(sys.argv) > 2 else "data/notes_pseudonymisees.txt"
    with open(src, encoding="utf-8") as f:
        result, counts = pseudonymize(f.read())
    with open(out, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Écrit : {out}\nÉléments remplacés : {counts}")
