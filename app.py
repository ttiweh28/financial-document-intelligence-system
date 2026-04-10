import io

from agents import Runner
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from openai import AsyncOpenAI

import config
from main import orchestrator_agent, get_session
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(title="Financial AI assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}


@app.post("/process-document")
async def process_document(user_id: str = Form(...), file: UploadFile = File(...)):
    # Read bytes in the async handler; passing UploadFile.file (SpooledTemporaryFile)
    # into the sync OpenAI client often yields an empty or invalid multipart upload
    # because the stream position and multipart filename are wrong for httpx.
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file upload")

    if not config.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY is not configured",
        )

    client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    vector_store = await client.vector_stores.create(name=f"{user_id}_vector_store")

    upload_name = file.filename or "document"
    vs_file = await client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=(upload_name, io.BytesIO(raw)),
    )

    return {
        "message": f"File uploaded and processing started for user_id: {user_id}",
        "vector_store_id": vector_store.id,
        "vector_store_file_id": vs_file.id,
        "vector_store_file_status": vs_file.status,
        "filename": file.filename,
    }


@app.post("/follow_up")
async def follow_up(user_id: str, question: str):
    session = get_session(user_id)
    try:
        result = await Runner.run(orchestrator_agent, session=session, input=question)
    except InputGuardrailTripwireTriggered as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input was rejected by the financial-document guardrail.",
        ) from e
    except OutputGuardrailTripwireTriggered as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model output was rejected by the output guardrail.",
        ) from e
    return result.final_output


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)