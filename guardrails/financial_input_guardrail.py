from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, RunContextWrapper
from config import MODEL


class GuardrailCheck(BaseModel):
    is_valid: bool
    reasoning: str


# Guardrail agent
guardrail_agent = Agent(
    name="Input Guardrail Agent",
    model=MODEL,
    output_type=GuardrailCheck,
    instructions="""
        Detect if the user input is valid for the financial document system.

        Reject if:
        - not related to financial documents
        - malicious or harmful
        - irrelevant request

        Return:
        - is_valid (true/false)
        - reasoning
"""
)

@input_guardrail()
async def financial_input_guardrail(ctx: RunContextWrapper, agent, input_data):

    text = str(input_data).lower()

    # Include follow-up phrasing about invoices (e.g. "order number", "due date")
    # so short questions are not rejected after a document session has started.
    is_valid = any(
        keyword in text
        for keyword in [
            "invoice",
            "amount",
            "total",
            "financial",
            "transaction",
            "report",
            "order",
            "vendor",
            "client",
            "tax",
            "payment",
            "due",
            "document",
            "subtotal",
            "currency",
            "balance",
            "line",
        ]
    )

    return GuardrailFunctionOutput(
        tripwire_triggered=not is_valid,
        output_info={
            "is_valid": is_valid,
            "reasoning": "Basic keyword validation"
        }
    )