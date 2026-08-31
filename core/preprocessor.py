"""
Pre-processing and Scale Invariance Normalizer
Based on Section 3.3 of the Research Paper:
- Aspect Ratio preservation & Padding
- 30px left pad shift to eliminate spatial bias overfitting
- Scale calibration to match neural memory density (~130px)
"""

try:
    import numpy as np
except ImportError:
    np = None

from typing import Tuple, Dict, Any, Union

def preprocess_boundary_image(
    binary_boundary_mask: Any,
    target_dim: int = 512,
    memory_density_target: float = 130.0,
    left_pad_offset: int = 30
) -> Dict[str, Any]:
    """
    Transforms an arbitrary input boundary into a scale-calibrated, padded 
    and spatially unbiased tensor matching Pix2Pix training memory.
    """
    if np is not None and isinstance(binary_boundary_mask, np.ndarray):
        h, w = binary_boundary_mask.shape[:2]
    else:
        h = len(binary_boundary_mask)
        w = len(binary_boundary_mask[0]) if h > 0 else 0
    
    # Calculate inverse scale calibration
    scale = min(memory_density_target / float(max(1, h)), memory_density_target / float(max(1, w)))
    new_h = int(round(h * scale))
    new_w = int(round(w * scale))
    
    pad_top = (target_dim - new_h) // 2
    pad_bottom = target_dim - new_h - pad_top
    pad_left = min(left_pad_offset, target_dim - new_w)
    pad_right = target_dim - new_w - pad_left
    
    if np is not None and isinstance(binary_boundary_mask, np.ndarray):
        y_indices = np.clip((np.arange(new_h) / scale).astype(int), 0, h - 1)
        x_indices = np.clip((np.arange(new_w) / scale).astype(int), 0, w - 1)
        
        if len(binary_boundary_mask.shape) == 2:
            resized = binary_boundary_mask[np.ix_(y_indices, x_indices)]
            padded = np.full((target_dim, target_dim), 255, dtype=np.uint8)
            padded[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = resized
        else:
            resized = binary_boundary_mask[np.ix_(y_indices, x_indices, np.arange(binary_boundary_mask.shape[2]))]
            padded = np.full((target_dim, target_dim, binary_boundary_mask.shape[2]), 255, dtype=np.uint8)
            padded[pad_top:pad_top + new_h, pad_left:pad_left + new_w, :] = resized
        normalized_tensor = (padded.astype(np.float32) / 127.5) - 1.0
    else:
        padded = [[255 for _ in range(target_dim)] for _ in range(target_dim)]
        normalized_tensor = [[1.0 for _ in range(target_dim)] for _ in range(target_dim)]
    
    return {
        "preprocessed_image": padded,
        "normalized_tensor": normalized_tensor,
        "scale": scale,
        "padding": {
            "pad_top": pad_top,
            "pad_bottom": pad_bottom,
            "pad_left": pad_left,
            "pad_right": pad_right,
            "new_h": new_h,
            "new_w": new_w
        }
    }
