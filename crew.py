from crewai import Crew, Task, LLM
from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent
from agents.summary_agent import summary_agent
from tasks.analyze_calendar import analyze_calendar
from tasks.compose_briefing import compose_briefing
from tasks.summarize_emails import summarize_emails
import os

# OpenRouter configuration using CrewAI LLM
model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter key stored as OPENAI_API_KEY
base_url = "https://openrouter.ai/api/v1"  # OpenRouter endpoint

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required (contains OpenRouter key)")

# CrewAI LLM configuration for OpenRouter
llm = LLM(
    model=f"openrouter/{model_name}",  # MODEL IDENTIFIER with openrouter/ prefix
    api_key=api_key,                   # STORED IN .env as OPENAI_API_KEY
    base_url=base_url                  # OPENROUTER ENDPOINT
)

crew = Crew(
    agents=[email_agent, calendar_agent, summary_agent],
    tasks=[analyze_calendar,
           summarize_emails,
           compose_briefing
        ],
    process="sequential",
    llm=llm,
    verbose=True
)