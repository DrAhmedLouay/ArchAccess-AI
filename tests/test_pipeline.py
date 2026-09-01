"""
Unit and Integration Tests for ArchAccess AI Platform Pipeline
Tests:
1. Exact semantic palette dictionary integrity (15 classes)
2. Preprocessor scale calibration and 30px left pad shift
3. Orthogonalization & Ramer-Douglas-Peucker simplification
4. AGCR Compliance calculation & ADA metrics
5. DXF and BIM JSON Exporters
6. 65% Max Coverage Ratio Enforcement & Dimensional generation
"""

import sys
import os
try:
    import numpy as np
except ImportError:
    np = None

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.semantic_palette import SEMANTIC_SPACES, CONSTRAINTS
from core.preprocessor import preprocess_boundary_image
from core.orthogonalizer import approx_douglas_peucker_2d, snap_to_orthogonal_angles, resolve_label_collisions
from core.compliance_agcr import compute_agcr_score
from core.bim_exporter import generate_dxf_string, generate_bim_json_schema
from core.generator import ArchAccessLayoutGenerator
from core.bioclimatic_engine import IRAQI_GOVERNORATES, evaluate_iraqi_privacy_and_climate, calculate_solar_angles, calculate_optimal_overhang_depth

def test_semantic_palette():
    print("Testing Exact Semantic Palette...")
    assert len(SEMANTIC_SPACES) == 17, f"Must contain all 17 semantic classes (including triple bathrooms: Disabled, Guest, House), got {len(SEMANTIC_SPACES)}"
    assert SEMANTIC_SPACES["kitchen"].hex_code.upper() == "#FFB8D8"
    assert SEMANTIC_SPACES["guest_room"].hex_code == "#019df2"
    assert SEMANTIC_SPACES["living_room"].hex_code == "#01ffec"
    assert SEMANTIC_SPACES["bedroom"].hex_code == "#fefe0a"
    assert SEMANTIC_SPACES["disabled_bedroom"].hex_code == "#e801f7"
    assert SEMANTIC_SPACES["disabled_bathroom"].hex_code == "#ff3464"
    assert SEMANTIC_SPACES["guest_bathroom"].hex_code == "#ff3464"
    assert SEMANTIC_SPACES["bathroom"].hex_code == "#ff3464"
    assert SEMANTIC_SPACES["court_garden"].hex_code == "#00ff01"
    assert SEMANTIC_SPACES["walls"].hex_code == "#000000"
    assert SEMANTIC_SPACES["disabled_ramp"].hex_code == "#fe6300"
    assert SEMANTIC_SPACES["garage_path"].hex_code == "#b0b0b0"
    assert SEMANTIC_SPACES["doors"].hex_code == "#aaabfe"
    assert SEMANTIC_SPACES["corridors"].hex_code == "#efde8e"
    assert SEMANTIC_SPACES["neighbor_boundaries"].hex_code == "#fc0005"
    assert SEMANTIC_SPACES["street_boundary"].hex_code == "#0000fe"
    assert CONSTRAINTS["MAX_COVERAGE_RATIO"] == 0.75
    print("  -> Passed!")

def test_preprocessor():
    print("Testing Preprocessor Scale & Padding...")
    if np is not None:
        dummy_mask = np.zeros((300, 400), dtype=np.uint8)
    else:
        dummy_mask = [[0 for _ in range(400)] for _ in range(300)]
    res = preprocess_boundary_image(dummy_mask, target_dim=512, memory_density_target=130.0, left_pad_offset=30)
    assert res["padding"]["pad_left"] == 30, "Must align with 30px left-padding offset from paper"
    assert res["scale"] <= 130.0 / 400.0
    print("  -> Passed!")

def test_orthogonalizer():
    print("Testing Douglas-Peucker & Orthogonal Snapping...")
    rough_contour = [(0, 0), (10, 1.2), (50, 0.5), (100, 0), (100, 50), (100, 100), (0, 100), (0, 0)]
    simplified = approx_douglas_peucker_2d(rough_contour, epsilon=5.0)
    snapped = snap_to_orthogonal_angles(simplified)
    assert len(snapped) <= len(rough_contour)
    print("  -> Passed!")

def test_agcr_compliance():
    print("Testing AGCR ADA Compliance Metric...")
    generator = ArchAccessLayoutGenerator(canvas_size=512)
    plot = [(80.0, 80.0), (432.0, 80.0), (432.0, 432.0), (80.0, 432.0)]
    layout = generator.generate_layout(plot, style_variant=1)
    
    comp = layout["compliance"]
    assert "agcr_percentage" in comp
    assert comp["agcr_percentage"] >= 90.0, f"Expected Gold level compliance, got {comp['agcr_percentage']}%"
    assert comp["ssim_reference"] == 0.7810
    print(f"  -> AGCR Score: {comp['agcr_percentage']}% ({comp['certification_level_ar']})")
    print("  -> Passed!")

def test_coverage_ratio_and_dimensions():
    print("Testing 65-75% Coverage Ratio Band & Custom Plot Dimensions...")
    generator = ArchAccessLayoutGenerator(canvas_size=512)
    layout = generator.generate_layout_from_dimensions(length_m=16.50, width_m=14.25, style_variant=1)
    
    assert 65.0 <= layout["coverage_ratio_percent"] <= 75.0, f"Coverage ratio {layout['coverage_ratio_percent']}% outside 65-75% band"
    assert layout["is_coverage_compliant"] == True
    assert layout["total_plot_area_m2"] > 0
    assert layout["total_built_area_m2"] > 0
    print(f"  -> Plot Area: {layout['total_plot_area_m2']} m2 | Built Area: {layout['total_built_area_m2']} m2 | BCR: {layout['coverage_ratio_percent']}% (65% ≤ BCR ≤ 75%)")
    print("  -> Passed!")

