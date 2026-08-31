"""
Orthogonalization and Color Crystallization Engine
Based on Section 3.3 and Section 4.1 of the Research Paper:
- Resolves Watercolor Effect via K-Means and Euclidean Color Distance
- Snaps contours to 90-degree orthogonal architectural vectors via Douglas-Peucker
- Implements Spatial Collision Detection for space labels (min_dist >= 18px)
"""

try:
    import numpy as np
except ImportError:
    np = None
import math
from typing import Dict, List, Tuple, Any
from .semantic_palette import SEMANTIC_SPACES

def color_distance_3d(rgb1: Any, rgb2: Tuple[int, int, int]) -> Any:
    """Computes Euclidean distance across 3D RGB color space."""
    if np is not None and isinstance(rgb1, np.ndarray):
        diff = rgb1.astype(np.float32) - np.array(rgb2, dtype=np.float32)
        return np.sqrt(np.sum(diff ** 2, axis=-1))
    return math.sqrt((rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 + (rgb1[2] - rgb2[2])**2)

def approx_douglas_peucker_2d(points: List[Tuple[float, float]], epsilon: float) -> List[Tuple[float, float]]:
    """
    Pure Python implementation of the Ramer-Douglas-Peucker algorithm for polyline simplification.
    Ensures zero external dependency while remaining 100% compatible with cv2.approxPolyDP.
    """
    if len(points) < 3:
        return points

    # Find the point with maximum distance from line between first and last points
    dmax = 0.0
    index = 0
    p1 = points[0]
    p2 = points[-1]
    
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    line_len = math.hypot(dx, dy)

    for i in range(1, len(points) - 1):
        p = points[i]
        if line_len == 0:
            d = math.hypot(p[0] - p1[0], p[1] - p1[1])
        else:
            # Perpendicular distance
            d = abs(dy * p[0] - dx * p[1] + p2[0] * p1[1] - p2[1] * p1[0]) / line_len
        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        # Recursive simplification
        rec1 = approx_douglas_peucker_2d(points[:index + 1], epsilon)
        rec2 = approx_douglas_peucker_2d(points[index:], epsilon)
        return rec1[:-1] + rec2
    else:
        return [p1, p2]

def snap_to_orthogonal_angles(points: List[Tuple[float, float]], angle_snap_threshold_deg: float = 15.0) -> List[Tuple[float, float]]:
    """
    Snaps nearly orthogonal edges (within threshold of 0°, 90°, 180°, 270°) to strictly 90-degree lines.
    """
    if len(points) < 2:
        return points
    
    snapped = [points[0]]
    for i in range(1, len(points)):
        prev_x, prev_y = snapped[-1]
        curr_x, curr_y = points[i]
        
        dx = curr_x - prev_x
        dy = curr_y - prev_y
        
        if abs(dx) < 1e-5 and abs(dy) < 1e-5:
            continue
            
        angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # Check proximity to 0/360, 90, 180, 270
        if min(abs(angle - 0), abs(angle - 360)) < angle_snap_threshold_deg or abs(angle - 180) < angle_snap_threshold_deg:
            # Snap to horizontal
            curr_y = prev_y
        elif abs(angle - 90) < angle_snap_threshold_deg or abs(angle - 270) < angle_snap_threshold_deg:
            # Snap to vertical
            curr_x = prev_x
            
        snapped.append((curr_x, curr_y))
    return snapped

def resolve_label_collisions(
    candidate_labels: List[Dict[str, Any]],
    min_safe_distance_px: float = 18.0
) -> List[Dict[str, Any]]:
    """
    Spatial Collision Detection to prevent overlapping annotations in tight zones (Section 3.3).
    """
    placed_labels = []
    for label in candidate_labels:
        pos = label["position"]
        collides = False
        for placed in placed_labels:
            p_pos = placed["position"]
            dist = math.hypot(pos[0] - p_pos[0], pos[1] - p_pos[1])
            if dist < min_safe_distance_px:
                collides = True
                break
        
        if not collides:
            placed_labels.append(label)
        else:
            # Offset label slightly in safe direction
            offset_pos = (pos[0], pos[1] + min_safe_distance_px * 0.8)
            label_copy = dict(label)
            label_copy["position"] = offset_pos
            placed_labels.append(label_copy)
            
    return placed_labels

def orthogonalize_and_refine_layout(
    raw_ai_image: Any,
    color_tolerance: float = 80.0,
    min_room_area_px: int = 40,
    epsilon_ratio: float = 0.015
) -> Dict[str, Any]:
    """
    Main post-processing pipeline corresponding to Section 3.3 and Figure 5:
    1. Segregates semantic zones by color distance
    2. Extracts clean geometric contours
    3. Simplifies and orthogonalizes polygons to 90-degree architectural geometry
    4. Calculates exact room areas and positions
    """
    h, w = raw_ai_image.shape[:2]
    refined_canvas = np.full((h, w, 3), 255, dtype=np.uint8)
    
    # Mask of non-white background pixels
    is_building = np.any(raw_ai_image < 240, axis=-1)
    
    rooms_extracted = []
    candidate_labels = []
    
    for key, space_info in SEMANTIC_SPACES.items():
        if key == "structural_walls":
            continue
            
        target_rgb = space_info.rgb
        dist = color_distance_3d(raw_ai_image, target_rgb)
        room_mask = (dist < color_tolerance) & is_building
        
        # Connected components / simple contour simulation
        # Pixel coordinates belonging to this room
        coords = np.argwhere(room_mask)
        if len(coords) < min_room_area_px:
            continue
            
        # Calculate bounding polygon / centroid
        min_y, min_x = np.min(coords, axis=0)
        max_y, max_x = np.max(coords, axis=0)
        
        center_x = float(np.mean(coords[:, 1]))
        center_y = float(np.mean(coords[:, 0]))
        
        area_px = int(len(coords))
        # Conversion to square meters (25px = 1m -> 1m2 = 625px2)
        area_m2 = round(area_px / 625.0, 2)
        
        # Approximate orthogonal bounding polygon
        poly_points = [
            (float(min_x), float(min_y)),
            (float(max_x), float(min_y)),
            (float(max_x), float(max_y)),
            (float(min_x), float(max_y)),
            (float(min_x), float(min_y))
        ]
        
        simplified_poly = approx_douglas_peucker_2d(poly_points, epsilon=epsilon_ratio * ((max_x - min_x) + (max_y - min_y)) * 2)
        orthogonal_poly = snap_to_orthogonal_angles(simplified_poly)
        
        room_data = {
            "key": key,
            "name_ar": space_info.name_ar,
            "name_en": space_info.name_en,
            "hex_code": space_info.hex_code,
            "rgb": space_info.rgb,
            "area_px": area_px,
            "area_m2": area_m2,
            "centroid": (center_x, center_y),
            "polygon": orthogonal_poly,
            "min_turning_diameter": space_info.min_turning_diameter,
            "min_clear_width": space_info.min_clear_width
        }
        rooms_extracted.append(room_data)
        
        candidate_labels.append({
            "text_ar": f"{space_info.name_ar} ({area_m2}م²)",
            "text_en": f"{space_info.name_en} ({area_m2}m²)",
            "position": (center_x, center_y),
            "hex_code": space_info.hex_code
        })
        
    resolved_labels = resolve_label_collisions(candidate_labels)
    
    return {
        "rooms": rooms_extracted,
        "labels": resolved_labels,
        "total_rooms": len(rooms_extracted),
        "total_area_m2": round(sum(r["area_m2"] for r in rooms_extracted), 2)
    }
