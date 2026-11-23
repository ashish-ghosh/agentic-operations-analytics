-- Business question: what are billed, collected and outstanding amounts by society/month?
-- Data source: synthetic sample_data/maintenance_collections.csv
WITH collections AS (
    SELECT
        CAST(month || '-01' AS DATE) AS month,
        society,
        CAST(units AS INTEGER) AS units,
        CAST(amount_due AS DECIMAL(18, 2)) AS amount_due,
        CAST(amount_collected AS DECIMAL(18, 2)) AS amount_collected
    FROM read_csv_auto('sample_data/maintenance_collections.csv')
),
monthly AS (
    SELECT
        month,
        society,
        SUM(units) AS units,
        SUM(amount_due) AS amount_due,
        SUM(amount_collected) AS amount_collected,
        SUM(GREATEST(amount_due - amount_collected, 0)) AS outstanding
    FROM collections
    GROUP BY month, society
)
SELECT
    month,
    society,
    units,
    amount_due,
    amount_collected,
    outstanding,
    ROUND(100.0 * amount_collected / NULLIF(amount_due, 0), 2) AS recovery_pct,
    ROUND(
        100.0 * amount_collected
        / NULLIF(SUM(amount_collected) OVER (PARTITION BY society), 0),
        2
    ) AS share_of_period_collections_pct
FROM monthly
ORDER BY society, month;