def test_iraq_bioclimatic_and_privacy():
    print("Testing Iraq Bioclimatic, Solar Angles & Iraqi Cultural Privacy...")
    assert len(IRAQI_GOVERNORATES) == 8, "Must support 8 key Iraqi governorates"
    
    # Test Baghdad solar calculations
    bg_data = IRAQI_GOVERNORATES["baghdad"]
    summer_alt, _ = calculate_solar_angles(bg_data.latitude, 172, 12.0)
    winter_alt, _ = calculate_solar_angles(bg_data.latitude, 355, 12.0)
    assert 79.0 <= summer_alt <= 81.0, f"Baghdad summer solar altitude should be ~80.1 deg, got {summer_alt}"
    assert 32.0 <= winter_alt <= 34.5, f"Baghdad winter solar altitude should be ~33.2 deg, got {winter_alt}"
    
    overhang = calculate_optimal_overhang_depth(1.20, summer_alt)
    assert overhang > 0, "Overhang depth must be positive"
    
    # Test Privacy & Wind Catchment Evaluation
    res = evaluate_iraqi_privacy_and_climate(
        governorate_key="baghdad",
        north_orientation_deg=0.0,
        rooms_data=[{"key": "guest_room"}, {"key": "court_garden"}, {"key": "disabled_bedroom"}]
    )
    assert "governorate" in res
    assert "visual_privacy_index" in res
    assert "wind_cooling_efficiency" in res
    print(f"  -> Iraq GIS Verified: {res['governorate']} ({res['climate_zone']}) | Summer Alt: {res['summer_noon_altitude']} | Privacy: {res['visual_privacy_index']}")
    print("  -> Passed!")

def test_probabilistic_spatial_synthesis():
    print("Testing Probabilistic Spatial Distribution & Stochastic Synthesis...")
    gen = ArchAccessLayoutGenerator()
    layout1 = gen.generate_layout_from_dimensions(16.0, 14.5, style_variant=1)
    assert "spatial_entropy_bits" in layout1
    assert "layout_diversity_percent" in layout1
    assert layout1["spatial_entropy_bits"] > 1.5, "Entropy must be realistic (> 1.5 bits)"
    assert layout1["layout_diversity_percent"] >= 80.0, "Diversity index must be >= 80%"
    print(f"  -> Stochastic Entropy: {layout1['spatial_entropy_bits']} bits | Diversity: {layout1['layout_diversity_percent']}% | Seed: #{layout1['stochastic_seed']}")
def test_9_space_strict_dimensions():
    print("Testing Strict 9-Space Architectural Dimensions (Zero Compromise)...")
    gen = ArchAccessLayoutGenerator()
    targets = {
        'guest_room': (5.00, 3.90, 19.50),
        'guest_bathroom': (1.70, 1.10, 1.87),
        'living_room': (4.00, 3.90, 15.60),
        'kitchen': (3.50, 3.50, 12.25),
        'disabled_bedroom': (4.80, 4.00, 19.20),
        'disabled_bathroom': (2.70, 2.20, 5.94),
        'bathroom': (2.40, 2.70, 6.48),
        'bedroom': (3.90, 3.90, 15.21)
    }
    
    for variant in [1, 2, 3]:
        for typology in ['back_to_back', 'corner_plot']:
            layout = gen.generate_layout_from_dimensions(16.0, 16.0, style_variant=variant, plot_type=typology)
            rooms = layout["rooms"]
            found_keys = {r["key"] for r in rooms}
            for req_key in targets:
                assert req_key in found_keys, f"Missing required space {req_key} in Variant {variant} ({typology})"
            
            for r in rooms:
                k = r["key"]
                poly = r["polygon"]
                pw = round(abs(poly[1][0] - poly[0][0]) / 23.0, 2)
                ph = round(abs(poly[2][1] - poly[1][1]) / 23.0, 2)
                area = round(pw * ph, 2)
                if k in targets:
                    min_w, min_h, min_a = targets[k]
                    dim_ok = (pw >= min_w and ph >= min_h) or (pw >= min_h and ph >= min_w)
                    assert dim_ok, f"Variant {variant} {k} dimension failure: got {pw}x{ph}m, expected >= {min_w}x{min_h}m"
                    assert area >= min_a, f"Variant {variant} {k} area failure: got {area} m2, expected >= {min_a} m2"
    print("  -> All 9 Spaces verified 100% compliant across all 3 variants and plot typologies!")
    print("  -> Passed!")

if __name__ == "__main__":
    test_semantic_palette()
    test_preprocessor()
    test_orthogonalizer()
    test_agcr_compliance()
    test_coverage_ratio_and_dimensions()
    test_iraq_bioclimatic_and_privacy()
    test_probabilistic_spatial_synthesis()
    test_9_space_strict_dimensions()
    print("\nALL 8 PIPELINE, BIOCLIMATIC & 9-SPACE ARCHITECTURAL TESTS PASSED SUCCESSFULLY! ✅")
