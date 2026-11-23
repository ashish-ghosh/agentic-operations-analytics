from __future__ import annotations

from typing import Iterable

import pandas as pd


def data_quality_report(df: pd.DataFrame, required_columns: Iterable[str] = ()) -> dict:
    """Summarise missing values, duplicate rows and missing required columns."""
    missing = {str(col): int(count) for col, count in df.isna().sum().items()}
    missing_pct = {
        str(col): round(float(count) / len(df) * 100, 2) if len(df) else 0.0
        for col, count in df.isna().sum().items()
    }
    required = list(required_columns)
    absent = [col for col in required if col not in df.columns]
    duplicate_rows = int(df.duplicated().sum())
    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": [str(col) for col in df.columns],
        "missing_by_column": missing,
        "missing_pct_by_column": missing_pct,
        "duplicate_rows": duplicate_rows,
        "missing_required_columns": absent,
        "status": "failed" if absent else ("review" if duplicate_rows or any(missing.values()) else "passed"),
    }
