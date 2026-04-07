from agents import Agent, Runner, trace
from config import MODEL


parser_agent = Agent(
    name="Document Parser Agent",
    model=MODEL,
    instructions="""
        Extract and clean text from the document.

        - Remove unnecessary formattings
        - Keep all financial information intact
        - Return plain readable text only

        Do NOT analyze or interpret.
"""
)