"""Client Ollama (modèle local, aucune donnée ne quitte l'ordinateur)."""
import json
import os
import urllib.error
import urllib.request

DEFAULT_MODEL = "qwen2.5:1.5b"


class LLMUnavailable(Exception):
    pass


def generate(prompt: str, model: str | None = None, timeout: int = 300) -> str:
    model = model or os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434") + "/api/generate"
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0.1, "num_ctx": 2048}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())["response"].strip()
    except urllib.error.URLError as e:
        raise LLMUnavailable(f"Ollama ne répond pas ({e}). Est-il lancé ? Le modèle « {model} » est-il téléchargé ?") from e
