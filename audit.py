"""Journal d'audit des questions posées à l'assistant (SQLite)."""
import contextlib
import json
import os
import sqlite3
import time


@contextlib.contextmanager
def session():
    db = sqlite3.connect(os.environ.get("RAG_DB", "rag_audit.db"))
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS audit(ts REAL, role TEXT, question TEXT, sources TEXT,
                  llm_used INTEGER, latency_s REAL, model TEXT)""")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def log(role: str, question: str, sources: list[str], llm_used: bool, latency: float, model: str) -> None:
    with session() as db:
        db.execute("INSERT INTO audit VALUES (?,?,?,?,?,?,?)",
                   (time.time(), role, question, json.dumps(sources), int(llm_used), round(latency, 2), model))


def last(n: int = 20) -> list[sqlite3.Row]:
    with session() as db:
        return db.execute("SELECT * FROM audit ORDER BY ts DESC LIMIT ?", (n,)).fetchall()
