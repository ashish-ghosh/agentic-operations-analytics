from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]


def run_sql(path: str):
    connection = duckdb.connect()
    try:
        return connection.execute((ROOT / path).read_text(encoding="utf-8")).df()
    finally:
        connection.close()


def test_collection_sql_produces_monthly_society_kpis():
    result = run_sql("sql/collection_recovery.sql")
    assert len(result) == 12
    assert {"month", "society", "amount_due", "amount_collected", "outstanding", "recovery_pct"}.issubset(result.columns)
    assert (result["outstanding"] >= 0).all()
    assert result["recovery_pct"].between(0, 100).all()


def test_complaint_sql_uses_declared_as_of_time():
    result = run_sql("sql/complaint_sla.sql")
    assert len(result) > 0
    assert "breached_including_open" in result.columns
    assert (result["ticket_count"] > 0).all()


def test_reconciliation_sql_returns_review_suggestions_not_postings():
    result = run_sql("sql/reconciliation_candidates.sql")
    assert len(result) > 0
    assert "review_status" in result.columns
    assert set(result["review_status"]).issubset({"high_confidence_review", "manual_review"})
    assert "resident_unit" in result.columns
