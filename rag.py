"""Assistant RAG : contrôle d'accès par rôle -> recherche -> réponse sourcée -> journal d'audit."""
import os
import time

import audit
import llm as llm_module

# Quels niveaux de confidentialité chaque rôle peut consulter.
ROLES = {"stagiaire": {"public"}, "referent": {"public", "restreint"}}
NO_INFO = "Je ne trouve pas cette information dans les documents auxquels vous avez accès."

PROMPT_V1 = """Tu es un assistant pour les agents d'un hôpital. Réponds en français, en 2 à 4 phrases, \
UNIQUEMENT à partir des extraits ci-dessous. Cite la source entre crochets, par exemple [charte_informatique]. \
Si la réponse n'est pas dans les extraits, réponds exactement : « {no_info} »

Extraits :
{context}

Question : {question}
Réponse :"""

# Variante 2 : même consigne + un exemple (sans rapport avec le corpus) qui montre le format de citation attendu.
PROMPT_V2 = PROMPT_V1.replace("Extraits :\n{context}", """Exemple de réponse attendue :
Extrait : [exemple_doc] Le parking visiteurs ferme à 20 h.
Question : À quelle heure ferme le parking visiteurs ?
Réponse : Le parking visiteurs ferme à 20 h. [exemple_doc]

Extraits :
{context}""")
PROMPTS = {"v1": PROMPT_V1, "v2": PROMPT_V2}


def prompt_version() -> str:
    return os.environ.get("RAG_PROMPT", "v1")


def answer(question: str, role: str, index, k: int = 3, llm=None) -> dict:
    """Retourne {answer, sources, latency, llm_used}. `llm` peut être remplacé (tests)."""
    if role not in ROLES:
        raise ValueError(f"Rôle inconnu : {role}. Rôles possibles : {', '.join(ROLES)}")
    llm = llm or llm_module.generate
    levels = ROLES[role]
    start = time.time()
    hits = index.search(question, k=k, allowed=lambda c: c["level"] in levels)
    sources = list(dict.fromkeys(c["doc"] for _, c in hits))
    if not hits:  # rien de pertinent : on n'appelle pas le modèle, donc il ne peut pas inventer
        result = {"answer": NO_INFO, "sources": [], "llm_used": False}
    else:
        context = "\n".join(f"[{c['doc']}] {c['text']}" for _, c in hits)
        text = llm(PROMPTS[prompt_version()].format(no_info=NO_INFO, context=context, question=question))
        result = {"answer": text, "sources": sources, "llm_used": True}
    result["latency"] = round(time.time() - start, 2)
    audit.log(role, question, sources, result["llm_used"], result["latency"], os.environ.get("OLLAMA_MODEL", llm_module.DEFAULT_MODEL))
    return result
