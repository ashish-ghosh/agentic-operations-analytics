-- Business question: identify bank and ledger entries that could refer to the same payment.
-- This is intentionally a candidate report, not an automatic accounting match.
WITH bank AS (
    SELECT
        bank_transaction_id,
        CAST(bank_date AS DATE) AS bank_date,
        CAST(bank_amount AS DECIMAL(18, 2)) AS bank_amount,
        LOWER(TRIM(reference)) AS reference
    FROM read_csv_auto('sample_data/bank_transactions.csv')
),
ledger AS (
    SELECT
        ledger_entry_id,
        CAST(ledger_date AS DATE) AS ledger_date,
        CAST(ledger_amount AS DECIMAL(18, 2)) AS ledger_amount,
        LOWER(TRIM(reference)) AS reference,
        resident_unit
    FROM read_csv_auto('sample_data/ledger_entries.csv')
),
candidates AS (
    SELECT
        b.bank_transaction_id,
        l.ledger_entry_id,
        l.resident_unit,
        ABS(b.bank_amount - l.ledger_amount) AS amount_difference,
        ABS(DATE_DIFF('day', b.bank_date, l.ledger_date)) AS date_difference_days,
        (b.reference <> '' AND b.reference = l.reference) AS reference_match,
        CASE WHEN b.reference <> '' AND b.reference = l.reference THEN 15 ELSE 0 END
          + GREATEST(0, 60 - 60 * ABS(b.bank_amount - l.ledger_amount) / 1.0)
          + GREATEST(0, 25 - 5 * ABS(DATE_DIFF('day', b.bank_date, l.ledger_date))) AS evidence_score
    FROM bank b
    JOIN ledger l
      ON ABS(b.bank_amount - l.ledger_amount) <= 1.0
     AND ABS(DATE_DIFF('day', b.bank_date, l.ledger_date)) <= 5
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY bank_transaction_id ORDER BY evidence_score DESC) AS candidate_rank
    FROM candidates
)
SELECT
    bank_transaction_id,
    ledger_entry_id,
    resident_unit,
    amount_difference,
    date_difference_days,
    reference_match,
    ROUND(LEAST(evidence_score, 100), 2) AS evidence_score,
    CASE WHEN evidence_score >= 85 THEN 'high_confidence_review' ELSE 'manual_review' END AS review_status
FROM ranked
WHERE candidate_rank = 1
ORDER BY bank_transaction_id;
