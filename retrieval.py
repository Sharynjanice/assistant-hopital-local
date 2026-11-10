"""Recherche documentaire BM25 (bibliothèque standard uniquement)."""
import math
import re
import unicodedata

STOP = set("le la les un une des de du d l et ou en a au aux dans sur pour par que qui quoi est sont etre avec sans ce cet "
           "cette ces se sa son ses leur leurs il elle ils elles on ne pas plus y quel quelle quels quelles combien quand "
           "comment faut ont fait fait-il".split())


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def tokenize(text: str) -> list[str]:
    tokens = []
    for w in re.findall(r"[a-z0-9]+", normalize(text)):
        if w in STOP or len(w) < 2:
            continue
        if len(w) > 4 and w[-1] in "sx":  # pluriel : racinisation très simple
            w = w[:-1]
        tokens.append(w)
    return tokens


def chunk_text(text: str, size: int = 60, overlap: int = 15) -> list[str]:
    words = text.split()
    if len(words) <= size:
        return [text]
    chunks, step = [], size - overlap
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks


class BM25Index:
    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.tokens = [tokenize(c["title"] + " " + c["text"]) for c in chunks]
        self.avg_len = sum(len(t) for t in self.tokens) / max(len(self.tokens), 1)
        self.df: dict[str, int] = {}
        for toks in self.tokens:
            for term in set(toks):
                self.df[term] = self.df.get(term, 0) + 1

    def search(self, query: str, k: int = 3, allowed=lambda chunk: True) -> list[tuple[float, dict]]:
        """Le filtre d'accès `allowed` est appliqué AVANT le calcul : un extrait interdit n'est jamais renvoyé."""
        q = tokenize(query)
        n = len(self.chunks)
        scored = []
        for chunk, toks in zip(self.chunks, self.tokens):
            if not allowed(chunk):
                continue
            score = 0.0
            for term in q:
                tf = toks.count(term)
                if tf == 0:
                    continue
                idf = math.log(1 + (n - self.df[term] + 0.5) / (self.df[term] + 0.5))
                score += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * len(toks) / self.avg_len))
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: -x[0])
        return scored[:k]
