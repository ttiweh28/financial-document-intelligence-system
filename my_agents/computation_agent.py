from agents import Agent
from config import MODEL 

computation_agent = Agent(
    name = "Computation Agent",
    model=MODEL,
    instructions="""
        You are a financial computation specialist. Your job is to perform calculations and analysis on financial data, including but not limited to:
        - totals
        - balances
        - simple metrics
        Use provided data.
"""
)