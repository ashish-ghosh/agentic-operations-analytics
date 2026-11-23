from __future__ import annotations

import pandas as pd


BANK_REQUIRED = {"bank_transaction_id", "bank_date", "bank_amount", "reference"}
LEDGER_REQUIRED = {"ledger_entry_id", "ledger_date", "ledger_amount", "reference"}


def suggest_matches(
    bank: pd.DataFrame,
    ledger: pd.DataFrame,
    amount_tolerance: float = 1.0,
    date_window_days: int = 5,
) -> pd.DataFrame:
    """Produce explainable one-to-one candidates; never post accounting entries."""
    missing_bank = sorted(BANK_REQUIRED - set(bank.columns))
    missing_ledger = sorted(LEDGER_REQUIRED - set(ledger.columns))
    if missing_bank or missing_ledger:
        raise ValueError(
            f"Missing bank columns: {missing_bank}; missing ledger columns: {missing_ledger}"
        )
    if amount_tolerance < 0 or date_window_days < 0:
        raise ValueError("Tolerances must be non-negative")

    bank_rows = bank.copy()
    ledger_rows = ledger.copy()
    bank_rows["bank_date"] = pd.to_datetime(bank_rows["bank_date"], errors="coerce", utc=True)
    ledger_rows["ledger_date"] = pd.to_datetime(
        ledger_rows["ledger_date"], errors="coerce", utc=True
    )
    bank_rows["bank_amount"] = pd.to_numeric(bank_rows["bank_amount"], errors="coerce")
    ledger_rows["ledger_amount"] = pd.to_numeric(ledger_rows["ledger_amount"], errors="coerce")

    if bank_rows[["bank_date", "bank_amount"]].isna().any().any():
        raise ValueError("Bank data contains invalid dates or amounts")
    if ledger_rows[["ledger_date", "ledger_amount"]].isna().any().any():
        raise ValueError("Ledger data contains invalid dates or amounts")

    remaining = set(ledger_rows.index)
    suggestions: list[dict] = []

    for _, bank_row in bank_rows.sort_values("bank_date").iterrows():
        candidates = []
        for idx in remaining:
            ledger_entry = ledger_rows.loc[idx]
            amount_diff = abs(
                float(bank_row["bank_amount"]) - float(ledger_entry["ledger_amount"])
            )
            date_diff = abs(
                (bank_row["bank_date"] - ledger_entry["ledger_date"]).total_seconds()
            ) / 86400

            if amount_diff > amount_tolerance or date_diff > date_window_days:
                continue

            bank_ref = str(bank_row["reference"]).strip().casefold()
            ledger_ref = str(ledger_entry["reference"]).strip().casefold()
            reference_match = bool(bank_ref and bank_ref == ledger_ref)
            amount_score = 60.0 if amount_tolerance == 0 and amount_diff == 0 else (
                max(0.0, 60.0 * (1 - amount_diff / max(amount_tolerance, 0.01)))
            )
            date_score = 25.0 if date_window_days == 0 and date_diff == 0 else (
                max(0.0, 25.0 * (1 - date_diff / max(date_window_days, 0.01)))
            )
            score = min(100.0, amount_score + date_score + (15.0 if reference_match else 0.0))
            candidates.append(
                (score, amount_diff, date_diff, reference_match, idx, ledger_entry)
            )

        if not candidates:
            suggestions.append({
                "bank_transaction_id": str(bank_row["bank_transaction_id"]),
                "ledger_entry_id": None,
                "amount_difference": None,
                "date_difference_days": None,
                "reference_match": False,
                "confidence_score": 0.0,
                "status": "unmatched",
            })
            continue

        score, amount_diff, date_diff, reference_match, idx, ledger_entry = max(
            candidates, key=lambda item: item[0]
        )
        status = "high_confidence_review" if score >= 85 else "manual_review"
        suggestions.append({
            "bank_transaction_id": str(bank_row["bank_transaction_id"]),
            "ledger_entry_id": str(ledger_entry["ledger_entry_id"]),
            "amount_difference": round(amount_diff, 2),
            "date_difference_days": round(date_diff, 2),
            "reference_match": reference_match,
            "confidence_score": round(score, 2),
            "status": status,
        })
        remaining.remove(idx)

    return pd.DataFrame(suggestions)
