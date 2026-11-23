from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "sample_data"

ALLOWED_SAMPLE_FILES = {
    "maintenance_collections.csv",
    "complaints.csv",
    "bank_transactions.csv",
    "ledger_entries.csv",
    "job_applications_template.csv",
    "cashflow_invoices.csv",
}


def data_directory() -> Path:
    """Return the configured local data directory, or the committed synthetic sample directory."""
    raw = os.getenv("OPS_DATA_DIR")
    if raw:
        return Path(raw).expanduser().resolve()
    return DEFAULT_DATA_DIR


def load_csv(filename: str) -> pd.DataFrame:
    """Load a known dataset from the configured data directory."""
    if filename not in ALLOWED_SAMPLE_FILES:
        raise ValueError(f"Dataset not allowed: {filename}")
    path = data_directory() / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"{path} does not exist. Copy the sample file or set OPS_DATA_DIR locally."
        )
    return pd.read_csv(path)


def local_job_tracker_path() -> Path:
    """Return a local-only job tracker path that is excluded from Git."""
    raw = os.getenv("OPS_DATA_DIR")
    base = Path(raw).expanduser().resolve() if raw else REPO_ROOT / "data"
    return base / "job_applications.csv"
