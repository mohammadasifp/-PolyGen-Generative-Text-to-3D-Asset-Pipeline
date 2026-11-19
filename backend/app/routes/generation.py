
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.generation_service import generate_model

router = APIRouter()


class GenerationRequest(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=500
    )


@router.post("/generate")
def create_model(request: GenerationRequest):

    try:
        result = generate_model(request.prompt)

        return {
            "success": True,
            "status": "completed",
            "prompt": request.prompt,
            "result": result
        }

    except NotImplementedError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "status": "not_configured",
                "message": str(error)
            }
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected generation error occurred."
        )
