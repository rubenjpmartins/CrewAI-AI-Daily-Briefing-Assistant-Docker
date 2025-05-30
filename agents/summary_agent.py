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

summary_agent = Agent(
    role="Daily Briefing Composer",
    goal="Write a daily briefing only from what the other agents found — do not make anything up.",
    backstory="""You are an executive assistant writing a summary based only on inputs.
            If the input says no useful calendar events or emails were found, your summary should reflect that honestly.
            Never add tasks, meetings, tips, or emails that aren't present.""",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

