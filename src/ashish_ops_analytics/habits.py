from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from ashish_ops_analytics.io import local_job_tracker_path

HABIT_COLUMNS = [
    "date",
    "habit_id",
    "area",
    "task",
    "completed",
    "minutes",
]


def daily_plan(day: date | None = None) -> dict:
    """Create a repeatable 60–75 minute career-transition routine."""
    current = day or date.today()
    tasks = [
        {
            "habit_id": "sql_python_practice",
            "minutes": 25,
            "area": "Core analytics",
            "task": "Practise SQL or Python using one measurable exercise.",
        },
        {
            "habit_id": "portfolio_build",
            "minutes": 25,
            "area": "Portfolio",
            "task": "Build, test or document one small improvement in a portfolio project.",
        },
        {
            "habit_id": "job_pipeline",
            "minutes": 15,
            "area": "Career pipeline",
            "task": "Review one relevant vacancy and log a tailored application or follow-up.",
        },
        {
            "habit_id": "professional_presence",
            "minutes": 10,
            "area": "Professional presence",
            "task": "Write one evidence-led LinkedIn note or record a project learning.",
        },
    ]
    if current.weekday() >= 5:
        tasks[1]["task"] = "Complete a portfolio milestone, dashboard, case study or code review."
        tasks[2]["task"] = "Review weekly applications, interview gaps and next week's target roles."
        tasks[3]["task"] = "Prepare one LinkedIn draft; publish only after personal review."
    return {
        "date": current.isoformat(),
        "total_minutes": sum(item["minutes"] for item in tasks),
        "tasks": tasks,
        "weekly_scorecard": [
            "5 SQL/Python practice sessions",
            "1 portfolio improvement with tests or documentation",
            "5 carefully matched job applications (quality over volume)",
            "2 LinkedIn drafts or one reviewed post",
            "1 weekly review of skills, applications and product opportunities",
        ],
    }


def local_habit_log_path() -> Path:
    """Return the local-only habit log path; it must never be committed."""
    return local_job_tracker_path().parent / "habit_log.csv"


def habit_log_path(path: Path | None = None) -> Path:
    """Resolve an explicit path for tests or the default local habit log."""
    return path or local_habit_log_path()


def habit_log_for_date(
    on_date: date | None = None,
    path: Path | None = None,
) -> dict[str, bool]:
    """Return the most recently recorded completion state for each habit on a date."""
    target = habit_log_path(path)
    if not target.exists():
        return {}
    df = pd.read_csv(target).reindex(columns=HABIT_COLUMNS)
    if df.empty:
        return {}
    day = (on_date or date.today()).isoformat()
    today_rows = df.loc[df["date"].astype(str) == day]
    if today_rows.empty:
        return {}
    latest = today_rows.drop_duplicates("habit_id", keep="last")
    return {
        str(row["habit_id"]): str(row["completed"]).strip().lower() in {"true", "1", "yes"}
        for _, row in latest.iterrows()
    }


def record_habit(
    habit_id: str,
    area: str,
    task: str,
    completed: bool,
    minutes: int,
    on_date: date | None = None,
    path: Path | None = None,
) -> Path:
    """Save one daily habit state locally, replacing any earlier state for the same day/id."""
    if not habit_id.strip() or not area.strip() or not task.strip():
        raise ValueError("Habit ID, area and task are required")
    if minutes < 0:
        raise ValueError("Minutes cannot be negative")

    target = habit_log_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = (
        pd.read_csv(target).reindex(columns=HABIT_COLUMNS)
        if target.exists()
        else pd.DataFrame(columns=HABIT_COLUMNS)
    )
    day = (on_date or date.today()).isoformat()
    if not existing.empty:
        keep = ~(
            (existing["date"].astype(str) == day)
            & (existing["habit_id"].astype(str) == habit_id)
        )
        existing = existing.loc[keep]

    row = pd.DataFrame([{
        "date": day,
        "habit_id": habit_id,
        "area": area,
        "task": task,
        "completed": bool(completed),
        "minutes": int(minutes),
    }])
    pd.concat([existing, row], ignore_index=True).to_csv(target, index=False)
    return target


def weekly_habit_summary(
    as_of: date | None = None,
    path: Path | None = None,
) -> pd.DataFrame:
    """Summarise completed habit days across the trailing seven-day window."""
    target = habit_log_path(path)
    if not target.exists():
        return pd.DataFrame(
            columns=["habit_id", "area", "task", "completed_days", "target_days", "completion_pct"]
        )

    df = pd.read_csv(target).reindex(columns=HABIT_COLUMNS)
    if df.empty:
        return pd.DataFrame(
            columns=["habit_id", "area", "task", "completed_days", "target_days", "completion_pct"]
        )

    end_day = as_of or date.today()
    start_day = end_day - timedelta(days=6)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["completed"] = df["completed"].astype(str).str.strip().str.lower().isin(
        {"true", "1", "yes"}
    )
    window = df.loc[df["date"].between(start_day, end_day)]
    latest = window.sort_values("date").drop_duplicates(["date", "habit_id"], keep="last")
    if latest.empty:
        return pd.DataFrame(
            columns=["habit_id", "area", "task", "completed_days", "target_days", "completion_pct"]
        )

    summary = (
        latest.groupby(["habit_id", "area", "task"], as_index=False)["completed"]
        .sum()
        .rename(columns={"completed": "completed_days"})
    )
    summary["target_days"] = 7
    summary["completion_pct"] = (summary["completed_days"] / 7 * 100).round(1)
    return summary.sort_values(["completion_pct", "area"], ascending=[False, True])
