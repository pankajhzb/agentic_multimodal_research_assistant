
from pathlib import Path
from app.rag.retriever import MultimodalRetriever


def test_retriever_returns_text_and_image_for_claim_workflow():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    retriever = MultimodalRetriever(data_dir)
    hits = retriever.retrieve("claim approval workflow diagram", top_k=10)
    kinds = {h["source_type"] for h in hits}
    assert "internal_text" in kinds
    assert "internal_image" in kinds
