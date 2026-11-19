
import os


def generate_model(prompt: str):
    # Check whether an AI model provider is configured.
    model_provider = os.getenv("POLYGEN_MODEL", "").strip()

    if not model_provider:
        return {
            "success": False,
            "status": "not_configured",
            "prompt": prompt,
            "message": (
                "Text-to-3D model is not configured yet. "
                "Please configure TripoSR or Shap-E."
            ),
            "model_path": None
        }

    # Actual model inference will be integrated here.
    return {
        "success": False,
        "status": "integration_pending",
        "prompt": prompt,
        "message": (
            f"{model_provider} is selected, "
            "but model inference is not implemented yet."
        ),
        "model_path": None
    }
