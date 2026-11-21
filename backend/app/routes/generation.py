
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.tripo_service import (
    create_generation_task,
    get_generation_status,
    download_generated_model
)

router = APIRouter()


class GenerationRequest(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=500
    )


@router.post("/generate")
async def generate_model(request: GenerationRequest):

    try:
        result = await create_generation_task(request.prompt)

        return {
            "success": True,
            "status": "queued",
            "message": "3D generation task created",
            "prompt": request.prompt,
            "task_id": result["task_id"]
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the Text-to-3D provider"
        )


@router.get("/generate/{task_id}")
async def check_generation(task_id: str):

    try:
        task = await get_generation_status(task_id)

        status = task.get("status", "unknown")
        progress = task.get("progress", 0)

        if status == "success":
            model_url = task.get("output", {}).get("model_url")

            if not model_url:
                raise HTTPException(
                    status_code=502,
                    detail="Generation completed but model URL is missing"
                )

            saved_model = await download_generated_model(
                model_url,
                task_id
            )

            return {
                "success": True,
                "status": "completed",
                "progress": 100,
                "task_id": task_id,
                "model": saved_model["filename"],
                "model_url": (
                    f"/models/{saved_model['filename']}"
                )
            }

        if status in ("failed", "cancelled", "banned", "expired"):
            return {
                "success": False,
                "status": status,
                "task_id": task_id,
                "message": "3D generation did not complete"
            }

        return {
            "success": True,
            "status": status,
            "progress": progress,
            "task_id": task_id,
            "message": "3D model generation is in progress"
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except RuntimeError as error:
        print("PolyGen generation error:", str(error))

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )