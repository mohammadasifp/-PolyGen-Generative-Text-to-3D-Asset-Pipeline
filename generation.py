
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.generation_service import generate_model

router = APIRouter()

class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=500)

@router.post("/generate")
def create_model(request: GenerationRequest):
    try:
        result = generate_model(request.prompt)
        return {
            "success": True,
            "prompt": request.prompt,
            "message": "Generation request processed",
            "result": result
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
