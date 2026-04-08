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

    result = await Runner.run(guardrail_agent, input_data)
    output = result.final_output_as(GuardrailCheck)

    return GuardrailFunctionOutput(
        tripwire_triggered=not output.is_valid,
        output_info=output
    )