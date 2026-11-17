import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="AI Study Assistant API")

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Student study question")

class AnswerResponse(BaseModel):
    question: str
    answer: str

def generate_llm_answer(question: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in environment variables.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"You are a helpful AI study assistant. Answer clearly:\n{question}"
    )
    return response.text

@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty or whitespace.")
    try:
        answer = generate_llm_answer(payload.question)
        return AnswerResponse(question=payload.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
