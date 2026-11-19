
import platform
import sys

print("===== PolyGen System Check =====")

print("Python Version:", sys.version)
print("Operating System:", platform.system())
print("Processor:", platform.processor())

try:
    import torch

    print("PyTorch Version:", torch.__version__)
    print("CUDA Available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
        print(
            "GPU Memory:",
            round(
                torch.cuda.get_device_properties(0).total_memory
                / (1024 ** 3), 2
            ),
            "GB"
        )
    else:
        print("No CUDA GPU detected.")

except ImportError:
    print("PyTorch is not installed.")
