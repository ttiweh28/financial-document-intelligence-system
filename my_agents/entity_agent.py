from agents import Agent
from config import MODEL

entity_agent = Agent(
    name="Entity Extraction Agent",
    model=MODEL,
    instructions="""
        You are a financial entity extraction specialist. Your job is to analyze financial text and extract all relevant entities, including but not limited to:
        - amounts
        - dates
        - vendors
        - transactions
        Return structured JSON-like output.
"""
)