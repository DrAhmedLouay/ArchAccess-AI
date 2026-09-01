"""
Semantic Palette and Architectural Standards
Updated according to Universal Design Pix2Pix Research & Color-Coding Language:
- Plot Typologies:
  * Back-to-back (Single Frontage: 1 Street Boundary #0000fe, 3 Neighbor Boundaries #fc0005)
  * Corner Plot (Corner: 2 Street Boundaries #0000fe, 2 Neighbor Boundaries #fc0005)
- Outdoor vs Indoor Categorization:
  * Outdoor Spaces & Site Elements:
    - Street Boundary: #0000fe (Solid Blue Line)
    - Neighbor Boundaries: #fc0005 (Solid Red Line)
    - Site / Car Entrance Gate: #e2ac2e (Opening into the site boundary)
    - Garage / surrounding foot path: #b0b0b0
    - Disabled ramp: #fe6300 (ADA slope <= 1:12)
    - Indoor court / Garden / Shaft: #00ff01
  * Indoor Spaces & Building Elements:
    - Guest Room: #019df2
    - Living Room: #01ffec
    - Kitchen: #FFB8D8
    - Bedroom: #fefe0a
    - Disabled Bedroom: #e801f7
    - Disabled Bathroom: #ff3464
    - Bathroom: #ff3464
    - Corridors / services area: #efde8e
    - Opening in the walls (Doors): #aaabfe
    - Walls: #000000
"""

from dataclasses import dataclass
from typing import Tuple, Dict, List

@dataclass
class SpaceStandard:
    name_ar: str
    name_en: str
    hex_code: str
    rgb: Tuple[int, int, int]
    category: str  # "outdoor" or "indoor"
    min_turning_diameter: float  # In meters (ADA standard: 1.50m)
    min_clear_width: float       # In meters (ADA standard: 0.91m or 1.20m for kitchens)
    description: str

