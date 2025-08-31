
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.diabetes_api import router as diabetes_router
from routes.heart_api import router as heart_router
from routes.neurotap_api import router as neurotap_router

app = FastAPI(title="Cura Companion AI Clinic")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(diabetes_router, prefix="/diabetes")
app.include_router(heart_router, prefix="/heart")
app.include_router(neurotap_router, prefix="/neurotap")

@app.get("/")
def home():
    return {"message": "Welcome to Cura Companion AI Clinic"}