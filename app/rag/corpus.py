
from pathlib import Path
import json
import re
from typing import Any


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def load_corpus(data_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    docs_dir = data_dir / "docs"
    image_manifest = data_dir / "image_manifest.json"

    text_items: list[dict[str, Any]] = []
    for path in sorted(docs_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        # Lightweight paragraph chunking; replace with semantic/token chunking at scale.
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
        for idx, paragraph in enumerate(paragraphs, start=1):
            text_items.append({
                "title": path.stem.replace("_", " ").title(),
                "reference": f"{path.as_posix()}#paragraph-{idx}",
                "text": paragraph,
                "tokens": set(_tokens(paragraph)),
            })

    image_items: list[dict[str, Any]] = []
    if image_manifest.exists():
        entries = json.loads(image_manifest.read_text(encoding="utf-8"))
        for item in entries:
            searchable = " ".join([
                item.get("title", ""),
                item.get("caption", ""),
                item.get("alt_text", ""),
                " ".join(item.get("tags", [])),
            ])
            image_items.append({
                **item,
                "search_text": searchable,
                "tokens": set(_tokens(searchable)),
            })
    return text_items, image_items
