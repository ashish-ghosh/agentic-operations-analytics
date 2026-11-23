# Cloud tools, ChatGPT connectivity and monetisation plan

**Owner:** Ashish Ghosh  
**Review date:** 2026-11-23  
**Scope:** MARS / Society Harmony, Agentic Operations Analytics, career portfolio and product opportunities.

This document distinguishes reviewed GitHub projects from installed software and connected accounts. A repository link is not an installation. A catalogue item is not an authenticated connection. A local MCP process is not a hosted ChatGPT integration.

## 1. Recommended tool shortlist

| Tool | Official repository | Why it fits | Decision |
|---|---|---|---|
| Langflow | https://github.com/langflow-ai/langflow | Visual agent workflows; exposes workflows over API and as an MCP server; can also connect to other MCP servers. MIT licence. | **First agent platform to evaluate** |
| Chatwoot | https://github.com/chatwoot/chatwoot | Omnichannel customer support for MARS: web chat, email and messaging inbox; MIT licence; self-hosting and cloud options. | **Product support layer candidate** |
| PostHog | https://github.com/PostHog/posthog | Product analytics, funnels, feature flags and event analysis. Official hosted MCP server is documented in its monorepo. | **First product analytics connection** |
| Inngest | https://github.com/inngest/inngest | Durable event-driven background jobs, retries and scheduled workflows. Lovable connector catalogue contains an Inngest integration. | **Preferred workflow engine** |
| Sentry | https://github.com/getsentry/sentry | Error and performance monitoring for the MARS and portfolio apps. Lovable connector catalogue contains Sentry. | **First observability connection** |
| Docling | https://github.com/docling-project/docling | Extract structured information from invoices, statements and contracts. | **Document intelligence phase** |
| Activepieces | https://github.com/activepieces/activepieces | Workflow automation with MIT community core and separately licensed enterprise features. | **Not selected now**; similar category to n8n, which the owner does not want to use |
| Dify | https://github.com/langgenius/dify | LLM app platform with RAG and visual agent workflows; cloud or self-hosted options. | **Internal prototype only until licensing is reviewed** |
| ERPNext | https://github.com/frappe/erpnext | Full ERP with accounting, asset, procurement and operations modules. GPL-3.0. | **Study/integration candidate; do not copy into MARS** |

### Exclusions and licence risks

- **Flowise**: its own repository README says the repository has been archived. Do not select it for new production work.
- **Dify**: its current source licence adds conditions around multi-tenant service operation and preserving logo/copyright. Obtain appropriate permission or legal review before building a multi-tenant commercial service on it.
- **ERPNext**: GPL-3.0. Treat it as a separate product or evaluate integration; do not mix its source into a proprietary MARS codebase without a licence review.
- **Open WebUI**: current releases include additional branding conditions from v0.6.6 onward. Not selected for resale/white-label work without reviewing the exact release licence.

## 2. Recommended architecture

### MARS production application
- Lovable / React / TypeScript: existing application UI.
- Supabase / PostgreSQL: existing application data layer, subject to RLS and secret review.
- Razorpay: payment collection and payment webhooks.
- Inngest: background work such as payment-event processing, scheduled recovery reports and retryable notifications.
- WhatsApp Business / existing voice-provider adapters: resident communications, subject to provider approvals and template compliance.
- Sentry: runtime errors and performance.
- PostHog: adoption and funnel analytics, with privacy-conscious event design.
- Docling: future invoice and contract extraction in a separate processing service.

### Agentic workflow layer
- Langflow: build and test workflows visually.
- OpenAI Agents SDK: retain in the Python portfolio for code-first agents.
- MCP: expose limited, authenticated, read-only business analytics tools first.
- Human approval: required before payment, ledger, resident communication or CRM write operations.

## 3. ChatGPT connectivity status and limitations

The public portfolio currently contains a local stdio MCP server. It is not internet-accessible and is not connected to ChatGPT.

For a custom ChatGPT connection, the server must be reachable through a supported remote HTTPS endpoint or Secure MCP Tunnel, with authentication and a reviewed permission set.

Current OpenAI help material describes custom MCP support for Business and Enterprise/Edu workspaces; Pro can connect custom MCP servers with read/fetch permissions. ChatGPT Go is not listed as a supported custom-MCP tier in that documentation. Re-check plan availability before paying for hosting or upgrading.

The GitHub integration available through the connected Composio account is already usable in this workspace. This is distinct from a custom MCP server connection.

## 4. Current account-connection inventory

The Lovable workspace connector catalogue includes:
- Sentry
- PostHog
- Inngest
- Razorpay
- HubSpot
- WhatsApp Business
- GitHub API
- Google Sheets / Drive / Calendar
- AWS S3, BigQuery, GCP and Cloudflare

