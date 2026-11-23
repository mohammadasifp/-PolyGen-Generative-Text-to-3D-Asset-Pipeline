
from copy import error

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fastapi import HTTPException
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
    task_id = create_generation_task(request.prompt)

    return {
        "task_id": task_id,
        "status": "queued",
        "message": "3D generation task created successfully"
    }

    except RuntimeError as error:
        message = str(error)

        if "INSUFFICIENT_CREDITS" in message:
            raise HTTPException(
                status_code=402,
                detail="Tripo credits are insufficient. "
                   "Please use Demo Mode or add provider credits."
        )

    raise HTTPException(
        status_code=502,
        detail="The 3D generation provider returned an error."
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
        
        

from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.tripo_service import (
    create_generation_task,
    get_generation_status,
    download_generated_model,
)

router = APIRouter()

SAMPLE_MODELS_DIR = (
    Path(__file__).resolve().parents[2] / "sample_models"
)


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=500)
    mode: Literal["tripo", "demo"] = "tripo"


@router.post("/generate")
async def generate_model(request: GenerationRequest):

    # FREE DEMO MODE
    if request.mode == "demo":

        demo_model = SAMPLE_MODELS_DIR / "demo.glb"

        if not demo_model.is_file():
            raise HTTPException(
                status_code=404,
                detail="Demo model not found. Add demo.glb to backend/sample_models/"
            )

        return {
            "mode": "demo",
            "status": "completed",
            "prompt": request.prompt,
            "model_url": "/sample-models/demo.glb",
            "message": (
                "Demo model returned successfully. "
                "This is a sample model, not AI-generated output."
            )
        }

    # TRIPO AI MODE
    try:
        result = await create_generation_task(request.prompt)

        return {
            "mode": "tripo",
            **result
        }

    except RuntimeError as error:

        error_message = str(error)

        if "INSUFFICIENT_CREDITS" in error_message:
            raise HTTPException(
                status_code=402,
                detail="Tripo credits are insufficient. "
                       "Switch to Demo Mode or add provider credits."
            )

        print("Tripo generation error:", error_message)

        raise HTTPException(
            status_code=502,
            detail="Unable to create a Tripo generation task."
        )


@router.get("/generate/{task_id}")
async def check_generation_status(task_id: str):

    try:
        task = await get_generation_status(task_id)

        status = task.get("status")

        if status == "success":

            output = task.get("output", {})
            model_url = output.get("model_url")

            if not model_url:
                raise HTTPException(
                    status_code=502,
                    detail="Tripo completed the task but returned no model URL."
                )

            downloaded = await download_generated_model(
                model_url,
                task_id
            )

            return {
                "mode": "tripo",
                "task_id": task_id,
                "status": "completed",
                "model_url": (
                    f"/models/{downloaded['filename']}"
                )
            }

        if status in ["failed", "cancelled", "banned", "expired"]:
            raise HTTPException(
                status_code=400,
                detail=f"Tripo generation {status}."
            )

        return {
            "mode": "tripo",
            "task_id": task_id,
            "status": status,
            "message": "3D model generation is still processing."
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except RuntimeError as error:
        print("Tripo status error:", str(error))
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve Tripo generation status."
        )
