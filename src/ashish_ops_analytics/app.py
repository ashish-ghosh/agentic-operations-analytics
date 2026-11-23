from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ashish_ops_analytics.collections import collection_by_period, collection_summary
from ashish_ops_analytics.complaints import complaint_sla_summary
from ashish_ops_analytics.io import load_csv
from ashish_ops_analytics.quality import data_quality_report
from ashish_ops_analytics.reconciliation import suggest_matches

st.set_page_config(page_title="Operations Analytics | Ashish Ghosh", page_icon="📊", layout="wide")
st.title("Operations Analytics")
st.caption("Portfolio demonstration by Ashish Ghosh • Synthetic sample data • Human-reviewed decisions only")

page = st.sidebar.selectbox(
    "Choose a module",
    ["Maintenance collections", "Complaint SLA", "Data quality", "Bank reconciliation"],
)

try:
    if page == "Maintenance collections":
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
            st.plotly_chart(px.bar(trend, x="month", y=["amount_due", "amount_collected"],
                                   barmode="group", title="Billed vs collected"), use_container_width=True)
        st.dataframe(df, use_container_width=True)
    elif page == "Complaint SLA":
        sample = load_csv("complaints.csv")
        upload = st.file_uploader("Optional: upload a complaints CSV", type=["csv"])
        df = pd.read_csv(upload) if upload else sample
        metrics = complaint_sla_summary(df)
        cols = st.columns(4)
        cols[0].metric("Tickets", metrics["total_tickets"])
        cols[1].metric("Open", metrics["open_tickets"])
        cols[2].metric("SLA breaches", metrics["sla_breaches_including_open"])
        cols[3].metric("Resolved on time", f"{metrics['resolved_sla_compliance_pct']:.1f}%")
        st.dataframe(df, use_container_width=True)
    elif page == "Data quality":
        dataset = st.selectbox("Sample dataset", ["maintenance_collections.csv", "complaints.csv"])
        df = load_csv(dataset)
        report = data_quality_report(df)
        st.json(report)
        st.dataframe(df, use_container_width=True)
    else:
        bank = load_csv("bank_transactions.csv")
        ledger = load_csv("ledger_entries.csv")
        result = suggest_matches(bank, ledger)
        st.info("Suggestions only. Review evidence and approve matches in your own accounting workflow.")
        st.dataframe(result, use_container_width=True)
except (ValueError, FileNotFoundError) as exc:
    st.error(str(exc))
