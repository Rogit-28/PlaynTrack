from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger("playntrack")


def is_gpu_available() -> bool:
    """Check whether a CUDA-capable GPU is available via PyTorch."""
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        logger.debug("PyTorch not installed; GPU check skipped")
        return False


def get_device() -> str:
    """Return the best available device string ('cuda' or 'cpu')."""
    if is_gpu_available():
        return "cuda"
    return "cpu"


def gpu_info() -> Optional[dict]:
    """Return basic GPU information or ``None`` if no GPU is found."""
    try:
        import torch

        if not torch.cuda.is_available():
            return None
        return {
            "device_name": torch.cuda.get_device_name(0),
            "device_count": torch.cuda.device_count(),
            "vram_total_mb": round(
                torch.cuda.get_device_properties(0).total_mem / 1e6, 1
            ),
            "vram_allocated_mb": round(torch.cuda.memory_allocated(0) / 1e6, 1),
        }
    except ImportError:
        return None


def clear_gpu_cache() -> None:
    """Release cached GPU memory."""
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:
        pass
