from __future__ import annotations

import pandas as pd


def complaint_sla_summary(df: pd.DataFrame, as_of: str | None = None) -> dict:
    """Measure complaint resolution time and SLA compliance using UTC timestamps."""
    required = {"created_at", "resolved_at", "sla_hours"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    created = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
    resolved = pd.to_datetime(df["resolved_at"], utc=True, errors="coerce")
    sla = pd.to_numeric(df["sla_hours"], errors="coerce")
    if created.isna().any() or sla.isna().any() or (sla <= 0).any():
        raise ValueError("created_at must be valid and sla_hours must be positive")
    if (resolved.dropna() < created[resolved.notna()]).any():
        raise ValueError("resolved_at cannot be earlier than created_at")

    reference_time = pd.Timestamp(as_of) if as_of else pd.Timestamp.now(tz="UTC")
    if reference_time.tzinfo is None:
        reference_time = reference_time.tz_localize("UTC")
    else:
        reference_time = reference_time.tz_convert("UTC")

    elapsed_resolved = (resolved - created).dt.total_seconds() / 3600
    elapsed_open = (reference_time - created).dt.total_seconds() / 3600
    elapsed = elapsed_resolved.where(resolved.notna(), elapsed_open)
    breached = elapsed > sla
    resolved_mask = resolved.notna()
    resolved_count = int(resolved_mask.sum())
    on_time = int((resolved_mask & ~breached).sum())
    compliance = (on_time / resolved_count * 100) if resolved_count else 0.0
    average_resolution = float(elapsed_resolved[resolved_mask].mean()) if resolved_count else 0.0

    return {
        "total_tickets": int(len(df)),
        "resolved_tickets": resolved_count,
        "open_tickets": int((~resolved_mask).sum()),
        "sla_breaches_including_open": int(breached.sum()),
        "resolved_on_time": on_time,
        "resolved_sla_compliance_pct": round(compliance, 2),
        "average_resolution_hours": round(average_resolution, 2),
    }
