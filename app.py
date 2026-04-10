from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from openai import OpenAI

from main import orchestrator_agent, get_session
from agents import Runner, trace



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
    
    client = OpenAI()

    vector_store = client.vector_stores.create(
        name=f"{user_id}_vector_store",
    )

    client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=file.file,
    )

    return {
        "message": f"File uploaded and processing started for user_id: {user_id}",
        "vector_store_id": vector_store.id,
        "filename": file.filename,
    }


@app.post("/follow-up")
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
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)