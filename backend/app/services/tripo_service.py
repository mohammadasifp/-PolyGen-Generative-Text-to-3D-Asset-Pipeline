
import os
import re
import uuid
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openapi.tripo3d.ai/v3"

API_KEY = os.getenv("TRIPO_API_KEY")
MODEL = os.getenv("TRIPO_MODEL", "v3.1-20260211")

GENERATED_DIR = (
    Path(__file__).resolve().parents[2] / "generated_models"
)

GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def get_headers():
    if not API_KEY:
        raise RuntimeError(
            "TRIPO_API_KEY is missing. Configure it in backend/.env"
        )

    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }



async def create_generation_task(prompt: str):

    if not API_KEY:
        raise RuntimeError(
            "TRIPO_API_KEY is missing. Check backend/.env"
        )

    url = f"{BASE_URL}/generation/text-to-model"

    headers = get_headers()

    payload = {
        "prompt": prompt,
        "model": MODEL,
        "texture": True,
        "pbr": True
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.post(
                url,
                headers=headers,
                json=payload
            )

            print("Tripo HTTP status:", response.status_code)

            try:
                result = response.json()
            except ValueError:
                raise RuntimeError(
                    f"Invalid Tripo response: HTTP {response.status_code}"
                )

            # Handle insufficient credits
            if result.get("code") == 2010:
                raise RuntimeError(
                    "INSUFFICIENT_CREDITS: "
                    "Your Tripo account does not have enough credits."
                )

            # Handle other HTTP errors
            if response.is_error:
                raise RuntimeError(
                    f"TRIPO_ERROR: HTTP {response.status_code}: "
                    f"{result.get('message', 'Unknown provider error')}"
                )

            # Handle other Tripo API errors
            if result.get("code") != 0:
                raise RuntimeError(
                    f"TRIPO_ERROR: {result.get('message', 'Unknown Tripo error')}"
                )

            task_id = result.get("data", {}).get("task_id")

            if not task_id:
                raise RuntimeError(
                    "Tripo did not return a task_id"
                )

            print("Tripo task created:", task_id)

            return {
                "task_id": task_id,
                "status": "queued",
                "prompt": prompt
            }

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Tripo connection error: "
            f"{type(error).__name__}: {error}"
        ) from error



async def get_generation_status(task_id: str):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", task_id):
        raise ValueError("Invalid task ID")

    url = f"{BASE_URL}/tasks/{task_id}"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            url,
            headers=get_headers()
        )

        response.raise_for_status()
        result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(
            result.get("message", "Could not retrieve task status")
        )

    return result.get("data", {})


async def download_generated_model(model_url: str, task_id: str):
    if not model_url.startswith("https://"):
        raise RuntimeError("Invalid model download URL")

    filename = f"{uuid.uuid4().hex}.glb"
    output_path = GENERATED_DIR / filename

    async with httpx.AsyncClient(
        timeout=120,
        follow_redirects=True
    ) as client:
        response = await client.get(model_url)
        response.raise_for_status()

    # Basic file-size protection: 100 MB maximum.
    if len(response.content) > 100 * 1024 * 1024:
        raise RuntimeError("Generated model exceeds 100 MB")

    if not response.content:
        raise RuntimeError("Downloaded model is empty")

    output_path.write_bytes(response.content)

    return {
        "filename": filename,
        "file_path": str(output_path)
    }
