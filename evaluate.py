"""Évaluation : python evaluate.py [--no-llm]   -> écrit evaluation_<modèle>_<prompt>.md
Mesures : le bon document est-il retrouvé ? la réponse contient-elle l'information attendue ? cite-t-elle sa source ?
Pour les questions sans réponse permise : l'assistant s'abstient-il, sans fuite d'information réservée ?"""
import json
import os
import sys

from documents import build_index
from rag import NO_INFO, ROLES, answer, prompt_version
from retrieval import normalize


def main(use_llm: bool) -> None:
    model_name = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b") if use_llm else "aucun (recherche seule)"
    index = build_index()
    level = {c["doc"]: c["level"] for c in index.chunks}
    with open(os.path.join("data", "eval_questions.json"), encoding="utf-8") as f:
        questions = json.load(f)
    rows, hits, kws, cites, abst, leaks, lat = [], 0, 0, 0, 0, 0, []
    n_answerable = sum(1 for q in questions if q["expected_doc"])
    n_blocked = len(questions) - n_answerable
    for q in questions:
        r = answer(q["question"], q["role"], index, llm=None if use_llm else (lambda p: "(modèle non utilisé)"))
        text = normalize(r["answer"])
        row = {"q": q["question"], "role": q["role"], "sources": ", ".join(r["sources"]) or "-", "latency": r["latency"],
               "answer": r["answer"].replace("\n", " ")}
        if q["expected_doc"]:
            row["retrieval"] = q["expected_doc"] in r["sources"]
            hits += row["retrieval"]
            if use_llm:
                row["info"] = all(normalize(k) in text for k in q["keywords"])
                row["cite"] = f"[{q['expected_doc']}]" in r["answer"]
                kws += row["info"]
                cites += row["cite"]
        else:
            row["leak"] = any(level[d] not in ROLES[q["role"]] for d in r["sources"]) or \
                (use_llm and any(normalize(x) in text for x in q.get("forbidden", [])))
            row["abstain"] = ((NO_INFO in r["answer"]) or not r["llm_used"] or normalize("ne trouve pas") in text) if use_llm else None
            leaks += row["leak"]
            abst += bool(row["abstain"]) and not row["leak"]
        lat.append(r["latency"])
        rows.append(row)
    mark = lambda v: "oui" if v else "NON"
    lines = ["# Rapport d'évaluation", "", f"Modèle : {model_name}  ", f"Prompt : {prompt_version()}  ", f"Questions : {len(questions)}", "",
             "| Question | Rôle | Sources | Doc retrouvé | Info correcte | Source citée | Abstention / fuite | Durée (s) |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        blocked = ("abstention " + (mark(r["abstain"]) if r["abstain"] is not None else "non évaluée") + ", fuite " + mark(r["leak"])) if "leak" in r else "-"
        lines.append(f"| {r['q']} | {r['role']} | {r['sources']} | {mark(r['retrieval']) if 'retrieval' in r else '-'} | "
                     f"{mark(r['info']) if 'info' in r else '-'} | {mark(r['cite']) if 'cite' in r else '-'} | {blocked} | {r['latency']} |")
    lines += ["", "## Synthèse", f"- Bon document retrouvé : {hits}/{n_answerable}"]
    if use_llm:
        lines += [f"- Information attendue présente dans la réponse : {kws}/{n_answerable}", f"- Source citée correctement : {cites}/{n_answerable}",
                  f"- Questions sans réponse permise : abstention correcte {abst}/{n_blocked}"]
    else:
        lines += ["- Questions sans réponse permise : abstention non évaluée (modèle requis)"]
    lines += [f"- Fuites d'information réservée : {leaks}", f"- Durée moyenne : {sum(lat) / len(lat):.1f} s",
              "", "## Réponses du modèle (pour analyser les erreurs)", ""]
    lines += [f"- **{r['q']}** ({r['role']}) : {r['answer']}" for r in rows]
    safe = model_name.replace(":", "_").replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
    path = f"evaluation_{safe}_{prompt_version()}.md" if use_llm else "evaluation_recherche_seule.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(l for l in lines if l.startswith("- ") and "**" not in l))
    print(f"\nRapport complet : {path}")


if __name__ == "__main__":
    main("--no-llm" not in sys.argv)
