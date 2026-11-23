# SQL case studies

These examples run in DuckDB against the committed synthetic CSV files. They demonstrate analyst-style SQL: aggregation, CTEs, window functions, business metric definitions and reconciliation logic.

From the repository root:

```bash
python -c "import duckdb; c=duckdb.connect(); c.execute(open('sql/collection_recovery.sql').read()).show()"
```

Each query documents the business question and its assumptions. Reconciliation results remain candidates for human review.
