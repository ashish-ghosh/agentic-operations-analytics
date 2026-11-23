from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from ashish_ops_analytics.cashflow import (
    assess_receivables,
    build_followup_email,
    daily_recovery_digest,
)
from ashish_ops_analytics.collections import collection_by_period, collection_summary
from ashish_ops_analytics.complaints import complaint_sla_summary
from ashish_ops_analytics.content_ideas import weekly_post_ideas
from ashish_ops_analytics.habits import (
    daily_plan,
    habit_log_for_date,
    record_habit,
    weekly_habit_summary,
)
from ashish_ops_analytics.io import load_csv, local_job_tracker_path
from ashish_ops_analytics.job_tracker import add_application, due_followups
from ashish_ops_analytics.quality import data_quality_report
from ashish_ops_analytics.reconciliation import suggest_matches

st.set_page_config(page_title="Operations Analytics | Ashish Ghosh", page_icon="📊", layout="wide")
st.title("Operations Analytics")
st.caption("Portfolio demonstration by Ashish Ghosh • Synthetic operations data • Human-reviewed decisions only")

page = st.sidebar.selectbox(
    "Choose a module",
    [
        "CashPilot — Cashflow Recovery",
        "Maintenance collections",
        "Complaint SLA",
        "Data quality",
        "Bank reconciliation",
        "Career & Learning",
    ],
)

