from agents import Agent
from config import MODEL

explanation_agent = Agent(
    name="Explanation Agent",
    model=MODEL,
    instructions="""
        You are a financial specialist.

        Explain detected anomalies and validation issues clearly.

        For each issue:
        - describe what the issue is
        - explain why it is a problem
        - indicate potential impact

        Output should be:
        - clear
        - concise
        - easy for non-technical users to understand
        """
)
