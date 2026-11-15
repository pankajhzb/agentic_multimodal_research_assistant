
from pathlib import Path
from collections import Counter
from typing import Any
from .corpus import load_corpus


def _score(query_tokens: set[str], document_tokens: set[str]) -> float:
    if not query_tokens or not document_tokens:
        return 0.0
    overlap = len(query_tokens & document_tokens)
    # Simple normalized overlap baseline; replace with hybrid BM25/vector retrieval.
    return overlap / (len(query_tokens) ** 0.5 * len(document_tokens) ** 0.5)


class MultimodalRetriever:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.text_items, self.image_items = load_corpus(data_dir)

    def retrieve(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        import re
        q_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        results: list[dict[str, Any]] = []

        for item in self.text_items:
            score = _score(q_tokens, item["tokens"])
            if score > 0:
                results.append({
                    "source_type": "internal_text",
                    "title": item["title"],
                    "reference": item["reference"],
                    "excerpt": item["text"][:700],
                    "score": round(score, 4),
                })

        for item in self.image_items:
            score = _score(q_tokens, item["tokens"])
            if score > 0:
                results.append({
                    "source_type": "internal_image",
                    "title": item["title"],
                    "reference": item["path"],
                    "excerpt": item.get("caption", ""),
                    "score": round(score, 4),
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
