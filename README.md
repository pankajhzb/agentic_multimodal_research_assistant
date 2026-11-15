
# Multi-Agent Multimodal RAG + Web Search (LangGraph)

A runnable reference implementation of a graph-based multi-agent application.

## Capabilities

- **Supervisor** classifies a query and routes to:
  - `rag`: internal multimodal knowledge corpus
  - `web`: external web-search tool (mock by default)
  - `both`: both retrieval agents
  - `neither`: neither retrieval agent; answer conversationally
- **Multimodal RAG** retrieves Markdown/text chunks and image assets using image captions, alt text and tags. It returns stable source references.
- **Web Search Agent** calls a replaceable search-tool interface. The included mock is deterministic and needs no API key.
- **Response synthesis** deduplicates evidence, labels internal vs external sources, handles partial failures, and produces a final response.
- **FastAPI** endpoint and automated tests.

> The included image retrieval is metadata/caption-based multimodal retrieval. It retrieves image assets using their descriptions and metadata; it does not perform visual understanding of arbitrary image pixels. For production visual retrieval, plug in OCR/captioning and a vision embedding model (for example, CLIP-compatible embeddings) in `rag/retriever.py`.

## Architecture

```text
                         User query
                             |
                      Supervisor Agent
                    route = rag/web/both/neither
                      /       |        \
                   RAG       Web      Neither
                    \         |        /
                     \        |       /
                      Response Synthesis
                              |
                        Final answer
```

The graph is implemented with LangGraph `StateGraph` and conditional edges. The supervisor and tool interfaces are deliberately kept replaceable so a production LLM classifier or managed search provider can be added without changing the graph topology.

## Project layout

```text
app/
  api.py                  FastAPI application
  graph.py                LangGraph graph definition
  schemas.py              Shared state and response models
  supervisor.py           Routing policy
  synthesis.py            Evidence deduplication and answer synthesis
  agents/
    rag_agent.py          Multimodal RAG agent
    web_agent.py          Web search agent
  rag/
    corpus.py             Corpus loading and chunking
    retriever.py          Text + image-metadata retrieval
  tools/
    web_search.py         Mock web search interface
data/
  docs/                   Internal knowledge corpus
  images/                 Example SVG image assets
  image_manifest.json     Image captions, alt text and tags
tests/
  test_routing.py
  test_graph.py
  test_retriever.py
```

## Run locally

Python 3.11+ recommended.

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.api:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain our claim approval workflow and show the process diagram"}'
```

## Run tests

```bash
pytest -q
```

## Example queries

| Query | Expected route | Why |
|---|---|---|
| `How does our claim approval workflow work?` | `rag` | Internal knowledge request |
| `What are the latest AI agent framework releases?` | `web` | Fresh external information |
| `Compare our approval process with current industry guidance` | `both` | Internal + external evidence |
| `Hello, what can you do?` | `neither` | No retrieval required |

## Replace the mock web search

The graph depends on the `WebSearchTool` protocol in `app/tools/web_search.py`.
Implement the same `search(query, max_results)` method using your approved provider
(for example, Tavily, Bing, SerpAPI, or an enterprise search API), then inject it into
`build_graph(...)`. Keep API keys in environment variables or a secrets manager.

## Replace the rule-based supervisor with an LLM

`app/supervisor.py` contains a deterministic baseline classifier. For production,
replace `classify_query()` with an LLM call that returns a validated structured
decision (`rag`, `web`, `both`, `neither`) plus a short rationale. Keep policy checks
outside the model: enforce allowed tools, query size limits, and authorization before
executing any tool.

## Production hardening checklist

- Add tenant-aware access control before retrieving internal documents.
- Use a vector store + hybrid keyword search and reranking for larger corpora.
- Add OCR/image captioning and multimodal embeddings for image understanding.
- Add document-level ACL filtering before retrieval.
- Add prompt-injection screening for retrieved content; treat documents and web pages as untrusted data.
- Add request timeouts, retries with backoff, rate limits and circuit breakers.
- Add tracing for graph nodes, retrieval scores, tool calls, latency and token/cost metrics.
- Persist conversation state only when required and apply retention policies.
- Add evaluation datasets for routing accuracy, retrieval recall, citation correctness and synthesis faithfulness.
- Keep external and internal evidence visibly separate in the final response.
