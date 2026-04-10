from agents import Agent, Runner, trace
from config import MODEL
from tools.ocr_tool import ocr_tool 


parser_agent = Agent(
    name="Document Parser Agent",
    model=MODEL,
    tools=[ocr_tool],
    instructions="""
       You are responsible for extracting text from documents.

            IMPORTANT:
            - Always call the OCR tool with the provided file_path
            - Do NOT try to interpret the file path yourself

            Input will be:
            {
            "file_path": "path_to_file"
            }

            You must call:
            ocr_extract_text(file_path=...)

            Then:
            - clean the text
            - return readable output

            Do NOT analyze.
"""
)