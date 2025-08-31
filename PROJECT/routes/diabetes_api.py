import joblib
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Load model and scaler
model = joblib.load('models/diabetes_model.pkl')
scaler = joblib.load('models/scaler.pkl')

class DiabetesInput(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

@router.post("/predict_diabetes")
def predict_diabetes(input_data: DiabetesInput):
    data = np.array([[
        input_data.Pregnancies,
        input_data.Glucose,
        input_data.BloodPressure,
        input_data.SkinThickness,
        input_data.Insulin,
        input_data.BMI,
        input_data.DiabetesPedigreeFunction,
        input_data.Age
    ]])
    
    # Scale data
    data_scaled = scaler.transform(data)
    
    # Predict
    prediction = model.predict(data_scaled)[0]
    result = "Diabetic" if prediction == 1 else "Not Diabetic"
    
    return {"Prediction": int(prediction), "result": result}