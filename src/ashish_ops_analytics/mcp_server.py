from __future__ import annotations

import json

from mcp.server import MCPServer

from ashish_ops_analytics.collections import collection_summary
from ashish_ops_analytics.complaints import complaint_sla_summary
from ashish_ops_analytics.io import load_csv
from ashish_ops_analytics.quality import data_quality_report
from ashish_ops_analytics.reconciliation import suggest_matches

mcp = MCPServer("Ashish Operations Analytics")


@mcp.tool()
def get_collection_kpis() -> str:
    """Read the configured maintenance collection dataset and return recovery KPIs as JSON."""
    df = load_csv("maintenance_collections.csv")
    return json.dumps(collection_summary(df), ensure_ascii=False)


@mcp.tool()
def get_complaint_sla_summary() -> str:
    """Read the configured complaints dataset and return SLA and resolution metrics as JSON."""
    df = load_csv("complaints.csv")
    return json.dumps(complaint_sla_summary(df), ensure_ascii=False)


@mcp.tool()
def profile_collection_data_quality() -> str:
    """Report missingness, duplicate rows and schema health for the collection sample dataset."""
    df = load_csv("maintenance_collections.csv")
    report = data_quality_report(df, required_columns=["month", "society", "amount_due", "amount_collected"])
    return json.dumps(report, ensure_ascii=False)


@mcp.tool()
def suggest_bank_ledger_matches() -> str:
    """Return explainable candidate matches from the sample bank and ledger CSVs; writes nothing."""
    bank = load_csv("bank_transactions.csv")
    ledger = load_csv("ledger_entries.csv")
    suggestions = suggest_matches(bank, ledger)
    return suggestions.to_json(orient="records")


def run() -> None:
    """Start the MCP server over stdio for a local MCP-compatible host."""
    mcp.run()


if __name__ == "__main__":
    run()
