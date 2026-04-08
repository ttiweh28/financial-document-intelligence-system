import asyncio
import os

from openai.types.graders.score_model_grader_param import Input
import config

from agents import Agent, Runner, trace,SQLiteSession
from financial_agents import explanation_agent, summarizer_agent
from financial_agents.parser_agent import parser_agent
from financial_agents.entity_agent import entity_agent
from financial_agents.computation_agent import computation_agent
from financial_agents.anomaly_agent import anomaly_agent
from financial_agents.explanation_agent import explanation_agent
from financial_agents.summarizer_agent import summarizer_agent


from config import MODEL
from guardrails import inputguardrail, outputguardrail


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
    tool_description="Detect anomalies in financial data"
)

explanation_tool = explanation_agent.as_tool(
    tool_name="explain_issues",
    tool_description="Explain anomalies and issues"
)
summarisation_tool = summarizer_agent.as_tool(
    tool_name="generate_summary",
    tool_description="Generate financial summary"
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
        explanation_tool,
        summarisation_tool
    ],
    input_guardrails=[inputguardrail],
    output_guardrails=[outputguardrail],
    instructions="""
        You are a financial document orchestrator. Your job is to coordinate specialized agents and tools to fully analyze financial documents and deliver clear, accurate, and structured results.

        Always follow this pipeline in order:
        1. parse_document      - Parse and clean the raw document
        2. extract_entities    - Extract all financial entities from parsed content
        3. compute_metrics     - Run calculations and derive financial metrics
        4. detect_anomalies    - Identify irregularities, duplicates, or suspicious patterns
        5. generate_summary    - Produce a structured summary of all findings
        6. explain_issues      - Clearly explain any anomalies or validation failures found

        RULES:
        - Always execute tools in the order listed above
        - Never skip a step, even if the previous step returns no results
        - Do NOT perform any task yourself — always delegate to the appropriate tool
        - Pass the output of each step as input to the next where relevant
        - If a tool fails or returns empty results, note it and continue the pipeline
        - Combine all outputs into a single, coherent final response

        """
)

#creating session to support followup questions on finanacial repport 
DB_PATH = "financial_sessions.db"

def get_session(user_id: str):
    """
    Create or retrieve session per user
    """
    return SQLiteSession(
        f"user_{user_id}",
        db_path=DB_PATH
    )


# pipeline 
async def process_document(user_id: str, file_path: str):

    session = get_session(user_id)

    with trace(f"Financial Workflow - User {user_id}"):

        result = await Runner.run(
            orchestrator_agent,
            f"Process this financial document: {file_path}",
            session=session
        )

        return result.final_output



# Support any followup questions
async def follow_up(user_id: str, question: str):

    session = get_session(user_id)

    with trace(f"Follow-up - User {user_id}"):

        result = await Runner.run(
            orchestrator_agent,
            question,
            session=session
        )

        return result.final_output
