import asyncio
import os

import config

from agents import Agent, Runner, trace, SQLiteSession
from financial_agents.parser_agent import parser_agent
from financial_agents.entity_agent import entity_agent
from financial_agents.computation_agent import computation_agent
from financial_agents.anomaly_agent import anomaly_agent
from financial_agents.explanation_agent import explanation_agent
from financial_agents.summarizer_agent import summarizer_agent
from config import MODEL
from guardrails.financial_input_guardrail import financial_input_guardrail
from guardrails.financial_output_guardrail import financial_output_guardrail
from models.output_schema import FinalReport


# Agent-as-Tools
parser_tool = parser_agent.as_tool(
    tool_name="parse_document",
    tool_description="Retrieve and clean document content from vector store"
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
    tool_name="explain_document",
    tool_description=(
    "Use this tool when the user asks to understand, summarize, or analyze a financial document, "
    "including explaining its contents or identifying and explaining anomalies."
)
)

summarisation_tool = summarizer_agent.as_tool(
    tool_name="generate_summary",
    tool_description="Generate financial summary"
)


orchestrator_agent = Agent(
    name="Financial Orchestrator Agent",
    model=MODEL,
    output_type=FinalReport,
    tools=[
        parser_tool,
        entity_tool,
        computation_tool,
        anomaly_tool,
        explanation_tool,
        summarisation_tool
    ],
    input_guardrails=[financial_input_guardrail],
    output_guardrails=[financial_output_guardrail],
    instructions="""
        You are a financial document orchestrator.

        Always follow this pipeline in order:
        1. parse_document      - Retrieve and clean document content from vector store
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
        - Return your final output as a structured JSON object matching the FinalReport schema
    """
)



# Session management
DB_PATH = "financial_sessions.db"

def get_session(user_id: str):
    """Create or retrieve session per user."""
    return SQLiteSession(
        f"user_{user_id}",
        db_path=DB_PATH
    )


# Main pipeline
async def process_document(user_id: str, *, persistent_session: bool = True):
    # When persistent_session is False, each run has no prior turns. Otherwise the
    # model may follow stale SQLiteSession history (e.g. an old "parse failed"
    # narrative) even though the vector store and tools are configured correctly.
    session = get_session(user_id) if persistent_session else None

    with trace(f"Financial Workflow - User {user_id}"):
        result = await Runner.run(
            orchestrator_agent,
            "Process the uploaded financial document and extract all data.",
            session=session,
        )

    return result.final_output


# Follow-up questions
async def follow_up(user_id: str, question: str):
    session = get_session(user_id)

    with trace(f"Follow-up - User {user_id}"):
        result = await Runner.run(
            orchestrator_agent,
            question,
            session=session
        )

    return result.final_output


if __name__ == "__main__":
    user_id = "test_user"

    # One-shot CLI: do not reuse SQLite history, or repeated runs can echo old failures.
    result = asyncio.run(process_document(user_id, persistent_session=False))

    print("\n========== FINANCIAL DOCUMENT REPORT ==========\n")
    print(f"📄 Document Type     : {result.parsed_document.document_type}")
    print(f"🏢 Vendor            : {result.entities.vendor}")
    print(f"👤 Client            : {result.entities.client}")
    print(f"🧾 Invoice #         : {result.entities.invoice_number}")
    print(f"📅 Invoice Date      : {result.entities.invoice_date}")
    print(f"📅 Due Date          : {result.entities.due_date}")
    print(f"💱 Currency          : {result.entities.currency}")
    print()
    print("── Line Items ──────────────────────────────────")
    for item in result.entities.line_items:
        print(f"   • {item}")
    print()
    print("── Financial Report ──────────────────────────────────")
    print(f"   Subtotal          : ${result.metrics.subtotal}")
    print(f"   Tax ({result.metrics.tax_rate}%)        : ${result.metrics.tax}")
    print(f"   Total             : ${result.metrics.total}")
    print(f"   Balanced          : {'✅' if result.metrics.is_balanced else '❌'}")
    print()
    print("── Anomalies ───────────────────────────────────")
    if result.anomalies.anomalies_found:
        for a in result.anomalies.anomalies:
            print(f"   ⚠️  {a}")
    else:
        print("   ✅ No anomalies detected")
    print()
    print("── Summary ─────────────────────────────────────")
    print(f"   {result.summary}")
    print()
    print("── Explanation ─────────────────────────────────")
    print(f"   {result.explanation}")
    print("\n================================================\n")