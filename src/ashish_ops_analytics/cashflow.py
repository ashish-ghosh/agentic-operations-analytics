from __future__ import annotations

from datetime import date

import pandas as pd


REQUIRED_COLUMNS = {
    "invoice_id",
    "customer_name",
    "site",
    "invoice_date",
    "due_date",
    "invoice_amount",
    "amount_received",
}


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "disputed"}


def _age_bucket(days_overdue: int) -> str:
    if days_overdue <= 0:
        return "Not overdue"
    if days_overdue <= 7:
        return "1–7 days"
    if days_overdue <= 30:
        return "8–30 days"
    if days_overdue <= 60:
        return "31–60 days"
    if days_overdue <= 90:
        return "61–90 days"
    return "Over 90 days"


def _next_action(row: pd.Series, as_of: date) -> str:
    if row["amount_outstanding"] <= 0:
        return "Closed — no collection action"
    if row["missing_documents"]:
        return f"Complete missing documents: {row['missing_documents']}"
    if row["dispute_flag"]:
        return "Assign an owner to resolve the customer dispute"
    promise = row["payment_promise_date"]
    if pd.notna(promise) and promise.date() < as_of:
        return "Follow up on the missed payment commitment"
    if pd.notna(promise) and 0 <= (promise.date() - as_of).days <= 3:
        return f"Check payment commitment due {promise.date().isoformat()}"
    if row["days_overdue"] > 0:
        return "Prepare an overdue invoice follow-up"
    if row["days_to_due"] <= 3:
        return "Confirm invoice receipt and payment readiness"
    return "Monitor until next review"


def _priority_score(row: pd.Series) -> int:
    """Transparent work-queue score; not a prediction of payment probability."""
    overdue_points = min(50, max(0, int(row["days_overdue"])))
    amount_points = min(25, max(0.0, float(row["amount_outstanding"]) / 20_000))
    document_points = 10 if row["missing_documents"] else 0
    dispute_points = 10 if row["dispute_flag"] else 0
    promise_points = 10 if row["missed_promise"] else 0
    due_soon_points = 8 if 0 <= int(row["days_to_due"]) <= 3 else 0
    return min(
        100,
        int(round(
            overdue_points + amount_points + document_points
            + dispute_points + promise_points + due_soon_points
        )),
    )


def assess_receivables(df: pd.DataFrame, as_of: date | None = None) -> pd.DataFrame:
    """Create a daily collections work queue from invoices; performs no external actions."""
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    result = df.copy()
    for col in ("invoice_date", "due_date"):
        result[col] = pd.to_datetime(result[col], errors="coerce")
        if result[col].isna().any():
            raise ValueError(f"{col} contains invalid or empty dates")

    if "payment_promise_date" not in result.columns:
        result["payment_promise_date"] = pd.NaT
    else:
        result["payment_promise_date"] = pd.to_datetime(
            result["payment_promise_date"], errors="coerce"
        )

    for col in ("invoice_amount", "amount_received"):
        result[col] = pd.to_numeric(result[col], errors="coerce")
        if result[col].isna().any():
            raise ValueError(f"{col} must contain valid numeric values")
        if (result[col] < 0).any():
            raise ValueError(f"{col} cannot contain negative values")

    current_day = as_of or date.today()
    result["amount_outstanding"] = (
        result["invoice_amount"] - result["amount_received"]
    ).clip(lower=0).round(2)
    result["days_overdue"] = result["due_date"].apply(
        lambda value: max(0, (current_day - value.date()).days)
    )
    result["days_to_due"] = result["due_date"].apply(
        lambda value: (value.date() - current_day).days
    )
    result["age_bucket"] = result["days_overdue"].apply(_age_bucket)

    if "missing_documents" not in result.columns:
        result["missing_documents"] = ""
    result["missing_documents"] = result["missing_documents"].fillna("").astype(str).str.strip()
    if "dispute_flag" not in result.columns:
        result["dispute_flag"] = False
    result["dispute_flag"] = result["dispute_flag"].apply(_as_bool)

    result["missed_promise"] = result["payment_promise_date"].apply(
        lambda value: bool(pd.notna(value) and value.date() < current_day)
    )
    result["next_action"] = result.apply(
        lambda row: _next_action(row, current_day), axis=1
    )
    result["priority_score"] = result.apply(_priority_score, axis=1)

    return result.sort_values(
        ["priority_score", "amount_outstanding"],
        ascending=[False, False],
    ).reset_index(drop=True)


def daily_recovery_digest(assessed: pd.DataFrame) -> dict:
    """Summarise receivables and operational blockers for a daily review."""
    if "amount_outstanding" not in assessed.columns or "days_overdue" not in assessed.columns:
        raise ValueError("Pass the result of assess_receivables()")

    open_items = assessed.loc[assessed["amount_outstanding"] > 0].copy()
    overdue = open_items.loc[open_items["days_overdue"] > 0]
    missing_docs = open_items.loc[open_items["missing_documents"].astype(str).str.len() > 0]
    disputed = open_items.loc[open_items["dispute_flag"]]
    missed_promises = open_items.loc[open_items["missed_promise"]]

    return {
        "invoice_count": int(len(assessed)),
        "open_invoice_count": int(len(open_items)),
        "overdue_invoice_count": int(len(overdue)),
        "total_outstanding": round(float(open_items["amount_outstanding"].sum()), 2),
        "overdue_outstanding": round(float(overdue["amount_outstanding"].sum()), 2),
        "missing_document_count": int(len(missing_docs)),
        "disputed_invoice_count": int(len(disputed)),
        "missed_promise_count": int(len(missed_promises)),
        "priority_actions": open_items.head(10)[
            [
                "invoice_id",
                "customer_name",
                "site",
                "amount_outstanding",
                "days_overdue",
                "priority_score",
                "next_action",
            ]
        ].to_dict("records"),
    }


def build_followup_email(row: pd.Series) -> dict:
    """Create a human-reviewed email draft; never sends a message."""
    invoice_id = str(row.get("invoice_id", ""))
    customer = str(row.get("customer_name", "Customer"))
    balance = float(row.get("amount_outstanding", 0))
    due_date = pd.Timestamp(row.get("due_date")).date().isoformat()
    subject = f"Payment status request — Invoice {invoice_id}"
    body = (
        f"Hello {customer},\n\n"
        f"We are following up on invoice {invoice_id} for ₹{balance:,.2f}, "
        f"which had a due date of {due_date}.\n\n"
        "Could you please confirm the current approval/payment status and advise "
        "whether any supporting document or clarification is still required from our side?\n\n"
        "Please share the expected payment date or the specific issue holding up processing.\n\n"
        "Regards,\nAccounts Team"
    )
    return {"subject": subject, "body": body, "send_status": "Draft only — human approval required"}
