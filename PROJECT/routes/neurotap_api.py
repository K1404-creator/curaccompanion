import joblib
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Load NeuroTaps model
model = joblib.load('models/neurotap_model.pkl')
# If you used a scaler, load it too
# scaler = joblib.load('models/neurotap_scaler.pkl')

class NeuroTapInput(BaseModel):
    avg_key_latency: float
    error_rate: float
    backspace_rate: float
    typing_speed: float
    session_duration: float

@router.post("/predict_neurotap")
def predict_neurotap(input_data: NeuroTapInput):
    data = np.array([[ 
        input_data.avg_key_latency,
        input_data.error_rate,
        input_data.backspace_rate,
        input_data.typing_speed,
        input_data.session_duration
    ]])
    # If scaler was used:
    # data = scaler.transform(data)
    prediction = model.predict(data)[0]
    result = "High Fatigue" if prediction == 1 else "Low Fatigue"
    return {"Prediction": int(prediction), "result": result}