# 16-Class Complete Semantic Color-Coding System
SEMANTIC_SPACES: Dict[str, SpaceStandard] = {
    # Outdoor Spaces & Boundaries
    "street_boundary": SpaceStandard(
        name_ar="حد الشارع (واجهة مطلة على الشارع)",
        name_en="Street Boundary",
        hex_code="#0000fe",
        rgb=(0, 0, 254),
        category="outdoor",
        min_turning_diameter=0.0,
        min_clear_width=0.0,
        description="خط أزرق مصمت سميك يمثل حد القطعة المطل على الشارع"
    ),
    "neighbor_boundaries": SpaceStandard(
        name_ar="حدود الجوار (قطع مجاورة)",
        name_en="Neighbor Boundaries",
        hex_code="#fc0005",
        rgb=(252, 0, 5),
        category="outdoor",
        min_turning_diameter=0.0,
        min_clear_width=0.0,
        description="خط أحمر مصمت سميك يمثل الحدود الملاصقة للجيران والارتدادات"
    ),
    "site_entrance": SpaceStandard(
        name_ar="مدخل الأرض الخارجي (مدخل السيارة)",
        name_en="Site / Car Entrance",
        hex_code="#e2ac2e",
        rgb=(226, 172, 46),
        category="outdoor",
        min_turning_diameter=3.00,
        min_clear_width=3.00,
        description="فتحة مدخل الموقع وبوابة حركة السيارات من الشارع"
    ),
    "garage_path": SpaceStandard(
        name_ar="المرآب والممرات الخارجية المحيطة",
        name_en="Garage / surrounding foot path",
        hex_code="#b0b0b0",
        rgb=(176, 176, 176),
        category="outdoor",
        min_turning_diameter=1.50,
        min_clear_width=1.00,
        description="مساحات ارتداد خارجية مرصوفة وممرات حركة محيطة بالمبنى"
    ),
    "disabled_ramp": SpaceStandard(
        name_ar="منحدر مهيأ للكراسي المتحركة",
        name_en="Disabled ramp",
        hex_code="#fe6300",
        rgb=(254, 99, 0),
        category="outdoor",
        min_turning_diameter=1.50,
        min_clear_width=1.00,
        description="منحدر وصول آمن بميل ≤ 1:12 مع بسطة استراحة لربط المنسوب"
    ),
    "court_garden": SpaceStandard(
        name_ar="فناء داخلي / حديقة / منور",
        name_en="Indoor court / Garden / Shaft",
        hex_code="#00ff01",
        rgb=(0, 255, 1),
        category="outdoor",
        min_turning_diameter=1.50,
        min_clear_width=0.91,
        description="إضاءة وتهوية طبيعية مستمرة ومساحات خضراء مفتوحة"
    ),

    # Indoor Spaces & Architecture
    "guest_room": SpaceStandard(
        name_ar="غرفة الضيوف / الاستقبال",
        name_en="Guest Room",
        hex_code="#019df2",
        rgb=(1, 157, 242),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=5.00,
        description="فضاء استقبال رئيسي لا تقل أبعاده عن 5.00م × 3.90م (مساحة ≥ 19.50م²)"
    ),
    "living_room": SpaceStandard(
        name_ar="غرفة المعيشة العائلية",
        name_en="Living Room",
        hex_code="#01ffec",
        rgb=(1, 255, 236),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=4.00,
        description="فضاء معيشة رئيسي لا تقل أبعاده عن 4.00م × 3.90م (مساحة ≥ 15.60م²)"
    ),
    "kitchen": SpaceStandard(
        name_ar="المطبخ",
        name_en="Kitchen",
        hex_code="#FFB8D8",
        rgb=(255, 184, 216),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=3.50,
        description="مطبخ رحب لا تقل أبعاده عن 3.50م × 3.50م (مساحة ≥ 12.25م²)"
    ),
    "bedroom": SpaceStandard(
        name_ar="غرفة النوم القياسية",
        name_en="Bedroom",
        hex_code="#fefe0a",
        rgb=(254, 254, 10),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=3.90,
        description="غرفة نوم قياسية لا تقل أبعادها عن 3.90م × 3.90م (مساحة ≥ 15.21م²)"
    ),
    "disabled_bedroom": SpaceStandard(
        name_ar="غرفة نوم مهيأة لذوي الاحتياجات",
        name_en="Disabled Bedroom",
        hex_code="#e801f7",
        rgb=(232, 1, 247),
        category="indoor",
        min_turning_diameter=1.60,
        min_clear_width=4.80,
        description="غرفة نوم مهيأة لا تقل عن 4.80م × 4.00م (مساحة ≥ 19.20م²) مع دوران صافٍ ≥ 1.60م"
    ),
    "disabled_bathroom": SpaceStandard(
        name_ar="حمام مهيأ لذوي الاحتياجات (En-Suite)",
        name_en="En-Suite Disabled Bathroom",
        hex_code="#ff3464",
        rgb=(255, 52, 100),
        category="indoor",
        min_turning_diameter=1.60,
        min_clear_width=2.70,
        description="حمام مهيأ خاص لا تقل أبعاده عن 2.70م × 2.20م (مساحة ≥ 5.94م²) متصل مباشرة بالجناح المهيأ"
    ),
    "guest_bathroom": SpaceStandard(
        name_ar="حمام الضيوف / WC",
        name_en="Guest Bathroom / WC",
        hex_code="#ff3464",
        rgb=(255, 52, 100),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=1.70,
        description="حمام ضيوف لا يقل عن 1.70م × 1.10م (مساحة ≥ 1.87م²)"
    ),
    "bathroom": SpaceStandard(
        name_ar="حمام البيت العام",
        name_en="House Bathroom / General",
        hex_code="#ff3464",
        rgb=(255, 52, 100),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=2.40,
        description="حمام عام للعائلة لا يقل عن 2.40م × 2.70م (مساحة ≥ 6.48م²)"
    ),
    "corridors": SpaceStandard(
        name_ar="الممرات ومناطق الخدمات",
        name_en="Corridors / services area",
        hex_code="#efde8e",
        rgb=(239, 222, 142),
        category="indoor",
        min_turning_diameter=1.50,
        min_clear_width=1.60,
        description="عرض موزع مركزي لا يقل عن 1.60م مع عقد دوران عند التقاطعات"
    ),
    "doors": SpaceStandard(
        name_ar="فتحات الجدران (الأبواب)",
        name_en="Opening in the walls (Doors)",
        hex_code="#aaabfe",
        rgb=(170, 171, 254),
        category="indoor",
        min_turning_diameter=0.0,
        min_clear_width=1.00,
        description="فتحات أبواب بعرض صافٍ لا يقل عن 1.00م"
    ),
    "walls": SpaceStandard(
        name_ar="الجدران الإنشائية والفاصلة",
        name_en="Structural & Partition Walls",
        hex_code="#000000",
        rgb=(0, 0, 0),
        category="indoor",
        min_turning_diameter=0.0,
        min_clear_width=0.25,
        description="جدران صلبة بسماكة موحدة 25 سم تفصل بين الفضاءات وتحتوي على فتحات الأبواب المهيأة"
    )
}

# Site & Building Regulations
CONSTRAINTS = {
    "MAX_COVERAGE_RATIO": 0.75,          # 65% - 75% Coverage Ratio Band
    "MIN_OUTDOOR_RATIO": 0.25,           # 25% - 35% Outdoor Setback / Garden
    "TURNING_CIRCLE_DIAMETER_MIN": 1.50,  # 60 inches (1525 mm)
    "CORRIDOR_WIDTH_MIN": 1.60,           # Strictly >= 1.60m
    "KITCHEN_CLEARANCE_MIN": 3.50,        # Strictly >= 3.50m
    "DOOR_CLEAR_OPENING_MIN": 1.00,       # Strictly >= 1.00m
    "MAX_RAMP_SLOPE": 1.0 / 12.0,         # 1:12 slope
    "PIXELS_PER_METER_DEFAULT": 23.0
}

ADA_STANDARDS = CONSTRAINTS
