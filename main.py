
from fastapi import FastAPI

app = FastAPI(
    title="PolyGen API",
    description="Generative Text-to-3D Asset Pipeline",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to PolyGen",
        "status": "Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "PolyGen"
    }
  
