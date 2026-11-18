from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.generation import router as generation_router

app = FastAPI(
    title="PolyGen API",
    description="Starter API for the PolyGen text-to-3D asset pipeline",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home() -> dict[str, str]:
    return {"project": "PolyGen", "status": "Backend running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


app.include_router(generation_router, prefix="/api", tags=["3D Generation"])
