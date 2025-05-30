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

email_agent = Agent(
    role="Email Summarizer",
    goal="Summarize only useful, actionable, and non-promotional unread emails from today.",
    backstory="""
        You are a strict assistant tasked with identifying relevant emails only.
        If the input data includes promotional, marketing, or unrelated content, discard it.
        You must only summarize emails that are work-related, personal, or include meeting, invoice, or project keywords.
        If nothing relevant exists, say: 'No important emails found today.'
        Never invent emails or fabricate content that wasn't clearly in the input.
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)