
from typing import Any, Literal, TypedDict
from pydantic import BaseModel, Field

Route = Literal["rag", "web", "both", "neither"]


class Source(BaseModel):
    source_type: Literal["internal_text", "internal_image", "external_web"]
    title: str
    reference: str
    excerpt: str = ""
    score: float | None = None
    url: str | None = None


class AgentResult(BaseModel):
    answer: str = ""
    sources: list[Source] = Field(default_factory=list)
    error: str | None = None


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)


class AskResponse(BaseModel):
    query: str
    route: Route
    rationale: str
    answer: str
    internal_sources: list[Source]
    external_sources: list[Source]
    warnings: list[str] = Field(default_factory=list)


class GraphState(TypedDict, total=False):
    query: str
    route: Route
    rationale: str
    rag_result: dict[str, Any]
    web_result: dict[str, Any]
    answer: str
    internal_sources: list[dict[str, Any]]
    external_sources: list[dict[str, Any]]
    warnings: list[str]
