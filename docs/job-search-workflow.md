# Job-search workflow: LinkedIn and Naukri

## Purpose

Use this repository to make the job search measurable and tailored. The workflow is designed for manual, user-controlled applications.

## Target roles

1. Data Analyst
2. Business Intelligence Analyst
3. Operations Data Analyst
4. MIS / BI Analyst
5. Business Analyst
6. Junior Analytics Engineer (after data-modelling practice)

## Evidence to prepare

- SQL: joins, CTEs, window functions, aggregation, date/time analysis and query explanation.
- Python: pandas, data cleaning, validation, EDA and simple automation.
- BI: Power BI data modelling, DAX, Power Query, dashboard design and KPI definitions.
- Business: requirements gathering, stakeholder communication, root-cause analysis and recommendations.
- Domain: maintenance collection, vendor performance, complaint/SLA and operational reporting.

## Manual application loop

1. Find a vacancy on LinkedIn, Naukri or the employer's own careers page.
2. Read the complete job description and confirm location, seniority, salary range and work authorisation requirements.
3. Save the URL and job description locally.
4. Run `ops-analytics analyse-job --file job-description.txt` if the optional API-backed agent is configured.
5. Verify every suggested match against genuine experience. Remove unsupported keywords.
6. Tailor the resume and cover note.
7. Submit the application yourself on the official portal.
8. Log the application and next follow-up date using `ops-analytics job-add`.
9. Review due follow-ups using `ops-analytics job-followups`.

## Example

```bash
ops-analytics job-add --company "Example Employer" --role "Data Analyst" --source "Naukri" --url "https://example.com/job" --followup "2026-12-01"
ops-analytics job-followups
```

The real tracker file is written locally to `data/job_applications.csv`, which is ignored by Git.

## LinkedIn professional content

Use the content prompts as starting points, then add a real lesson, reproducible chart or carefully anonymised example. Never publish employer-confidential information, resident details or fabricated performance metrics. The helper does not post to LinkedIn.

## Important boundaries

- Do not scrape LinkedIn or Naukri pages.
- Do not store portal passwords, cookies, session tokens or OTPs.
- Do not automate submissions or messages.
- Use official platform features or authorised APIs where available.
- Review every resume, message and post before sending or publishing.