try:
    if page == "CashPilot — Cashflow Recovery":
        st.header("CashPilot — Daily Collections Work Queue")
        st.caption(
            "Synthetic demonstration data. Scores prioritise work; they do not predict "
            "payment probability. Email output is draft-only."
        )
        sample = load_csv("cashflow_invoices.csv")
        upload = st.file_uploader("Optional: upload an invoice CSV using the sample column structure", type=["csv"])
        invoice_df = pd.read_csv(upload) if upload else sample
        as_of = st.date_input("Report date", value=date.today())
        assessed = assess_receivables(invoice_df, as_of=as_of)
        digest = daily_recovery_digest(assessed)

        columns = st.columns(4)
        columns[0].metric("Outstanding", f"₹{digest['total_outstanding']:,.0f}")
        columns[1].metric("Overdue balance", f"₹{digest['overdue_outstanding']:,.0f}")
        columns[2].metric("Overdue invoices", digest["overdue_invoice_count"])
        columns[3].metric("Missing-document blockers", digest["missing_document_count"])

        st.subheader("Priority action queue")
        st.dataframe(
            assessed[
                [
                    "invoice_id", "customer_name", "site", "amount_outstanding",
                    "days_overdue", "age_bucket", "priority_score", "next_action",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Blocker summary")
        blocker_cols = st.columns(2)
        blocker_cols[0].metric("Disputed invoices", digest["disputed_invoice_count"])
        blocker_cols[1].metric("Missed payment promises", digest["missed_promise_count"])

        st.subheader("Human-reviewed follow-up drafts")
        open_items = assessed.loc[assessed["amount_outstanding"] > 0]
        if open_items.empty:
            st.success("No open receivables in this dataset.")
        else:
            selected_invoice = st.selectbox(
                "Choose an invoice",
                open_items["invoice_id"].astype(str).tolist(),
            )
            selected_row = open_items.loc[
                open_items["invoice_id"].astype(str) == selected_invoice
            ].iloc[0]
            draft = build_followup_email(selected_row)
            st.text_input("Email subject", value=draft["subject"])
            st.text_area("Draft body — not sent", value=draft["body"], height=220)
            st.warning("This dashboard does not send emails or update accounting records.")

        st.download_button(
            "Download daily action queue",
            assessed.to_csv(index=False).encode("utf-8"),
            file_name="cashpilot_daily_action_queue.csv",
            mime="text/csv",
        )

    elif page == "Maintenance collections":
        sample = load_csv("maintenance_collections.csv")
        upload = st.file_uploader("Optional: upload a CSV with month, society, units, amount_due, amount_collected", type=["csv"])
        df = pd.read_csv(upload) if upload else sample
        kpis = collection_summary(df)
        columns = st.columns(4)
        columns[0].metric("Total billed", f"₹{kpis['total_due']:,.0f}")
        columns[1].metric("Collected", f"₹{kpis['total_collected']:,.0f}")
        columns[2].metric("Outstanding", f"₹{kpis['outstanding']:,.0f}")
        columns[3].metric("Recovery rate", f"{kpis['recovery_pct']:.1f}%")
        if "month" in df.columns:
            trend = collection_by_period(df)
            st.plotly_chart(
                px.bar(
                    trend, x="month", y=["amount_due", "amount_collected"],
                    barmode="group", title="Billed vs collected",
                ),
                use_container_width=True,
            )
        st.dataframe(df, use_container_width=True)

    elif page == "Complaint SLA":
        sample = load_csv("complaints.csv")
        upload = st.file_uploader("Optional: upload a complaints CSV", type=["csv"])
        df = pd.read_csv(upload) if upload else sample
        metrics = complaint_sla_summary(df)
        columns = st.columns(4)
        columns[0].metric("Tickets", metrics["total_tickets"])
        columns[1].metric("Open", metrics["open_tickets"])
        columns[2].metric("SLA breaches", metrics["sla_breaches_including_open"])
        columns[3].metric(
            "Resolved on time",
            f"{metrics['resolved_sla_compliance_pct']:.1f}%",
        )
        st.dataframe(df, use_container_width=True)

    elif page == "Data quality":
        dataset = st.selectbox(
            "Sample dataset",
            ["maintenance_collections.csv", "complaints.csv", "cashflow_invoices.csv"],
        )
        df = load_csv(dataset)
        report = data_quality_report(df)
        st.json(report)
        st.dataframe(df, use_container_width=True)

    elif page == "Bank reconciliation":
        bank = load_csv("bank_transactions.csv")
        ledger = load_csv("ledger_entries.csv")
        result = suggest_matches(bank, ledger)
        st.info("Suggestions only. Review evidence and approve matches in your own accounting workflow.")
        st.dataframe(result, use_container_width=True)

    else:
        st.header("Career & Learning Hub")
        st.caption(
            "Local-only personal tracker. Job applications and habit records are saved on this "
            "computer and excluded from Git."
        )

        plan = daily_plan(date.today())
        completed_today = habit_log_for_date()
        weekly = weekly_habit_summary()
        completed_total = int(weekly["completed_days"].sum()) if not weekly.empty else 0
        target_total = int(weekly["target_days"].sum()) if not weekly.empty else 0

        columns = st.columns(3)
        columns[0].metric("Today's learning plan", f"{plan['total_minutes']} min")
        columns[1].metric("Completed habit days (7-day window)", completed_total)
        columns[2].metric(
            "Habit completion",
            f"{(completed_total / target_total * 100) if target_total else 0:.0f}%",
        )

        st.subheader("Today's 75-minute routine")
        with st.form("daily-habits"):
            habit_states = {}
            for item in plan["tasks"]:
                label = f"{item['area']} · {item['minutes']} min — {item['task']}"
                habit_states[item["habit_id"]] = st.checkbox(
                    label,
                    value=completed_today.get(item["habit_id"], False),
                    key=f"habit-{date.today().isoformat()}-{item['habit_id']}",
                )
            saved = st.form_submit_button("Save today's habit record")
        if saved:
            for item in plan["tasks"]:
                record_habit(
                    habit_id=item["habit_id"],
                    area=item["area"],
                    task=item["task"],
                    completed=habit_states[item["habit_id"]],
                    minutes=item["minutes"],
                )
            st.success("Today's learning and career routine has been saved locally.")

        if not weekly.empty:
            st.subheader("Last seven days")
            weekly_display = weekly.rename(
                columns={
                    "habit_id": "Habit", "area": "Area", "task": "Activity",
                    "completed_days": "Completed days", "target_days": "Target days",
                    "completion_pct": "Completion %",
                }
            )
            st.dataframe(weekly_display, use_container_width=True, hide_index=True)
        else:
            st.info("Your weekly habit scorecard will appear after you save your first day.")

        st.divider()
        st.subheader("Job application tracker")
        with st.form("add-job-application"):
            company = st.text_input("Company")
            role = st.text_input("Role")
            source = st.selectbox("Source", ["LinkedIn", "Naukri", "Employer website", "Referral", "Other"])
            job_url = st.text_input("Job URL")
            followup = st.date_input("Next follow-up date", value=date.today())
            notes = st.text_area("Notes / skill gaps")
            submitted = st.form_submit_button("Save application locally")
        if submitted:
            if not company.strip() or not role.strip():
                st.error("Enter both company and role.")
            else:
                saved_path = add_application(
                    company=company, role=role, source=source, job_url=job_url,
                    next_followup_date=followup.isoformat(), notes=notes,
                )
                st.success(f"Application saved locally to {saved_path.name}.")

        st.subheader("Follow-ups due")
        followups = due_followups()
        if followups.empty:
            st.caption("No follow-ups are currently due.")
        else:
            st.dataframe(followups, use_container_width=True, hide_index=True)

        st.subheader("Recent applications")
        tracker_path = local_job_tracker_path()
        if tracker_path.exists():
            applications = pd.read_csv(tracker_path)
            st.dataframe(applications.tail(20), use_container_width=True, hide_index=True)
        else:
            st.caption("Your private application tracker will appear here after the first entry.")

        st.divider()
        st.subheader("LinkedIn learning-to-content prompts")
        st.caption("These are draft prompts only. Add verified examples and review before publishing.")
        for item in weekly_post_ideas():
            with st.expander(item["theme"]):
                st.write(item["hook"])
                st.caption(f"Evidence to add: {item['evidence_to_add']}")

except (ValueError, FileNotFoundError) as exc:
    st.error(str(exc))
