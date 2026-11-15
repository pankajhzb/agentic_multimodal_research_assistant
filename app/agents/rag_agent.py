
from pathlib import Path
from ..rag.retriever import MultimodalRetriever


class MultimodalRAGAgent:
    def __init__(self, data_dir: Path):
        self.retriever = MultimodalRetriever(data_dir)

    def run(self, query: str) -> dict:
        hits = self.retriever.retrieve(query)
        if not hits:
            return {
                "answer": "I could not find relevant material in the supplied internal knowledge corpus.",
                "sources": [],
                "error": None,
            }

        text_hits = [h for h in hits if h["source_type"] == "internal_text"]
        image_hits = [h for h in hits if h["source_type"] == "internal_image"]

        lines = []
        if text_hits:
            lines.append("Relevant internal knowledge:")
            lines.extend(f"- {h['excerpt']}" for h in text_hits[:3])
        if image_hits:
            lines.append("Relevant image assets:")
            lines.extend(
                f"- {h['title']}: {h['excerpt']} (asset: {h['reference']})"
                for h in image_hits
            )

        return {"answer": "\n".join(lines), "sources": hits, "error": None}
