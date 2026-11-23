# Agentic Operations Analytics

**Author:** Ashish Ghosh  
**Focus:** Business Intelligence • Data Analytics • Python • SQL • Agentic AI

A practical, open-source portfolio toolkit for analysing operational and financial workflows. It combines deterministic Python analytics with a read-only Model Context Protocol (MCP) server and optional AI-agent workflows.

## Featured agentic workflow: CashPilot

CashPilot is a zero-cost, synthetic-data MVP for daily receivables prioritisation, designed initially for Indian facility-management contractors and manpower service providers.

It:
- Calculates outstanding balances and ageing.
- Identifies missing documentation, disputes and missed payment promises.
- Ranks a daily collection work queue using transparent rules.
- Prepares human-reviewed email drafts; it never sends automatically.
- Produces a daily recovery digest.

It is not a reminder bot and does not replace accounting software. The product hypothesis is that contractors need cross-app follow-through when invoices are blocked by missing approvals or evidence. That willingness to pay remains unvalidated.

See [CashPilot architecture and commercial validation plan](docs/cashpilot-agent.md).

## Other portfolio modules

| Module | Demonstration |
|---|---|
| Collection analytics | Recovery rate, outstanding amount and trends |
| Complaint analytics | Open tickets, SLA breaches and resolution time |
| Reconciliation suggestions | Explainable bank-to-ledger matching candidates |
| Data quality | Missingness, duplicate rows and schema checks |
| Career & Learning Hub | Local job tracker, follow-ups and habit scorecard |
| LinkedIn content planner | Evidence-led drafts; no automated publishing |
| MCP server | Read-only analytics tools |
| OpenAI agent | Optional job-description analysis |

## Technology choices

- Python, pandas and DuckDB for data analysis.
- Streamlit and Plotly for the dashboard.
- MCP Python SDK for read-only agent tools.
- OpenAI Agents SDK as an optional API-backed example.
- Composio for a future per-customer integration layer.
- pytest, Ruff and GitHub Actions for quality checks.

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

### Run CashPilot on synthetic invoice data

```bash
ops-analytics cashflow --as-of 2026-11-23
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

The MCP server uses stdio and sample-data tools. It is not a hosted ChatGPT integration.

## Data and safety

- All committed datasets are synthetic.
- CashPilot does not send emails, change accounting records, initiate payments or submit legal claims.
- Local job applications and habit records are excluded from Git.
- Never commit customer invoices, bank statements, employee payroll records, personal data or provider credentials.
- Composio integrations are planned per customer, with separate stable user IDs and least-privilege tools.
- Hosted multi-tenant service and customer OAuth connections are not implemented yet.

See [architecture](docs/architecture.md), [MCP setup](docs/mcp-setup.md), [security](docs/safety-and-data-handling.md), and [six-month roadmap](docs/six-month-roadmap.md).

## Licence

MIT. See [LICENSE](LICENSE).
