from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

PROFILE = {
    "name": "Ashish Ghosh",
    "education": [
        "MSc Business Analytics, FOM University of Applied Sciences, Essen, Germany",
        "B.Tech Computer Science",
    ],
    "skills": [
        "Python", "SQL", "Tableau", "Power BI", "Excel", "Business Analytics",
        "Facility Operations", "Vendor Management", "Maintenance Recovery",
        "Complaint and SLA Management", "Operational Reporting",
    ],
    "portfolio_url": "https://github.com/ashish-ghosh/agentic-operations-analytics",
}


def candidate_profile_json() -> str:
    """Return a transparent candidate profile used by the optional job-description agent."""
    return json.dumps(PROFILE, indent=2)


async def analyse_job_description(job_description: str) -> str:
    """Use the OpenAI Agents SDK to analyse a job description; no applications are submitted."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY locally before running the optional AI agent.")

    from agents import Agent, Runner
    from agents.decorators import tool

    @tool
    def get_candidate_profile() -> str:
        """Return the candidate's declared education, skills and portfolio URL."""
        return candidate_profile_json()

    agent = Agent(
        name="Ashish Career Match Analyst",
        instructions=(
            "You help a candidate evaluate analyst and BI job descriptions. Use the profile tool. "
            "Return: role fit, supported matching evidence, missing skills, five interview topics, "
            "and resume keywords that are genuinely supported. Do not invent experience, metrics, "
            "certifications or tools. Clearly label any gap. Never apply for jobs, log in to portals, "
            "send messages or publish content."
        ),
        tools=[get_candidate_profile],
    )
    result = await Runner.run(agent, input=job_description)
    return str(result.final_output)


def analyse_job_file(path: str | Path) -> str:
    """Read a user-supplied job description text file and analyse it with the optional agent."""
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("The job-description file is empty")
    return asyncio.run(analyse_job_description(text))
