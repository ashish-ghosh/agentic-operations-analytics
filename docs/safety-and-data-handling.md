# Safety, privacy and data handling

## Public repository rules

- Only synthetic demonstration records belong in Git.
- Never commit `.env`, API keys, access tokens, passwords, bank files, resident data, phone numbers, e-mail addresses or employer-confidential documents.
- The real local job application tracker is excluded by `.gitignore`.
- Use `.env.example` for variable names only. It contains no credentials.

## MCP boundaries

The MCP server exposes only four read-only analytics functions over known dataset filenames. It does not expose:
- arbitrary filesystem paths,
- unrestricted SQL,
- database writes,
- payment actions,
- resident communication,
- job-portal logins,
- GitHub writes.

A hosted deployment would need authentication, authorisation, tenant isolation, rate limiting, audit logging, secure secret storage and reviewed data-source allowlists.

## Decision controls

Reconciliation results are candidate suggestions only. Human review is mandatory before any accounting action. Career agent outputs are advisory; the candidate must verify all facts and submit applications themselves.

## Incident response

If a secret is ever committed:
1. Revoke or rotate it at the issuing provider immediately.
2. Remove it from the repository and consider the entire Git history exposed.
3. Review logs for misuse.
4. Do not rely on deleting the visible file as sufficient remediation.

Use GitHub secret scanning and push protection where available, plus dependency review and regular updates.
