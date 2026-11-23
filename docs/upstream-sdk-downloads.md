# Downloaded upstream SDK repositories

**Prepared for:** Ashish Ghosh  
**Download date:** 2026-11-23  
**Purpose:** Reference source for cloud development, MCP integration and agent workflows.

These official upstream GitHub archives were downloaded and ZIP-tested. They are supplied separately from this project's original source code. No upstream source was copied into this repository, installed into MARS, or deployed.

| Repository | Why it matters | Licence | Archive state |
|---|---|---|---|
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | MCP servers and clients; stdio and Streamable HTTP transports. Official release page currently shows v2.3.0. | MIT | Downloaded from main branch; archive folder commit prefix 77001c9 |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | Code-first AI agents, tool calls, handoffs and guardrails. Archive package metadata reports openai-agents 0.25.0. | MIT | Downloaded from main branch; archive folder commit prefix 6c4e4a2 |
| [inngest/inngest-py](https://github.com/inngest/inngest-py) | Python SDK for durable, retryable background jobs and event-driven workflows. Archive package metadata reports inngest 0.5.20. | Apache-2.0 | Downloaded from main branch; archive folder commit prefix 1ae076f |

## How these fit the portfolio

### MCP Python SDK
Use it to expose tightly scoped, read-only operations analytics to an MCP host. The current portfolio server is a local stdio demonstration. For remote ChatGPT use, the server needs a reachable HTTPS endpoint or supported secure tunnel, plus an appropriate authentication design.

### OpenAI Agents SDK
Use it for the optional job-description analyst and future agent workflows. Keep tool permissions narrow and human approval in front of applications, messages, payments and accounting changes. API calls may incur OpenAI API charges.

### Inngest Python SDK
Use it when a workflow needs durable execution, retries, schedules or event triggers—for example, generating a monthly society collection report after a verified payment import. A real Inngest account and deployment must be configured separately.

## Download bundle

The reference bundle contains all three original upstream ZIP archives and a manifest with checksums. It is a separate download; no third-party archive is part of this repository's MIT distribution.

## Cloud development

This repository now includes `.devcontainer/devcontainer.json` for GitHub Codespaces. Use GitHub's **Code → Codespaces → Create codespace on main** flow to open it in a browser. Review your Codespaces quota and billing before creating one. The default setup installs only this portfolio's Python dependencies; it does not deploy a production service.

## ChatGPT connection status

The GitHub connector available in this ChatGPT session is already authorised and can access the user's repositories. This is separate from a custom MCP server.

OpenAI's current Help Center lists custom MCP connections for Business and Enterprise/Edu, with Pro support limited to read/fetch connections. ChatGPT Go is not listed among the supported plans on that page. Therefore this project must not be described as connected to a custom MCP server in the user's current Go plan. The local stdio server remains useful with compatible developer hosts.

## Licence handling

The upstream archives contain their own licence files. Preserve the original notices when modifying or redistributing those projects, and re-check each upstream licence before commercial reuse. A compatible package dependency does not mean the upstream code should be copied wholesale into a proprietary product.
