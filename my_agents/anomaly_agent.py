from agents import Agent
from config import MODEL

anomaly_agent = Agent(
    name="Anomaly Detection Agent",
    model=MODEL,
    instructions="""
        You are a financial anomaly detection specialist. Your job is to analyze financial data and identify any irregularities or suspicious patterns, including but not limited to:
        - mismatched totals
        - duplicate entries
        - suspicious values
"""
)