# Architecture

## Local-first design

```text
Synthetic / user-approved CSV files
              |
              v
       pandas validation
              |
      +-------+--------+----------------+
      |                |                |
      v                v                v
Collection KPIs   Complaint SLA   Reconciliation suggestions
      |                |                |
      +----------------+----------------+
                       |
              +--------+--------+
              |                 |
              v                 v
        Streamlit UI       CLI reports
              |
              v
       Read-only MCP server
              |
       MCP-compatible host

Optional: OpenAI Agents SDK job-description analyst
        (user-supplied job description; no portal actions)
```

## Safety boundaries

- The MCP server exposes read-only analytics functions over known CSV filenames.
- Reconciliation creates candidate suggestions only. It does not write bank or ledger records.
- Job applications are entered manually into a local CSV file ignored by Git.
- The optional AI career analyst sees a declared candidate profile and user-provided job-description text only.
- No LinkedIn or Naukri scraping, browser automation, credential storage, auto-apply or auto-publishing is included.
- All committed demonstration records are synthetic.

## Extending safely

A future hosted MCP deployment must add authentication, tenant isolation, request limits, observability and explicit data-source allowlists. Do not expose a local file path or an unrestricted SQL execution tool to a public MCP server.
