import os

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

app = FastAPI(title="Health Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chatbot/ask")
async def ask_bot(request: ChatRequest):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": request.message}]}
        ]
    }
    try:
        resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        result = resp.json()
        ai_response = (
            result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if result.get("candidates") else "No response from Gemini."
        )
        return {"response": ai_response}
    except Exception as e:
        return {"error": f"Error when calling Gemini: {str(e)}"}
