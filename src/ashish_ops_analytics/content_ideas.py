"""Evidence-led LinkedIn prompts. This module drafts ideas only; it never publishes."""
from __future__ import annotations

POST_IDEAS = [
    {
        "theme": "Collections analytics",
        "hook": "A maintenance collection report is more useful when it explains the recovery gap, not just the amount collected.",
        "evidence_to_add": "Use synthetic or approved anonymised figures; explain billed, collected, outstanding and recovery rate.",
    },
    {
        "theme": "Operations KPIs",
        "hook": "Complaint volume alone is not an operations-performance metric.",
        "evidence_to_add": "Show resolution time, SLA compliance, ageing and repeat-complaint rate.",
    },
    {
        "theme": "Data quality",
        "hook": "A dashboard is only as reliable as the data definitions behind it.",
        "evidence_to_add": "Describe missingness, duplicates, validation rules and reconciliation exceptions.",
    },
    {
        "theme": "Bank reconciliation",
        "hook": "Automated matching should explain why a transaction is a candidate, not silently mark it paid.",
        "evidence_to_add": "Demonstrate amount, reference and date evidence with a human-review queue.",
    },
    {
        "theme": "Career transition",
        "hook": "Facility operations taught me to translate service problems into measurable business questions.",
        "evidence_to_add": "Connect a real skill (vendor/SLA/collection operations) to a demonstrable SQL or Python analysis.",
    },
]


def weekly_post_ideas() -> list[dict]:
    """Return five prompts to adapt into original, human-reviewed posts."""
    return POST_IDEAS.copy()
