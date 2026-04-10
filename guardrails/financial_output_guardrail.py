from pydantic import BaseModel
from agents import Agent, Runner, output_guardrail, GuardrailFunctionOutput, RunContextWrapper
from config import MODEL


class GuardrailCheck(BaseModel):
    is_valid: bool
    reasoning: str


guardrail_agent = Agent(
    name="Output Guardrail Agent",
    model=MODEL,
    output_type=GuardrailCheck,
    instructions="""
        Validate the system output.

        Reject if:
        - contains incorrect financial claims
        - hallucinated values
        - misleading conclusions

        Return:
        - is_valid (true/false)
        - reasoning
    """
)


@output_guardrail()
async def financial_output_guardrail(ctx: RunContextWrapper, agent, output_data):

    # Serialize output to string before passing to guardrail agent
    if hasattr(output_data, "model_dump_json"):
        output_str = output_data.model_dump_json(indent=2)
    else:
        output_str = str(output_data)

    result = await Runner.run(guardrail_agent, output_str)
    output = result.final_output_as(GuardrailCheck)

    return GuardrailFunctionOutput(
        tripwire_triggered=not output.is_valid,
        output_info=output
    )