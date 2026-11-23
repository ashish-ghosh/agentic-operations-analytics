from datetime import date

import pandas as pd
import pytest

from ashish_ops_analytics.collections import collection_summary
from ashish_ops_analytics.complaints import complaint_sla_summary
from ashish_ops_analytics.habits import daily_plan
from ashish_ops_analytics.job_tracker import add_application, due_followups
from ashish_ops_analytics.quality import data_quality_report
from ashish_ops_analytics.reconciliation import suggest_matches


def test_collection_summary_calculates_recovery_and_outstanding():
    df = pd.DataFrame({"amount_due": [100, 200], "amount_collected": [80, 220]})
    result = collection_summary(df)
    assert result["total_due"] == 300
    assert result["total_collected"] == 300
    assert result["outstanding"] == 20
    assert result["over_collected"] == 20
    assert result["recovery_pct"] == 100


def test_collection_summary_rejects_invalid_values():
    with pytest.raises(ValueError):
        collection_summary(pd.DataFrame({"amount_due": [-1], "amount_collected": [0]}))


def test_data_quality_report_detects_missing_and_duplicates():
    df = pd.DataFrame({"id": [1, 1], "amount": [10, None]})
    result = data_quality_report(df, required_columns=["id", "amount", "date"])
    assert result["duplicate_rows"] == 0
    assert result["missing_required_columns"] == ["date"]
    assert result["missing_by_column"]["amount"] == 1
    assert result["status"] == "failed"


def test_complaint_sla_summary_uses_as_of_for_open_tickets():
    df = pd.DataFrame({
        "created_at": ["2026-11-01T00:00:00Z", "2026-11-01T00:00:00Z"],
        "resolved_at": ["2026-11-01T04:00:00Z", None],
        "sla_hours": [8, 8],
    })
    result = complaint_sla_summary(df, as_of="2026-11-01T12:00:00Z")
    assert result["resolved_tickets"] == 1
    assert result["open_tickets"] == 1
    assert result["sla_breaches_including_open"] == 1
    assert result["resolved_sla_compliance_pct"] == 100


def test_reconciliation_is_suggestion_only_and_matches_reference():
    bank = pd.DataFrame({
        "bank_transaction_id": ["B1"],
        "bank_date": ["2026-11-01"],
        "bank_amount": [1000],
        "reference": ["REF-1"],
    })
    ledger = pd.DataFrame({
        "ledger_entry_id": ["L1"],
        "ledger_date": ["2026-11-02"],
        "ledger_amount": [1000],
        "reference": ["REF-1"],
    })
    result = suggest_matches(bank, ledger)
    assert result.iloc[0]["ledger_entry_id"] == "L1"
    assert result.iloc[0]["confidence_score"] >= 85
    assert result.iloc[0]["status"] == "high_confidence_review"


def test_daily_plan_is_actionable_and_timeboxed():
    plan = daily_plan(date(2026, 11, 23))
    assert plan["total_minutes"] == 75
    assert len(plan["tasks"]) == 4


def test_job_tracker_writes_only_to_provided_local_path(tmp_path):
    target = tmp_path / "applications.csv"
    add_application("Example Co", "Data Analyst", "Naukri", path=target)
    result = due_followups(path=target, as_of=date(2026, 11, 23))
    assert target.exists()
    assert len(result) == 0
