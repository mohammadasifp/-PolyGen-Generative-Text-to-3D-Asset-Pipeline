
import sys
import platform

def get_system_status():
    try:
        import torch

        cuda_available = torch.cuda.is_available()

        if cuda_available:
            device = torch.cuda.get_device_name(0)
        else:
            device = "CPU"

        torch_version = torch.__version__

    except ImportError:
        cuda_available = False
        device = "Unknown"
        torch_version = None

    return {
        "project": "PolyGen",
        "python_version": sys.version.split()[0],
        "operating_system": platform.system(),
        "pytorch_version": torch_version,
        "cuda_available": cuda_available,
        "device": device,
        "api_status": "running"
    }
