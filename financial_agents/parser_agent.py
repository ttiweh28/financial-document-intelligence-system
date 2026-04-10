from agents import Agent, FileSearchTool
from config import MODEL
from dotenv import load_dotenv
import os

load_dotenv()

vector_store_id = os.getenv("VECTOR_STORE_ID")

parser_agent = Agent(
    name="Document Parser Agent",
    model=MODEL,
    tools=[
        FileSearchTool(
            vector_store_ids=[vector_store_id],
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