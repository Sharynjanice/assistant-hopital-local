"""Utilisation :
  python ask.py stagiaire "Combien de caractères pour un mot de passe ?"
  python ask.py referent            (mode conversation)
  python ask.py --audit             (derniers échanges)
"""
import sys
import time

import audit
from documents import build_index
from llm import LLMUnavailable
from rag import ROLES, answer


def show(question, role, index):
    try:
        r = answer(question, role, index)
    except LLMUnavailable as e:
        print(f"Erreur : {e}")
        return
    print(f"\n{r['answer']}")
    print(f"Sources : {', '.join(r['sources']) or 'aucune'}  |  durée : {r['latency']} s\n")


def main(argv):
    if argv[:1] == ["--audit"]:
        for row in audit.last():
            print(time.strftime("%d/%m %H:%M:%S", time.localtime(row["ts"])), row["role"], "|", row["question"], "|", row["sources"], "|", row["latency_s"], "s")
        return
    if not argv or argv[0] not in ROLES:
        sys.exit(__doc__ + f"\nRôles : {', '.join(ROLES)}")
    role, index = argv[0], build_index()
    if len(argv) > 1:
        show(" ".join(argv[1:]), role, index)
        return
    print(f"Rôle : {role}. Tapez une question (ligne vide pour quitter).")
    while (q := input("> ").strip()):
        show(q, role, index)


if __name__ == "__main__":
    main(sys.argv[1:])
