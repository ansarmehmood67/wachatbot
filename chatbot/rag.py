import os
import json
import math
from openai import OpenAI

# Initialize OpenAI client for embeddings
rag_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _flatten(obj, prefix=""):
    """
    Recursively extract all string values from nested JSON.
    Returns list of (key, text) tuples.
    """
    items = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            items.extend(_flatten(v, new_key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            items.extend(_flatten(v, f"{prefix}[{i}]") )
    else:
        text = str(obj).strip()
        if text:
            items.append((prefix, text))
    return items

# Load and flatten JSON files
_passages = []
base_dir = os.path.join(os.path.dirname(__file__), "data")
for fname in ["marco_wizard_flow.json", "marco_tax_rules.json"]:
    path = os.path.join(base_dir, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for key, txt in _flatten(data):
        _passages.append({"id": f"{fname}:{key}", "text": txt})

# Embed passages once at import time
_embeddings = []
for p in _passages:
    resp = rag_client.embeddings.create(
        model="text-embedding-3-small",
        input=p["text"]
    )
    emb = resp.data[0].embedding
    _embeddings.append(emb)


def _cosine(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0


def retrieve(query: str, top_k: int = 5):
    """
    Return the top_k most relevant passages for the given query.
    """
    # Embed query
    q_resp = rag_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    q_emb = q_resp.data[0].embedding

    # Score each passage
    scores = [( _cosine(q_emb, emb), idx ) for idx, emb in enumerate(_embeddings)]
    # Select top_k
    scores.sort(key=lambda x: x[0], reverse=True)
    top = scores[:top_k]
    return [ _passages[idx]["text"] for _, idx in top ]
