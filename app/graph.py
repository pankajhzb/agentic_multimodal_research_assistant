
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from .schemas import GraphState
from .supervisor import classify_query
from .agents.rag_agent import MultimodalRAGAgent
from .agents.web_agent import WebSearchAgent
from .tools.web_search import MockWebSearchTool
from .synthesis import synthesize


def build_graph(data_dir: Path | None = None, web_search_tool=None):
    project_root = Path(__file__).resolve().parents[1]
    corpus_dir = data_dir or project_root / "data"
    rag_agent = MultimodalRAGAgent(corpus_dir)
    web_agent = WebSearchAgent(web_search_tool or MockWebSearchTool())

    def supervisor_node(state: GraphState):
        route, rationale = classify_query(state["query"])
        return {"route": route, "rationale": rationale, "warnings": []}

    def rag_node(state: GraphState):
        try:
            return {"rag_result": rag_agent.run(state["query"])}
        except Exception as exc:
            return {"rag_result": {
                "answer": "", "sources": [],
                "error": f"RAG failed: {type(exc).__name__}: {exc}"
            }}

    def web_node(state: GraphState):
        return {"web_result": web_agent.run(state["query"])}

    def no_retrieval_node(state: GraphState):
        return {
            "rag_result": {"answer": "", "sources": [], "error": None},
            "web_result": {"answer": "", "sources": [], "error": None},
        }

    def route_after_supervisor(state: GraphState):
        return state["route"]

    builder = StateGraph(GraphState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("rag", rag_node)
    builder.add_node("web", web_node)
    builder.add_node("no_retrieval", no_retrieval_node)
    builder.add_node("synthesis", lambda state: synthesize(state))

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "rag": "rag",
            "web": "web",
            "both": "rag",
            "neither": "no_retrieval",
        },
    )
    builder.add_conditional_edges(
        "rag",
        lambda state: "web" if state["route"] == "both" else "synthesis",
        {"web": "web", "synthesis": "synthesis"},
    )
    builder.add_edge("web", "synthesis")
    builder.add_edge("no_retrieval", "synthesis")
    builder.add_edge("synthesis", END)

    return builder.compile()


def ask(graph, query: str) -> dict:
    result = graph.invoke({"query": query})
    return {
        "query": query,
        "route": result.get("route", "neither"),
        "rationale": result.get("rationale", ""),
        "answer": result.get("answer", ""),
        "internal_sources": result.get("internal_sources", []),
        "external_sources": result.get("external_sources", []),
        "warnings": result.get("warnings", []),
    }
