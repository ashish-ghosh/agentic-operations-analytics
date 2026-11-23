from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from ashish_ops_analytics.io import local_job_tracker_path

COLUMNS = [
    "company", "role", "source", "job_url", "applied_date", "stage",
    "next_followup_date", "notes",
]


def add_application(
    company: str,
    role: str,
    source: str,
    job_url: str = "",
    applied_date: str | None = None,
    next_followup_date: str = "",
    notes: str = "",
    path: Path | None = None,
) -> Path:
    """Append a manually entered application to a local CSV file."""
    if not company.strip() or not role.strip():
        raise ValueError("Company and role are required")
    target = path or local_job_tracker_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    exists = target.exists()
    row = {
        "company": company.strip(),
        "role": role.strip(),
        "source": source.strip() or "manual",
        "job_url": job_url.strip(),
        "applied_date": applied_date or date.today().isoformat(),
        "stage": "applied",
        "next_followup_date": next_followup_date,
        "notes": notes.strip(),
    }
    pd.DataFrame([row], columns=COLUMNS).to_csv(target, mode="a" if exists else "w",
                                                  header=not exists, index=False)
    return target


def due_followups(path: Path | None = None, as_of: date | None = None) -> pd.DataFrame:
    """Return follow-ups due today or earlier from the local tracker."""
    target = path or local_job_tracker_path()
    if not target.exists():
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(target).reindex(columns=COLUMNS)
    dates = pd.to_datetime(df["next_followup_date"], errors="coerce").dt.date
    cutoff = as_of or date.today()
    return df.loc[dates.notna() & (dates <= cutoff)].copy()
