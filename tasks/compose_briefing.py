from crewai import Task
from agents.summary_agent import summary_agent

compose_briefing = Task(
    description="Compose a final daily briefing using the email and calendar summaries.",
    agent=summary_agent,
    expected_output="A polished, human-sounding daily briefing combining email and calendar insights, written in a friendly tone for a busy professional.",
    async_execution=False
)