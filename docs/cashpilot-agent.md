# CashPilot — Agentic Cashflow Recovery Appliance

**Owner:** Ashish Ghosh  
**Initial niche:** Indian facility-management contractors, housekeeping/security agencies and manpower service providers.  
**Status:** Zero-cost local MVP specification and synthetic-data engine. No customer accounts connected; no live messages sent; no production deployment.

## The problem

Service contractors often need to collect invoices while continuing to fund payroll, statutory obligations, materials and site operations. A generic payment reminder is not enough: invoices may be blocked by missing work orders, attendance certificates, service-entry approvals, disputed quantities or customer-side approval delays.

The product is an agentic invoice-to-cash workflow that finds the blocker, proposes the next action and keeps the follow-up process moving.

## Product promise

**Every morning, tell the business which invoices need attention, what is blocking collection, what evidence is missing and what action should happen next.**

## First-release workflow

1. Read invoice balances and due dates from an approved CSV export or accounting connector.
2. Search approved Drive folders for work orders, service certificates and attendance evidence.
3. Review relevant Gmail threads and classify customer replies as payment promise, dispute, missing-document request, payment confirmation or unknown.
4. Calculate outstanding balances and ageing deterministically.
5. Rank the work queue using transparent rules, not a claimed prediction of payment probability.
6. Prepare personalised email drafts and follow-up tasks.
7. Match bank statement entries to receivables as candidate suggestions only.
8. Produce a daily collection digest and 7/30-day expected-cash view.
9. Ask the operator to approve any external message or write.

## Why this is not another reminder bot

Zoho Books already includes invoice reminders, bank reconciliation and a free plan. The product must not compete on sending reminders.

The specialised wedge is the cross-app follow-through:
- Identify missing proof that prevents client approval.
- Read the email thread to understand the actual blocker.
- Connect contract/WO/attendance evidence to the invoice.
- Track payment promises and broken promises.
- Prioritise collection action against the contractor's payroll and site-cash obligations.
- Keep the customer's existing accounting system as the system of record.

## Composio integration plan

Use Composio as the integration/authentication layer, not as the product itself.

### Initial connectors
- Zoho Books: read invoice, customer, payment and balance data (optional; the current development connection is not authorised).
- Gmail: read relevant invoice conversations and create follow-up drafts.
- Google Drive: search for work orders, attendance sheets and service-acceptance documents.
- Google Sheets: read existing AR trackers and write a separate action register only after approval.
- Google Calendar: schedule owner follow-ups.
- WhatsApp Business: defer to a later phase because a Business account, approved templates, permissions and provider charges may be required.

Each business must connect its own accounts using a distinct stable Composio user ID. Never use Ashish's personal Gmail, Drive or Sheets credentials for a customer tenant. Scope each session to required tools and accounts. Keep customer data isolated.

### Agent boundaries
- Read-only by default.
- Email actions create drafts, never send automatically.
- Spreadsheet updates require explicit approval.
- No payment initiation, invoice deletion, ledger posting, payroll changes or legal debt-collection actions.
- Preserve source links/IDs and record an audit trail for every suggested action.
- Never use personal data or employer-confidential records in the public demo.

## Free-first implementation stack

| Layer | Choice | Cost approach |
|---|---|---|
| Agent framework | Composio + LangGraph or OpenAI Agents adapter | OSS framework; Composio free tier within limits |
| Model | Ollama with a commercially licensed open-weight model | Local inference; hardware is not free |
| Data processing | Python, pandas, DuckDB | Open source |
| PDF extraction | pypdf; local OCR only for scans | Open source; review document licence |
| API | FastAPI | Open source |
| Demo | Existing Streamlit portfolio app | No Lovable credits |
| Tests and source control | GitHub Actions + public repository | Free usage limits apply |
| Initial storage | Local SQLite/CSV synthetic data | No cloud database spend |
| Production cloud | Do not select until a paid pilot | Hosting and uptime will eventually cost money |

Important: Composio's Platform free tier advertises monthly usage limits, but premium provider tools, message delivery, LLM APIs and hosting may still cost money. OpenAI API usage is billed separately from a ChatGPT subscription. The first version therefore uses deterministic rules and local inference, with no OpenAI API dependency.

## Pricing experiments — not validated market prices

1. Free one-day sample analysis with synthetic data only.
2. ₹1,499 one-time onboarding for a single-business, read-only pilot.
3. ₹2,999/month Starter: one legal entity, limited active invoices and daily action queue.
4. ₹4,999/month Business: more invoices/sites, document checks, email-thread classification and weekly cash outlook.

Do not publish pricing until at least five qualified buyer conversations have been completed. Do not guarantee recovered money or payment dates.

## Who to interview first

- Facility-management contractors managing several client sites.
- Housekeeping, security and manpower agencies.
- Small electrical/mechanical maintenance contractors.
- Finance/accounts managers who chase client approvals and overdue invoices.

## 14-day validation gate

- Interview 15 qualified owners/accounts heads.
- Request two sample anonymised receivables workflows.
- Demonstrate the agent against synthetic or explicitly approved data.
- Offer three paid pilots at ₹1,499 onboarding plus a proposed ₹2,999 monthly plan.
- Continue only if at least two buyers agree to a paid pilot or provide a specific, credible purchasing path.
- If nobody will pay, stop or change the niche before adding more code.

## Revenue reality

This is not guaranteed daily income and it is not passive at launch. Initial revenue will be irregular onboarding/pilot fees. Recurring monthly revenue is possible only when businesses keep paying for the ongoing workflow. Five customers at ₹2,999 would be ₹14,995 gross monthly revenue, before platform, hosting, support, taxes and delivery costs; this is a scenario, not a forecast.

## Next build stage

- Composio per-customer Connect Link and user isolation.
- Zoho Books/Gmail/Drive read-only adapters.
- Evidence-linked invoice blocker classifier.
- Operator approval inbox for follow-up drafts.
- Audit log and tenant isolation tests.
- Secure hosted pilot only after customer validation.
