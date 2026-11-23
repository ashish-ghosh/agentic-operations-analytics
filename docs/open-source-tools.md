# Open-source tools selected for this portfolio

The project uses a small number of libraries that directly support demonstrable skills.

| Project / library | Role here | License / note |
|---|---|---|
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Optional job-description analyst | MIT |
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Read-only tool server | MIT; this project targets the stable 2.x API |
| [DuckDB](https://github.com/duckdb/duckdb) | Local analytical SQL | MIT |
| [pandas](https://github.com/pandas-dev/pandas) | Data cleaning and transformations | BSD-3-Clause |
| [Streamlit](https://github.com/streamlit/streamlit) | Local analytics dashboard | Apache-2.0 |
| [Plotly](https://github.com/plotly/plotly.py) | Interactive charts | MIT |
| [Docling](https://github.com/docling-project/docling) | Optional future invoice / contract parsing | MIT codebase; individual model licences can differ |
| [dbt Core](https://github.com/dbt-labs/dbt-core) | Next-stage analytics engineering practice | Apache-2.0 |
| [Prefect](https://github.com/PrefectHQ/prefect) | Future data-pipeline orchestration study | Apache-2.0 |

## Why these tools

- SQL, pandas, DuckDB and dbt build a credible analytics-engineering foundation.
- Streamlit and Plotly make analytical output easy to demonstrate.
- MCP lets an LLM host call clearly scoped read-only analytics tools.
- OpenAI Agents SDK supports the optional career-analysis workflow with a local function tool.
- Docling is deferred to an optional extra because document AI models may add significant installation size and model-specific licence requirements.
- Prefect is a later learning track, not another dependency in the first release.

## Install

```bash
pip install -e ".[dev]"
```

Optional document parsing:

```bash
pip install -e ".[documents]"
```

No upstream repository has been copied into this project. Use each dependency through its package distribution and retain its respective licence notices.
