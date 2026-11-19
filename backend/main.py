
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.generation import router as generation_router

app = FastAPI(
    title="PolyGen API",
    description="Generative Text-to-3D Asset Pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "project": "PolyGen",
        "status": "Backend Running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(
    generation_router,
    prefix="/api",
    tags=["3D Generation"]
)
