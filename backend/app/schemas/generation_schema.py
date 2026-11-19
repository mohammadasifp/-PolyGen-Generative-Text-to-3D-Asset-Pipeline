
from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=500,
        description="Description of the 3D object"
    )


class GenerationResponse(BaseModel):
    success: bool
    status: str
    prompt: str
    message: str
    model_path: str | None = None
