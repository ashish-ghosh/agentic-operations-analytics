from __future__ import annotations

import pandas as pd


def collection_summary(df: pd.DataFrame) -> dict:
    """Calculate billed, collected, outstanding and recovery KPIs from one row per unit or period."""
    required = {"amount_due", "amount_collected"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    due = pd.to_numeric(df["amount_due"], errors="coerce")
    collected = pd.to_numeric(df["amount_collected"], errors="coerce")
    if due.isna().any() or collected.isna().any():
        raise ValueError("amount_due and amount_collected must contain valid numeric values")
    if (due < 0).any() or (collected < 0).any():
        raise ValueError("Amounts cannot be negative")

    total_due = float(due.sum())
    total_collected = float(collected.sum())
    outstanding = float((due - collected).clip(lower=0).sum())
    over_collected = float((collected - due).clip(lower=0).sum())
    fully_paid = int(((due > 0) & (collected >= due)).sum())
    recovery_pct = (total_collected / total_due * 100) if total_due else 0.0

    return {
        "records": int(len(df)),
        "total_due": round(total_due, 2),
        "total_collected": round(total_collected, 2),
        "outstanding": round(outstanding, 2),
        "over_collected": round(over_collected, 2),
        "recovery_pct": round(recovery_pct, 2),
        "fully_paid_records": fully_paid,
    }


def collection_by_period(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate collection values by month when a month field is available."""
    required = {"month", "amount_due", "amount_collected"}
    if not required.issubset(df.columns):
        raise ValueError(f"Required columns: {', '.join(sorted(required))}")
    result = (
        df.assign(
            amount_due=pd.to_numeric(df["amount_due"], errors="coerce"),
            amount_collected=pd.to_numeric(df["amount_collected"], errors="coerce"),
        )
        .groupby("month", as_index=False)[["amount_due", "amount_collected"]]
        .sum()
        .sort_values("month")
    )
    result["recovery_pct"] = (
        result["amount_collected"].div(result["amount_due"].replace(0, pd.NA)).fillna(0) * 100
    ).round(2)
    return result
