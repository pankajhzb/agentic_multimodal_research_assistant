
from pathlib import Path
from app.graph import build_graph, ask


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_rag_route_returns_internal_sources():
    graph = build_graph(DATA_DIR)
    result = ask(graph, "How does our claim approval workflow work?")
    assert result["route"] == "rag"
    assert result["internal_sources"]
    assert result["external_sources"] == []


def test_web_route_returns_external_sources():
    graph = build_graph(DATA_DIR)
    result = ask(graph, "What is the latest guidance for prompt injection security?")
    assert result["route"] == "web"
    assert result["external_sources"]


def test_both_route_separates_evidence():
    graph = build_graph(DATA_DIR)
    result = ask(graph, "Compare our internal approval workflow with current industry guidance")
    assert result["route"] == "both"
    assert result["internal_sources"]
    assert result["external_sources"]
    assert "Internal knowledge" in result["answer"]
    assert "External information" in result["answer"]


def test_neither_route_does_not_retrieve():
    graph = build_graph(DATA_DIR)
    result = ask(graph, "Hello, what can you do?")
    assert result["route"] == "neither"
    assert result["internal_sources"] == []
    assert result["external_sources"] == []
    assert "Hello" in result["answer"]
