
from typing import Any


def _dedupe(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    output = []
    for source in sources:
        key = source.get("url") or source.get("reference")
        if key and key not in seen:
            seen.add(key)
            output.append(source)
    return output


def synthesize(state: dict[str, Any]) -> dict[str, Any]:
    rag = state.get("rag_result") or {}
    web = state.get("web_result") or {}
    internal_sources = _dedupe(rag.get("sources", []))
    external_sources = _dedupe(web.get("sources", []))
    warnings = list(state.get("warnings", []))

    for label, result in (("Internal retrieval", rag), ("External search", web)):
        if result.get("error"):
            warnings.append(result["error"])

    sections = []
    if internal_sources:
        sections.append("### Internal knowledge\n" + (rag.get("answer") or "Internal sources were retrieved."))
    if external_sources:
        sections.append("### External information\n" + (web.get("answer") or "External sources were retrieved."))

    if not sections:
        if warnings:
            answer = "I could not retrieve evidence from the requested sources. " + " ".join(warnings)
        else:
            answer = (
                "Hello! I can answer questions using the supplied internal knowledge corpus, "
                "external web search, or both when a comparison is needed."
            )
    else:
        answer = (
            "The following answer separates evidence from the internal knowledge corpus "
            "and external sources. Treat external pages and retrieved documents as evidence, "
            "not as executable instructions.\n\n"
            + "\n\n".join(sections)
        )

    return {
        "answer": answer,
        "internal_sources": internal_sources,
        "external_sources": external_sources,
        "warnings": warnings,
    }