A catalogue entry marked enabled means the integration is available, not necessarily authenticated to an account.

The custom connector inventory currently shows two connected n8n MCP records. Do not use n8n in new workflows. Remove the duplicate records manually only after reviewing the relevant workspace connector settings; the current management tools do not expose a safe removal action.

Connector additions require the owner to open Lovable's connector dashboard and complete the provider's OAuth or API-key setup. Do not store provider secrets in frontend code or public GitHub repositories.

## 5. Passive-income product ladder

### Product A — Society Operations MIS Starter Kit
A downloadable pack built from original templates:
- Monthly maintenance recovery tracker.
- Defaulter ageing report.
- Complaint and SLA dashboard.
- Vendor scorecard.
- Bank reconciliation review sheet.
- KPI dictionary and setup guide.

**Buyer:** society managers, facility supervisors, small property managers and accounting teams.  
**Revenue model:** one-time digital download; offer a paid setup add-on.

### Product B — MARS Reconciliation Add-on
A paid MARS module for payment reference matching, bank-versus-ledger exceptions and review queues.

**Buyer:** housing societies and property managers.  
**Revenue model:** recurring add-on subscription or per-society plan.  
**Control:** never post unmatched transactions automatically; customer approval is required.

### Product C — Operations Intelligence subscription
Scheduled monthly dashboards for collections, complaints, vendor SLA, water/energy usage and operating costs.

**Buyer:** builders, facility management operators and multi-site property managers.  
**Revenue model:** monthly subscription or reporting contract.

### Product D — Invoice and AMC Intelligence
A document-processing add-on that extracts invoice/AMC data, compares contract rates and flags renewal dates.

**Buyer:** property operations and procurement teams.  
**Revenue model:** subscription or per-document pricing.

## 6. Validation before monetisation

Do not assume downloads or GitHub stars create revenue. Validate demand before hosting spend.

1. Interview 10 society/facility managers and 5 accounting users.
2. Identify the three most repetitive spreadsheet/reporting tasks.
3. Show a synthetic-data demonstration and ask for a paid pilot commitment.
4. Build only the highest-frequency workflow.
5. Test with one customer using written scope, synthetic or approved data and human review.
6. Price after understanding the current manual cost, time saved and willingness to pay.
7. Publish a downloadable starter kit only after its instructions, sample data and calculations are tested.

Price experiments should be treated as hypotheses, not forecasts. Do not promise a particular monthly income.

## 7. 30 / 60 / 90 day execution

### Days 1–30: foundations
- Run the current Streamlit analytics portfolio locally.
- Create the first downloadable MIS pack from the sample CSVs.
- Connect Sentry and PostHog through Lovable after the owner completes OAuth.
- Evaluate Inngest on a non-production project.
- Review and rotate any privileged secret found in the private MARS repository's tracked .env file.

### Days 31–60: customer validation
- Demonstrate the MIS kit to 10 prospects.
- Collect feedback and record which reports they would pay for.
- Build one paid-pilot workflow.
- Add product analytics and error monitoring only after event privacy is reviewed.

### Days 61–90: first commercial test
- Deliver one small pilot.
- Document onboarding, support and data-handling procedures.
- Offer the template pack as a separate low-cost product.
- Measure conversion, setup time, support effort and gross margin before scaling.

## 8. Approval gates

The following require explicit approval before execution:
- Connecting an external provider account or entering credentials.
- Deploying any cloud service or publicly exposing an MCP endpoint.
- Paid hosting, API usage, upgrades or subscriptions.
- Live Razorpay credentials, live payments or customer data.
- Publishing sales pages, LinkedIn posts or outbound messages.
- Production database changes and migrations.

## Sources

- Langflow repository and MIT licence: https://github.com/langflow-ai/langflow
- Langflow MCP server documentation: https://docs.langflow.org/mcp-server
- Chatwoot repository and MIT licence: https://github.com/chatwoot/chatwoot
- PostHog official MCP documentation: https://posthog.com/docs/model-context-protocol
- PostHog MCP source location: https://github.com/PostHog/posthog/tree/master/services/mcp
- Inngest repository: https://github.com/inngest/inngest
- Sentry JavaScript SDK: https://github.com/getsentry/sentry-javascript
- Docling repository: https://github.com/docling-project/docling
- Dify source licence: https://github.com/langgenius/dify/blob/main/LICENSE
- Flowise archived README: https://github.com/FlowiseAI/Flowise
- ERPNext licence: https://github.com/frappe/erpnext
- Activepieces licence details: https://github.com/activepieces/activepieces/blob/main/docs/about/license.mdx
- OpenAI custom MCP availability: https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt
