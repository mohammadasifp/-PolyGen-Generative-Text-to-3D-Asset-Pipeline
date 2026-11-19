
from fastapi import APIRouter
from app.schemas.generation_schema import (
    GenerationRequest,
    GenerationResponse
)
from app.services.generation_service import generate_model

router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerationResponse
)
def create_generation(request: GenerationRequest):

    result = generate_model(request.prompt)

    return result
