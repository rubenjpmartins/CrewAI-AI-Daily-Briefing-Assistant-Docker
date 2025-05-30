from crewai import Task
from agents.calendar_agent import calendar_agent

analyze_calendar = Task(
    name="analyze_calendar",
    description="Analyze today's calendar events from the list below:\n\n {calendar_data}. Events can be both in eglish or spanish.",
    agent=calendar_agent,
    expected_output="A list of today's events",
    async_execution=True,
    verbose=True
)