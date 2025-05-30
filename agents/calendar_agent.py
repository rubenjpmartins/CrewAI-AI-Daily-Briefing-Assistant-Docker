from crewai import Agent, LLM
import os

# OpenRouter configuration using CrewAI LLM
model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter key stored as OPENAI_API_KEY
base_url = "https://openrouter.ai/api/v1"  # OpenRouter endpoint

if api_key:
    llm = LLM(
        model=f"openrouter/{model_name}",  # MODEL IDENTIFIER with openrouter/ prefix
        api_key=api_key,                   # STORED IN .env as OPENAI_API_KEY
        base_url=base_url                  # OPENROUTER ENDPOINT
    )
else:
    llm = None

calendar_agent = Agent(
    role="Calendar Analyzer",
    goal="""
        List all events scheduled for today. Recognize if there are any overlaps, or free time gaps. 
    """,
    backstory="""
        You are a calendar assistant. You receive a list of calendar events for today.

        Your job is to:
        - List every event scheduled for TODAY
        - Preserve the title and time as written
        - Optionally rephrase for readability, but NEVER remove or invent content
        - Do not make events, descriptions or times up
        - You speak and understand both english and spanish
    """,
    allow_delegation=False,
    verbose=True,
    llm=llm
)