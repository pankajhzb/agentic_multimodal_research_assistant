
from ..tools.web_search import WebSearchTool


class WebSearchAgent:
    def __init__(self, search_tool: WebSearchTool):
        self.search_tool = search_tool

    def run(self, query: str) -> dict:
        try:
            hits = self.search_tool.search(query, max_results=5)
            sources = [{
                "source_type": "external_web",
                "title": h["title"],
                "reference": h["url"],
                "url": h["url"],
                "excerpt": h["snippet"],
                "score": h.get("score"),
            } for h in hits]
            if not sources:
                return {
                    "answer": "The external search tool returned no matching results.",
                    "sources": [],
                    "error": None,
                }
            answer = "Relevant external information:\n" + "\n".join(
                f"- {s['excerpt']}" for s in sources
            )
            return {"answer": answer, "sources": sources, "error": None}
        except Exception as exc:
            return {
                "answer": "",
                "sources": [],
                "error": f"Web search failed: {type(exc).__name__}: {exc}",
            }
