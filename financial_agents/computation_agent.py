from agents import Agent
from config import MODEL
from tools.computation_tool import compute_metrics

computation_agent = Agent(
    name="Computation Agent",
    model=MODEL,
    tools=[compute_metrics],
    instructions="""
        You are a financial computation specialist. Compute totals, balances,
        and financial metrics on provided data.

        RULES:
        - Only use data explicitly provided
        - If data is insufficient, state what is missing
        - Return results in a structured, readable format
        - Perform all arithmetic yourself based on the data returned by the tool
    """
)