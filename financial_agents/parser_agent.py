from agents import Agent, Runner, trace
from config import MODEL
from tools.ocr_tool import ocr_tool 


parser_agent = Agent(
    name="Document Parser Agent",
    model=MODEL,
    tools=[ocr_tool],
    instructions="""
        Use the OCR tool to extract text from the document.

        Then:

        - Remove unnecessary formattings
        - Keep all financial information intact
        - Return plain readable text only

        Do NOT analyze or interpret.
"""
)