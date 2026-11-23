# Agentic Operations Analytics

**Author:** Ashish Ghosh  
**Focus:** Business Intelligence • Data Analytics • Python • SQL • Agentic AI

A practical, open-source portfolio toolkit for analysing operational and financial workflows. It combines deterministic Python analytics with a read-only Model Context Protocol (MCP) server and an optional OpenAI agent interface.

The use cases reflect common facility-management and property-operations problems: maintenance collections, complaint SLA performance, bank-to-ledger reconciliation, data quality, job-search tracking and structured daily learning.

> **Data and safety:** All committed datasets are synthetic. The analytics and MCP tools are read-only. Job-search workflows are manual-assist tools: this project does not scrape LinkedIn or Naukri, log in to job portals, submit applications, or publish posts.

## What is included

| Module | Demonstration |
|---|---|
| Collection analytics | Recovery rate, outstanding amount, fully paid units and collection trend |
| Complaint analytics | Open tickets, SLA breaches, compliance rate and average resolution time |
| Reconciliation suggestions | Explainable amount/reference/date matching with review statuses; never posts ledger entries |
| Data quality | Missingness, duplicate rows, schema checks and row counts |
| Job tracker | Local CSV tracker and upcoming follow-ups for applications |
| Daily plan | Repeatable 60–75 minute learning, portfolio and job-search routine |
| LinkedIn content planner | Evidence-led post prompts; drafts remain human-reviewed |
| MCP server | Exposes selected sample-data analytics as read-only tools to MCP-compatible hosts |
| OpenAI agent | Optional job-description analysis against a transparent candidate profile |

## Technology choices

- **Python + pandas:** transparent analytical transformations.
- **DuckDB:** local analytical SQL for future case studies; included as a dependency.
- **Streamlit + Plotly:** interactive demonstration dashboard.
- **MCP Python SDK 2.x:** standard interface for read-only tools.
- **OpenAI Agents SDK:** optional job-description analysis with a local profile tool.
- **pytest + Ruff + GitHub Actions:** automated quality checks.

These upstream projects are dependencies, not copied source trees. Keep their own license notices and follow the terms of each dependency.

## Quick start

Requires Python 3.11 or newer.

```bash
git clone https://github.com/ashish-ghosh/agentic-operations-analytics.git
cd agentic-operations-analytics
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Run the dashboard

```bash
streamlit run src/ashish_ops_analytics/app.py
```

### Run the command-line tools

```bash
ops-analytics collections
ops-analytics complaints
ops-analytics quality maintenance_collections.csv
ops-analytics reconcile
ops-analytics daily-plan
ops-analytics job-followups
```

### Run tests and lint

```bash
pytest
ruff check .
```

### Run the read-only MCP server

```bash
ops-analytics-mcp
```

The server uses stdio by default. Configure the command in an MCP host only after reviewing that host's connection and data-access settings. It exposes sample-data summaries and does not write to MARS, GitHub, LinkedIn, Naukri or any external system.

### Run the optional job-description agent

Set an OpenAI API key in your local environment (never commit it), then run:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your-key"
# macOS/Linux
export OPENAI_API_KEY="your-key"

ops-analytics analyse-job --file path/to/job-description.txt
```

This optional command makes model API requests and may incur usage charges on your OpenAI API account. It is not needed for the local analytics, dashboard, tests or MCP server.

## Data contract

The sample files in `sample_data/` are intentionally small and synthetic:

- `maintenance_collections.csv`: one row per society/month with units, amount due and collected.
- `complaints.csv`: ticket timestamps, priority, category, vendor and SLA target.
- `bank_transactions.csv` and `ledger_entries.csv`: synthetic reconciliation candidates.
- `job_applications_template.csv`: schema for a local job-search tracker.

For personal use, point `OPS_DATA_DIR` to a local folder containing files with the same expected names. Do not place real resident data, bank statements, API keys or employer-confidential material in this public repository.

## Analytical assumptions

- Collection recovery is calculated as total collected divided by total billed/due for the reporting rows. Outstanding is floored at zero per row; over-collection is surfaced separately.
- Complaint SLA compliance is based on elapsed time against the row's SLA target. Open tickets are assessed against the supplied `as_of` timestamp or current UTC time.
- Reconciliation output is a **candidate suggestion**, not an accounting decision. Amount, date and reference evidence are scored transparently; a human must review ambiguous matches before posting anything.
- The sample forecasting and prioritisation material is educational, not financial advice or a promise of predictive accuracy.

## Portfolio status

This is an actively developed portfolio project. The first release is a demonstrable local toolkit; external connectors, hosted MCP access, production data integrations and commercial multi-tenant operation are not included.

See:
- [Architecture](docs/architecture.md)
- [Six-month transition roadmap](docs/six-month-roadmap.md)
- [Job-search workflow](docs/job-search-workflow.md)
- [Open-source tool inventory](docs/open-source-tools.md)
- [Safety and data-handling notes](docs/safety-and-data-handling.md)
- [Portfolio and resume positioning](docs/resume-positioning.md)

## License

MIT. See [LICENSE](LICENSE).
