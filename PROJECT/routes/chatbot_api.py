
import json
import os
import random

import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

# Load intents.json once at startup
INTENTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "json file", "intents.json")
with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

def find_intent_response(user_message):
    user_message_lower = user_message.lower()
    for intent in intents:
        for pattern in intent.get("patterns", []):
            if pattern.lower() in user_message_lower or user_message_lower in pattern.lower():
                return random.choice(intent["responses"])
    # Check for default intent
    for intent in intents:
        if intent["tag"] == "default":
            return random.choice(intent["responses"])
    return None

class ChatRequest(BaseModel):
    message: str

@router.post("/ask")
async def ask_bot(request: ChatRequest):
    # 1. Try to match local intents
    local_response = find_intent_response(request.message)
    # If not default, return local response
    if local_response and "this website" not in local_response.lower():
        return {"response": local_response}
    # 2. Otherwise, call Gemini
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
