import joblib
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

model = joblib.load('models/heart.pkl')
# Add scaler if needed

class HeartInput(BaseModel):
    # Add the features your heart model expects
    age: int
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@router.post("/predict_heart")
def predict_heart(input_data: HeartInput):
    data = np.array([[
        input_data.age,
        input_data.sex,
        input_data.cp,
        input_data.trestbps,
        input_data.chol,
        input_data.fbs,
        input_data.restecg,
        input_data.thalach,
        input_data.exang,
        input_data.oldpeak,
        input_data.slope,
        input_data.ca,
        input_data.thal
    ]])
    prediction = model.predict(data)[0]
    result = "High Risk" if prediction == 1 else "Low Risk"
    return {"Prediction": int(prediction), "result": result}