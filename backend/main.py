
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.generation import router as generation_router

from app.services.system_service import get_system_status


from pathlib import Path
from fastapi.staticfiles import StaticFiles

GENERATED_DIR = Path(__file__).resolve().parent / "generated_models"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


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
app.mount(
    "/models",
    StaticFiles(directory=GENERATED_DIR),
    name="models"
)


@app.get("/")
def home():
    return {
        "project": "PolyGen",
        "status": "Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "PolyGen"
    }

@app.get("/api/system/status", tags=["System"])
def system_status():
    return get_system_status()


app.include_router(
    generation_router,
    prefix="/api",
    tags=["3D Generation"]
)
