# backend/app/services/meshy_service.py

import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.meshy.ai/openapi/v2"
API_KEY = os.getenv("MESHY_API_KEY")

GENERATED_DIR = (
    Path(__file__).resolve().parents[2] / "generated_models"
)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def get_headers():
    if not API_KEY:
        raise RuntimeError(
            "MESHY_API_KEY is missing. Configure it in backend/.env"
        )

    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


async def create_meshy_preview(prompt: str):
    payload = {
        "mode": "preview",
        "prompt": prompt,
        "ai_model": "meshy-7.1",
        "target_formats": ["glb"],
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{BASE_URL}/text-to-3d",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

    task_id = result.get("result")
    if not task_id:
        raise RuntimeError(f"Meshy returned no task ID: {result}")

    return {
        "task_id": task_id,
        "status": "PENDING",
        "stage": "preview",
    }


async def create_meshy_refine(preview_task_id: str):
    payload = {
        "mode": "refine",
        "preview_task_id": preview_task_id,
        "enable_pbr": True,
        "target_formats": ["glb"],
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{BASE_URL}/text-to-3d",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

    task_id = result.get("result")
    if not task_id:
        raise RuntimeError(f"Meshy returned no refine task ID: {result}")

    return {
        "task_id": task_id,
        "status": "PENDING",
        "stage": "refine",
    }


async def get_meshy_status(task_id: str):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{BASE_URL}/text-to-3d/{task_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


async def download_meshy_model(model_url: str):
    parsed = urlparse(model_url)

    if (
        parsed.scheme != "https"
        or parsed.hostname != "assets.meshy.ai"
    ):
        raise RuntimeError("Invalid Meshy model download URL")

    async with httpx.AsyncClient(
        timeout=120,
        follow_redirects=True,
    ) as client:
        response = await client.get(model_url)
        response.raise_for_status()

    if not response.content:
        raise RuntimeError("Downloaded Meshy model is empty")

    if len(response.content) > 100 * 1024 * 1024:
        raise RuntimeError("Meshy model exceeds 100 MB")

    filename = f"meshy_{uuid.uuid4().hex}.glb"
    output_path = GENERATED_DIR / filename
    output_path.write_bytes(response.content)

    return {
        "filename": filename,
        "file_path": str(output_path),
    }
