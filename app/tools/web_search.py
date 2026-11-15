
from typing import Protocol


class WebSearchTool(Protocol):
    def search(self, query: str, max_results: int = 5) -> list[dict]:
        ...


class MockWebSearchTool:
    """Deterministic mock search tool. Replace with an approved provider adapter."""
    def __init__(self):
        self.records = [
            {
                "title": "OWASP guidance for LLM applications",
                "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
                "snippet": "LLM applications should address prompt injection, sensitive information disclosure, excessive agency and insecure output handling.",
                "keywords": {"security", "llm", "prompt", "injection", "agent", "risk"},
            },
            {
                "title": "LangGraph documentation",
                "url": "https://langchain-ai.github.io/langgraph/",
                "snippet": "LangGraph supports stateful, controllable agent workflows with graph nodes, edges and conditional routing.",
                "keywords": {"langgraph", "graph", "agent", "orchestration", "workflow"},
            },
            {
                "title": "NIST AI Risk Management Framework",
                "url": "https://www.nist.gov/itl/ai-risk-management-framework",
                "snippet": "The AI RMF provides a voluntary framework for managing risks across AI system design, development, deployment and use.",
                "keywords": {"nist", "risk", "governance", "ai", "framework"},
            },
            {
                "title": "OWASP Web Security Testing Guide",
                "url": "https://owasp.org/www-project-web-security-testing-guide/",
                "snippet": "The testing guide provides a structured approach to assessing web application security.",
                "keywords": {"testing", "security", "web", "application"},
            },
        ]

    def search(self, query: str, max_results: int = 5) -> list[dict]:
        terms = set(query.lower().replace("?", " ").split())
        ranked = []
        for record in self.records:
            score = len(terms & record["keywords"])
            if score:
                ranked.append((score, record))
        ranked.sort(key=lambda pair: pair[0], reverse=True)
        return [
            {
                "title": r["title"],
                "url": r["url"],
                "snippet": r["snippet"],
                "score": float(score),
            }
            for score, r in ranked[:max_results]
        ]
