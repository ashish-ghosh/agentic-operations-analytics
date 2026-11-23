from datetime import date

from ashish_ops_analytics.habits import (
    daily_plan,
    habit_log_for_date,
    record_habit,
    weekly_habit_summary,
)


def test_daily_plan_has_four_timeboxed_habits():
    plan = daily_plan(date(2026, 11, 23))
    assert plan["total_minutes"] == 75
    assert len(plan["tasks"]) == 4
    assert len({task["habit_id"] for task in plan["tasks"]}) == 4


def test_habit_record_is_local_and_replaces_same_day_state(tmp_path):
    target = tmp_path / "habit_log.csv"
    day = date(2026, 11, 23)
    record_habit("sql", "Analytics", "Practise SQL", True, 25, on_date=day, path=target)
    record_habit("sql", "Analytics", "Practise SQL", False, 25, on_date=day, path=target)
    assert habit_log_for_date(day, path=target)["sql"] is False


def test_weekly_habit_summary_counts_distinct_completed_days(tmp_path):
    target = tmp_path / "habit_log.csv"
    for day in [date(2026, 11, 17), date(2026, 11, 19), date(2026, 11, 23)]:
        record_habit("sql", "Analytics", "Practise SQL", True, 25, on_date=day, path=target)
    summary = weekly_habit_summary(as_of=date(2026, 11, 23), path=target)
    assert summary.iloc[0]["completed_days"] == 3
    assert summary.iloc[0]["target_days"] == 7
    assert summary.iloc[0]["completion_pct"] == 42.9
