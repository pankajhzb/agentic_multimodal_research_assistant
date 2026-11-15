
import re
from .schemas import Route

INTERNAL_TERMS = {
    "our", "internal", "company", "enterprise", "policy", "policies",
    "claim", "claims", "workflow", "approval", "case", "knowledge base",
    "documentation", "runbook", "process", "corpus", "show the diagram",
}
WEB_TERMS = {
    "latest", "current", "today", "recent", "news", "2026", "2025",
    "market", "industry guidance", "compare with", "external", "internet",
    "web", "official documentation", "release", "version",
}


def classify_query(query: str) -> tuple[Route, str]:
    """
    Deterministic routing baseline.
    Replace with an LLM structured-output classifier if desired, but retain
    policy validation and a safe fallback around the model response.
    """
    q = query.lower()
    tokens = set(re.findall(r"[a-z0-9]+", q))

    internal_hit = any(term in q for term in INTERNAL_TERMS)
    web_hit = any(term in q for term in WEB_TERMS)

    # Explicit requests for both internal comparison and current/external context.
    comparison = any(p in q for p in (
        "compare", "versus", " vs ", "against", "difference between"
    ))
    if internal_hit and web_hit:
        return "both", "The query asks for internal knowledge and external/current information."
    if comparison and internal_hit:
        return "both", "The query requests a comparison involving internal knowledge."
    if web_hit:
        return "web", "The query depends on current or external information."
    if internal_hit:
        return "rag", "The query asks about the supplied internal knowledge corpus."

    # Greetings and general capability questions do not need retrieval.
    if tokens.intersection({"hello", "hi", "hey", "thanks", "thank", "help"}):
        return "neither", "The query is conversational and does not require retrieval."

    return "neither", "No clear need for internal or external retrieval was detected."
