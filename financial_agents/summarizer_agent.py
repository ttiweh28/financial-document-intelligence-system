from agents import Agent, ModelSettings
from config import MODEL 

summarizer = Agent(

    name = "Summarizer Agent",
    model = MODEL,
    instructions="""
        You are a financial analyst.

        Generate a clear and concise summary of the financial document.

        Focus on:
        - total amounts
        - key transactions
        - overall financial trend or insight

        Output should be:
        - short (3–5 sentences)
        - easy to understand
        - business-focused (not technical)
    """,
    model_settings = ModelSettings(
    temperature=0.3,
    max_tokens=500,
    verbosity="medium"),

)