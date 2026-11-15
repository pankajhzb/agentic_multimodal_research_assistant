
from fastapi import FastAPI, HTTPException
from .graph import build_graph, ask
from .schemas import AskRequest, AskResponse

app = FastAPI(
    title="Multi-Agent Multimodal RAG + Web Search",
    version="1.0.0",
    description="Supervisor-routed LangGraph application with internal multimodal RAG and external search.",
)
graph = build_graph()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    try:
        result = ask(graph, request.query)
        return AskResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Request processing failed: {type(exc).__name__}",
        ) from exc
