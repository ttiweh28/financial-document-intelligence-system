import asyncio
import os
import config

from agents import Agent, Runner, trace
from my_agents.parser_agent import parser_agent
from my_agents.entity_agent import entity_agent
from my_agents.computation_agent import computation_agent
from my_agents.anomaly_agent import anomaly_agent


from config import MODEL


#Agent-as-Tools

parser_tool = parser_agent.as_tool(
    tool_name="parse_document",
    tool_description="Clean and extract document text"
)

entity_tool = entity_agent.as_tool(
    tool_name="extract_entities",
    tool_description="Extract financial entities"
)

computation_tool = computation_agent.as_tool(
    tool_name="compute_metrics",
    tool_description="Compute totals and balances"
)

anomaly_tool = anomaly_agent.as_tool(
    tool_name="detect_anomalies",
    tool_description="Detect anomalies"
)


# Orchestrator Agent
orchestrator_agent = Agent(
    name="Financial Orchestrator Agent",
    model=MODEL,
    tools=[
        parser_tool,
        entity_tool,
        computation_tool,
        anomaly_tool,
    ],
    instructions="""
        You are a financial document orchestrator. Your job is to coordinate specialized agents and tools to fully analyze financial documents and deliver clear, accurate, and structured results.

        Always follow this pipeline in order:
        1. parse_document      - Parse and clean the raw document
        2. extract_entities    - Extract all financial entities from parsed content
        3. compute_metrics     - Run calculations and derive financial metrics
        4. detect_anomalies    - Identify irregularities, duplicates, or suspicious patterns
        5. validate_data       - Cross-check outputs from previous steps for consistency
        6. generate_summary    - Produce a structured summary of all findings
        7. explain_issues      - Clearly explain any anomalies or validation failures found

        RULES:
        - Always execute tools in the order listed above
        - Never skip a step, even if the previous step returns no results
        - Do NOT perform any task yourself — always delegate to the appropriate tool
        - Pass the output of each step as input to the next where relevant
        - If a tool fails or returns empty results, note it and continue the pipeline
        - Combine all outputs into a single, coherent final response
        """
)

# To-do: Write the pipeline to test the agent 