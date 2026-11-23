-- Business question: how many tickets met their SLA, and which categories carry the largest breach burden?
-- Open tickets are measured against a declared reporting timestamp, not the machine's current clock.
WITH params AS (
    SELECT TIMESTAMP '2026-11-10 00:00:00' AS as_of_utc
),
tickets AS (
    SELECT
        ticket_id,
        society,
        category,
        priority,
        CAST(created_at AS TIMESTAMPTZ) AS created_at,
        TRY_CAST(
            NULLIF(TRIM(CAST(resolved_at AS VARCHAR)), '')
            AS TIMESTAMPTZ
        ) AS resolved_at,
        CAST(sla_hours AS DOUBLE) AS sla_hours
    FROM read_csv_auto('sample_data/complaints.csv')
),
measured AS (
    SELECT
        t.*,
        COALESCE(t.resolved_at, p.as_of_utc) AS end_time,
        DATE_DIFF(
            'minute',
            t.created_at,
            COALESCE(t.resolved_at, p.as_of_utc)
        ) / 60.0 AS elapsed_hours
    FROM tickets t
    CROSS JOIN params p
)
SELECT
    society,
    category,
    COUNT(*) AS ticket_count,
    COUNT(*) FILTER (WHERE resolved_at IS NULL) AS open_tickets,
    COUNT(*) FILTER (WHERE elapsed_hours > sla_hours) AS breached_including_open,
    ROUND(AVG(elapsed_hours) FILTER (WHERE resolved_at IS NOT NULL), 2) AS avg_resolution_hours,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE resolved_at IS NOT NULL AND elapsed_hours <= sla_hours
        )
        / NULLIF(COUNT(*) FILTER (WHERE resolved_at IS NOT NULL), 0),
        2
    ) AS resolved_sla_compliance_pct
FROM measured
GROUP BY society, category
ORDER BY breached_including_open DESC, ticket_count DESC;
