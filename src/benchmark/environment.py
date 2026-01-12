import platform
import sys

import psutil

try:
    import torch
except ImportError:
    torch = None

try:
    import transformers
except ImportError:
    transformers = None

try:
    import pynvml
    _NVML_AVAILABLE = True
except ImportError:
    _NVML_AVAILABLE = False


def get_environment_metadata() -> dict:
    """
    Collect hardware and software environment metadata.
    """
    metadata = {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version.split()[0],
        "cpu_cores": psutil.cpu_count(logical=True),
        "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "torch_version": torch.__version__ if torch else None,
        "transformers_version": transformers.__version__ if transformers else None,
        "gpu": None,
    }

    if _NVML_AVAILABLE:
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            gpu_mem = pynvml.nvmlDeviceGetMemoryInfo(handle).total

            metadata["gpu"] = {
                "name": gpu_name.decode("utf-8") if isinstance(gpu_name, bytes) else gpu_name,
                "total_vram_gb": round(gpu_mem / (1024 ** 3), 2),
            }

            pynvml.nvmlShutdown()
        except Exception:
            metadata["gpu"] = None

    return metadata
