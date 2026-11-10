"""Chargement des documents (en-tête : Titre / Accès / Source, puis le texte)."""
import os

from retrieval import BM25Index, chunk_text

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "documents")


def load_chunks(folder: str = DOCS_DIR) -> list[dict]:
    chunks = []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".txt"):
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            raw = f.read()
        head, _, body = raw.partition("\n\n")
        meta = {}
        for line in head.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip().lower()] = value.strip()
        doc_id = name[:-4]
        for i, text in enumerate(chunk_text(body.strip())):
            chunks.append({"doc": doc_id, "title": meta.get("titre", doc_id),
                           "level": meta.get("accès", "public"), "text": text, "n": i})
    return chunks


def build_index(folder: str = DOCS_DIR) -> BM25Index:
    return BM25Index(load_chunks(folder))
