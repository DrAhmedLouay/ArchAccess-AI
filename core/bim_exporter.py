"""
BIM & CAD Vector Exporter
Transforms crystallized orthogonal layouts into:
1. DXF CAD files with dedicated architectural layers (Walls, Doors, Rooms, Circulation, ADA Checkpoints)
2. Revit-Ready BIM JSON / IFC Property Sets for direct wall/door generation
"""

import json
from typing import Dict, List, Any

def generate_dxf_string(rooms: List[Dict[str, Any]], boundary_points: List[tuple]) -> str:
    """
    Generates a standard ASCII DXF format string containing layered architectural vectors.
    Compatible with AutoCAD, Autodesk Revit, Rhino, SketchUp.
    """
    dxf_lines = [
        "0", "SECTION",
        "2", "HEADER",
        "9", "$ACADVER", "1", "AC1015",
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "TABLES",
        "0", "TABLE", "2", "LAYER",
        # Layers
        "0", "LAYER", "2", "A-WALL-EXTR", "70", "0", "62", "7", "6", "CONTINUOUS",
        "0", "LAYER", "2", "A-WALL-INTR", "70", "0", "62", "8", "6", "CONTINUOUS",
        "0", "LAYER", "2", "A-DOOR-ADA", "70", "0", "62", "1", "6", "CONTINUOUS",
        "0", "LAYER", "2", "A-AREA-TEXT", "70", "0", "62", "3", "6", "CONTINUOUS",
        "0", "LAYER", "2", "A-CIRC-ADA-150", "70", "0", "62", "4", "6", "CONTINUOUS",
        "0", "ENDTAB",
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "ENTITIES"
    ]
    
    # Write Boundary / Exterior Walls
    if boundary_points and len(boundary_points) > 1:
        for i in range(len(boundary_points)):
            p1 = boundary_points[i]
            p2 = boundary_points[(i + 1) % len(boundary_points)]
            dxf_lines.extend([
                "0", "LINE",
                "8", "A-WALL-EXTR",
                "10", f"{p1[0]:.2f}", "20", f"{-p1[1]:.2f}", "30", "0.0",
                "11", f"{p2[0]:.2f}", "21", f"{-p2[1]:.2f}", "31", "0.0"
            ])
            
    # Write Room Polygons & Interior Walls
    for room in rooms:
        poly = room.get("polygon", [])
        if len(poly) > 1:
            for i in range(len(poly) - 1):
                p1 = poly[i]
                p2 = poly[i + 1]
                dxf_lines.extend([
                    "0", "LINE",
                    "8", "A-WALL-INTR",
                    "10", f"{p1[0]:.2f}", "20", f"{-p1[1]:.2f}", "30", "0.0",
                    "11", f"{p2[0]:.2f}", "21", f"{-p2[1]:.2f}", "31", "0.0"
                ])
                
        # Room Label and Centroid Marker
        cx, cy = room.get("centroid", (0, 0))
        dxf_lines.extend([
            "0", "TEXT",
            "8", "A-AREA-TEXT",
            "10", f"{cx:.2f}", "20", f"{-cy:.2f}", "30", "0.0",
            "40", "12.0",  # Text height
            "1", f"{room.get('name_en', 'Room')} ({room.get('area_m2', 0)} m2)"
        ])
        
        # 1.5m Turning Circle Marker
        dxf_lines.extend([
            "0", "CIRCLE",
            "8", "A-CIRC-ADA-150",
            "10", f"{cx:.2f}", "20", f"{-cy:.2f}", "30", "0.0",
            "40", "18.75"  # Radius for 1.50m diameter (0.75m * 25px/m)
        ])
        
    dxf_lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(dxf_lines)

def generate_bim_json_schema(rooms: List[Dict[str, Any]], compliance_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produces structured BIM data schema consumable by pyRevit or IFC generation tools.
    """
    bim_elements = {
        "project_metadata": {
            "standards": "ADA Standards for Accessible Design 2010 (Section 304)",
            "generator": "ArchAccess AI - Universal Design Deep Generative Modeler",
            "scale_factor_px_per_m": 25.0,
            "unit": "Meters",
            "total_area_m2": round(sum(r.get("area_m2", 0) for r in rooms), 2),
            "agcr_score": compliance_data.get("agcr_percentage", 95.0),
            "certification": compliance_data.get("certification_level_en", "GOLD")
        },
        "walls": [],
        "doors": [],
        "spaces": []
    }
    
    wall_id = 1
    for room in rooms:
        poly = room.get("polygon", [])
        # Space definition
        cx, cy = room.get("centroid", (0, 0))
        bim_elements["spaces"].append({
            "space_id": f"SP-{room.get('key', 'room')}",
            "name_ar": room.get("name_ar", ""),
            "name_en": room.get("name_en", ""),
            "category": room.get("key", ""),
            "area_m2": room.get("area_m2", 0),
            "centroid_m": {"x": round(cx / 25.0, 3), "y": round(cy / 25.0, 3)},
            "ada_clearance_diameter_m": room.get("min_turning_diameter", 1.50)
        })
        
        # Walls for this room
        for i in range(len(poly) - 1):
            p1 = poly[i]
            p2 = poly[i + 1]
            bim_elements["walls"].append({
                "wall_id": f"W-{wall_id}",
                "family_name": "Basic Wall - 200mm Concrete Masonry",
                "thickness_m": 0.20,
                "height_m": 3.00,
                "start_point_m": {"x": round(p1[0] / 25.0, 3), "y": round(p1[1] / 25.0, 3)},
                "end_point_m": {"x": round(p2[0] / 25.0, 3), "y": round(p2[1] / 25.0, 3)}
            })
            wall_id += 1
            
        # Add ADA Compliant Door for room
        bim_elements["doors"].append({
            "door_id": f"D-{room.get('key', 'room')}",
            "family_name": "Single-Flush ADA Accessible Door - 950x2100mm",
            "clear_opening_width_m": 0.95,  # >= 0.90m standard
            "height_m": 2.10,
            "host_space": room.get("name_en", "")
        })
        
    return bim_elements
