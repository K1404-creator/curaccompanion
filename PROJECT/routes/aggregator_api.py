from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
import threading

router = APIRouter()

STORE: Dict[str, Dict] = {}
LOCK = threading.Lock()

class PredEvent(BaseModel):
    user_id: Optional[str] = "anonymous"
    feature: str  # "diabetes" | "heart" | "neurotap"
    prediction: int  # 0 or 1

@router.post("/event")
async def add_event(evt: PredEvent):
    user = evt.user_id
    with LOCK:
        STORE.setdefault(user, {})
        STORE[user][evt.feature] = evt.prediction
    
    score = compute_avg_score(STORE[user])
    return {"health_score": score, "predictions": STORE[user]}

def compute_avg_score(user_preds: Dict[str, int]) -> int:
    if not user_preds:
        return 100
    scores = []
    for feature, pred in user_preds.items():
        scores.append(100 if pred == 0 else 50)
    return int(sum(scores) / len(scores))

@router.get("/score/{user_id}")
async def get_score(user_id: str):
    preds = STORE.get(user_id, {})
    return {"health_score": compute_avg_score(preds), "predictions": preds}