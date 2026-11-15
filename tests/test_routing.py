
from app.supervisor import classify_query


def test_internal_query_routes_to_rag():
    route, _ = classify_query("How does our claim approval workflow work?")
    assert route == "rag"


def test_current_external_query_routes_to_web():
    route, _ = classify_query("What are the latest AI agent framework releases?")
    assert route == "web"


def test_internal_external_comparison_routes_to_both():
    route, _ = classify_query("Compare our internal approval workflow with current industry guidance")
    assert route == "both"


def test_greeting_routes_to_neither():
    route, _ = classify_query("Hello, what can you do?")
    assert route == "neither"
