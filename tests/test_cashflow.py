from datetime import date

import pandas as pd
import pytest

from ashish_ops_analytics.cashflow import (
    assess_receivables,
    build_followup_email,
    daily_recovery_digest,
)


def sample_invoices():
    return pd.DataFrame({
        "invoice_id": ["INV-1", "INV-2", "INV-3"],
        "customer_name": ["Sample A", "Sample B", "Sample C"],
        "site": ["Site A", "Site B", "Site C"],
        "invoice_date": ["2026-10-01", "2026-10-10", "2026-11-01"],
        "due_date": ["2026-10-31", "2026-11-10", "2026-11-30"],
        "invoice_amount": [100000, 50000, 25000],
        "amount_received": [20000, 0, 0],
        "payment_promise_date": ["2026-11-05", "", ""],
        "missing_documents": ["", "Attendance certificate", ""],
        "dispute_flag": [False, False, False],
    })


def test_assess_receivables_calculates_balance_ageing_and_actions():
    result = assess_receivables(sample_invoices(), as_of=date(2026, 11, 23))
    first = result.loc[result["invoice_id"] == "INV-1"].iloc[0]
    second = result.loc[result["invoice_id"] == "INV-2"].iloc[0]
    third = result.loc[result["invoice_id"] == "INV-3"].iloc[0]

    assert first["amount_outstanding"] == 80000
    assert first["days_overdue"] == 23
    assert first["missed_promise"] is True or bool(first["missed_promise"])
    assert "missed payment commitment" in first["next_action"]
    assert "Attendance certificate" in second["next_action"]
    assert third["days_to_due"] == 7


def test_daily_digest_reports_outstanding_and_blockers():
    result = assess_receivables(sample_invoices(), as_of=date(2026, 11, 23))
    digest = daily_recovery_digest(result)
    assert digest["invoice_count"] == 3
    assert digest["open_invoice_count"] == 3
    assert digest["total_outstanding"] == 155000
    assert digest["overdue_invoice_count"] == 2
    assert digest["missing_document_count"] == 1
    assert digest["missed_promise_count"] == 1


def test_followup_email_is_a_draft_and_never_sends():
    result = assess_receivables(sample_invoices(), as_of=date(2026, 11, 23))
    row = result.loc[result["invoice_id"] == "INV-1"].iloc[0]
    draft = build_followup_email(row)
    assert "INV-1" in draft["subject"]
    assert "₹80,000.00" in draft["body"]
    assert draft["send_status"].startswith("Draft only")


def test_assess_receivables_rejects_invalid_amounts():
    df = sample_invoices()
    df.loc[0, "invoice_amount"] = -100
    with pytest.raises(ValueError):
        assess_receivables(df, as_of=date(2026, 11, 23))



def test_priority_score_orders_urgent_invoice_before_larger_low_risk_invoice():
    df = sample_invoices()
    df.loc[df["invoice_id"] == "INV-1", "invoice_amount"] = 200000
    df.loc[df["invoice_id"] == "INV-1", "amount_received"] = 0
    df.loc[df["invoice_id"] == "INV-1", "due_date"] = "2026-11-30"
    df.loc[df["invoice_id"] == "INV-1", "payment_promise_date"] = ""
    df.loc[df["invoice_id"] == "INV-2", "invoice_amount"] = 50000
    df.loc[df["invoice_id"] == "INV-2", "due_date"] = "2026-10-10"
    result = assess_receivables(df, as_of=date(2026, 11, 23))

    assert result.iloc[0]["invoice_id"] == "INV-2"
    assert result.iloc[0]["priority_score"] > result.iloc[1]["priority_score"]
