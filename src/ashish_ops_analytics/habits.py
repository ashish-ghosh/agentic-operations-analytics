from __future__ import annotations

from datetime import date


def daily_plan(day: date | None = None) -> dict:
    """Create a repeatable 60–75 minute career-transition routine."""
    current = day or date.today()
    tasks = [
        {"minutes": 25, "area": "Core analytics", "task": "Practise SQL or Python using one measurable exercise."},
        {"minutes": 25, "area": "Portfolio", "task": "Build, test or document one small improvement in a portfolio project."},
        {"minutes": 15, "area": "Career pipeline", "task": "Review one relevant vacancy and log a tailored application or follow-up."},
        {"minutes": 10, "area": "Professional presence", "task": "Write one evidence-led LinkedIn note or record a project learning."},
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
