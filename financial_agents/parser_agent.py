from agents import Agent, FileSearchTool
from config import MODEL

parser_agent = Agent(
    name="Document Parser Agent",
    model=MODEL,
    tools=[
        FileSearchTool(
            vector_store_ids=["vs_69d9174f3bb881918f9c22bb9202af7f"],
            max_num_results=20
        )
    ],
    instructions="""
        You are responsible for extracting text from financial documents.
        Use the file_search tool to retrieve all relevant content.
        Return the full extracted text cleanly formatted.
        Do NOT analyze — only extract and clean.
    """
)