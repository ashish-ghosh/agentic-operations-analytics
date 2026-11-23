from __future__ import annotations

import argparse
import json
from datetime import date

from ashish_ops_analytics.agent import analyse_job_file
from ashish_ops_analytics.cashflow import assess_receivables, daily_recovery_digest
from ashish_ops_analytics.collections import collection_summary
from ashish_ops_analytics.complaints import complaint_sla_summary
from ashish_ops_analytics.content_ideas import weekly_post_ideas
from ashish_ops_analytics.habits import daily_plan
from ashish_ops_analytics.io import load_csv
from ashish_ops_analytics.job_tracker import add_application, due_followups
from ashish_ops_analytics.quality import data_quality_report
from ashish_ops_analytics.reconciliation import suggest_matches


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ops-analytics",
        description="Ashish Operations Analytics toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("collections", help="Summarise maintenance collections")
    sub.add_parser("complaints", help="Summarise complaint SLA performance")
    cashflow_parser = sub.add_parser(
        "cashflow",
        help="Create the daily cash-recovery queue from synthetic or configured invoice data",
    )
    cashflow_parser.add_argument(
        "--as-of",
        default=date.today().isoformat(),
        help="Reporting date in YYYY-MM-DD format",
    )
    quality_parser = sub.add_parser("quality", help="Profile dataset quality")
    quality_parser.add_argument(
        "dataset",
        choices=[
            "maintenance_collections.csv",
            "complaints.csv",
            "cashflow_invoices.csv",
        ],
    )
    sub.add_parser("reconcile", help="Generate bank-to-ledger match suggestions")
    sub.add_parser("daily-plan", help="Print today's learning and job-search routine")
    sub.add_parser("job-followups", help="Show job applications needing follow-up")
    sub.add_parser("linkedin-ideas", help="Print human-reviewed LinkedIn post prompts")

    add_parser = sub.add_parser(
        "job-add",
        help="Log a manually submitted job application locally",
    )
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--source", default="manual")
    add_parser.add_argument("--url", default="")
    add_parser.add_argument("--followup", default="")
    add_parser.add_argument("--notes", default="")

    agent_parser = sub.add_parser(
        "analyse-job",
        help="Analyse a local job-description text file using an optional AI agent",
    )
    agent_parser.add_argument("--file", required=True)

    args = parser.parse_args()
    if args.command == "collections":
        result = collection_summary(load_csv("maintenance_collections.csv"))
    elif args.command == "complaints":
        result = complaint_sla_summary(load_csv("complaints.csv"))
    elif args.command == "cashflow":
        assessed = assess_receivables(
            load_csv("cashflow_invoices.csv"),
            as_of=date.fromisoformat(args.as_of),
        )
        result = daily_recovery_digest(assessed)
    elif args.command == "quality":
        result = data_quality_report(load_csv(args.dataset))
    elif args.command == "reconcile":
        result = suggest_matches(
            load_csv("bank_transactions.csv"),
            load_csv("ledger_entries.csv"),
        ).to_dict("records")
    elif args.command == "daily-plan":
        result = daily_plan(date.today())
    elif args.command == "job-followups":
        result = due_followups().to_dict("records")
    elif args.command == "linkedin-ideas":
        result = weekly_post_ideas()
    elif args.command == "job-add":
        path = add_application(
            args.company,
            args.role,
            args.source,
            args.url,
            next_followup_date=args.followup,
            notes=args.notes,
        )
        result = {"saved_locally_to": str(path), "committed_to_git": False}
    elif args.command == "analyse-job":
        result = {"analysis": analyse_job_file(args.file)}
    else:
        raise RuntimeError("Unknown command")

    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
