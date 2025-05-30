from crewai import Task
from agents.email_agent import email_agent

summarize_emails = Task(
    description="Summarize today's most important unread emails. Here's the list \n\n {emails_data}. If there are spam or ads don't analyze those, just say that there are X amount of spam/ads",
    agent=email_agent,
    expected_output="A short summary of the top 3-5 most important unread emails relevant to the user’s priorities. the rest of the emails can be a single line summary, just a few words to know what it is about.",
    async_execution=True,
    verbose=True
)