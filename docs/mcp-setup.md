# MCP connection guide

## What this server exposes

The local server provides read-only tools over the repository's synthetic or explicitly selected local CSV datasets:

- `get_collection_kpis`
- `get_complaint_sla_summary`
- `profile_collection_data_quality`
- `suggest_bank_ledger_matches`

No tool writes to a bank ledger, sends resident messages, submits job applications, publishes LinkedIn content, or changes GitHub.

## Local setup

Install the project:

```bash
python -m pip install -e ".[dev]"
```

Run the server:

```bash
ops-analytics-mcp
```

The entry point uses the MCP Python SDK over stdio. Use it with a local MCP-compatible host that supports stdio server definitions. Example configuration (adjust the absolute paths for your computer):

```json
{
  "mcpServers": {
    "ashish-operations-analytics": {
      "command": "C:/path/to/project/.venv/Scripts/ops-analytics-mcp.exe",
      "args": [],
      "env": {
        "OPS_DATA_DIR": "C:/path/to/project/sample_data"
      }
    }
  }
}
```

Do not set `OPS_DATA_DIR` to a folder containing resident phone numbers, real bank statements, or employer-confidential data when using a public or third-party AI host.

## ChatGPT connection requirements

ChatGPT cannot connect directly to a developer's local stdio process. A ChatGPT custom MCP connection requires a remotely reachable HTTPS MCP endpoint or a supported Secure MCP Tunnel. Workspace/account plan and admin policy determine whether custom MCP connections can be created and which actions are allowed.

This repository does **not** deploy a public MCP server. Do not expose the stdio process through an unauthenticated reverse proxy. A future hosted service needs authentication, per-user or per-tenant authorization, rate limits, audit logs, data-source allowlists, request-size limits and privacy controls before it can be used remotely.

The current server has read-only tools only. It should remain that way until a separate security review.

## ChatGPT app availability

Check the current ChatGPT workspace's Plugins / Apps interface and plan policy before expecting a custom server connection. Some plans support creating or testing custom MCP apps; other plans may not expose that option. If the option is unavailable, the local MCP server remains useful with other compatible developer hosts and as a portfolio demonstration.
