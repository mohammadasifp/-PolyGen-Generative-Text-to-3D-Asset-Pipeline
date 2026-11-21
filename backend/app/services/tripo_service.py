
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openapi.tripo3d.ai/v3"
API_KEY = os.getenv("TRIPO_API_KEY")
MODEL = os.getenv("TRIPO_MODEL", "v3.1-20260211")


async def create_generation_task(prompt: str):

    if not API_KEY:
        raise RuntimeError(
            "TRIPO_API_KEY is missing. Check backend/.env"
        )

    url = f"{BASE_URL}/generation/text-to-model"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

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

            response.raise_for_status()

            result = response.json()

            print("Tripo response:", result)

            if result.get("code") != 0:
                raise RuntimeError(
                    f"Tripo API error: {result}"
                )

            task_id = result.get("data", {}).get("task_id")

            if not task_id:
                raise RuntimeError(
                    f"Tripo did not return task_id: {result}"
                )

            return {
                "task_id": task_id,
                "status": "queued",
                "prompt": prompt
            }

    except httpx.HTTPStatusError as error:
        status_code = error.response.status_code
        response_body = error.response.text[:2000]

        raise RuntimeError(
            f"Tripo HTTP {status_code}: {response_body}"
        ) from error

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Tripo connection error: {type(error).__name__}: {error}"
        ) from error
