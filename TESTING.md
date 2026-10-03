# Automated tests

`tests/` holds a pytest suite organized by build order, bottom of the stack
first. Each file is runnable on its own so you can verify one layer before
moving to the next.

| Stage | File | Covers |
|---|---|---|
| 1 | `test_01_config.py` | `config.py` - paths, provider switch, model resolution |
| 2 | `test_02_database.py` | `common/db.py` against a throwaway seeded database |
| 3 | `test_03_network_diagnostics_tools.py` | `adk-services/network_diagnostics/agent.py` tool functions |
| 4 | `test_04_billing_resolution_tools.py` | `adk-services/billing_resolution/agent.py`, incl. the $50 auto-approval rule |
| 5 | `test_05_orchestration_state.py` | `orchestration/state.py` shared state shape |
| 6 | `test_06_adk_remote_client.py` | `orchestration/adk_remote_client.py` "service not running" handling |
| 7 | `test_07_orchestration_graph.py` | `orchestration/graph.py` graph wiring |
| 8 | `test_08_rag_error_paths.py` | `llamaindex_rag/*` "index/DB not ready" handling |
| 9 | `test_09_crew_nodes_fallback.py` | `orchestration/crew_nodes.py` failure fallback text |

None of these tests call a real LLM, so no API key is required. Stages 3-4
need `google-adk` installed (already in `requirements.txt`) and skip
automatically if it isn't.

## Setup

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

## Running

```bash
# one stage at a time
pytest tests/test_01_config.py -v
pytest tests/test_02_database.py -v
...

# everything
pytest tests/ -v
```

What these tests intentionally don't cover: the actual LLM-routed supervisor
decisions, real RAG/semantic-SQL answers, and the live two-agent CrewAI
response. Those require a configured `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` and
are exercised manually via the scenarios in `HOW_TO_RUN.md`.
