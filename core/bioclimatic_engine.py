"""
ArchAccess AI - Iraq Bioclimatic & Cultural Privacy Engine
==========================================================
Computes solar angles, seasonal sun paths, prevailing winds (Shamal/Sharqi),
shading overhang depths, and Iraqi socio-cultural visual privacy indices.
Developed and Designed by Dr Ahmed Louay
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

@dataclass
class GovernorateClimate:
    name_ar: str
    name_en: str
    latitude: float
    longitude: float
    climate_zone: str
    climate_zone_ar: str
    summer_peak_temp_c: float
    winter_low_temp_c: float
    summer_solar_altitude_deg: float   # June 21 Solar Noon
    winter_solar_altitude_deg: float   # Dec 21 Solar Noon
    prevailing_summer_wind: str       # Northwest (Shamal)
    prevailing_winter_wind: str       # Northwest / Southeast
    relative_humidity_summer_pct: float
    architectural_recommendation_ar: str
    architectural_recommendation_en: str

# Database of Iraqi Governorates with exact coordinates and bioclimatic parameters
IRAQI_GOVERNORATES: Dict[str, GovernorateClimate] = {
    "baghdad": GovernorateClimate(
        name_ar="بغداد (العاصمة)",
        name_en="Baghdad",
        latitude=33.3152,
        longitude=44.3661,
        climate_zone="Hot Arid / Desert",
        climate_zone_ar="صحراوي حار وجاف",
        summer_peak_temp_c=48.5,
        winter_low_temp_c=4.0,
        summer_solar_altitude_deg=80.1,
        winter_solar_altitude_deg=33.2,
        prevailing_summer_wind="الشمالية الغربية (الشمالي)",
        prevailing_winter_wind="الشمالية الغربية والجنوبية الشرقية",
        relative_humidity_summer_pct=22.0,
        architectural_recommendation_ar="كواسر شمس أفقية جنوبية بعمق 0.45م، عزل حراري للجدران، فناء وسطي (حوش) لتوليد تيار تبريدي طبيعي.",
        architectural_recommendation_en="Horizontal southern louvers (0.45m depth), high thermal mass walls, central courtyard for microclimatic stack effect."
    ),
    "basra": GovernorateClimate(
        name_ar="البصرة",
        name_en="Basra",
        latitude=30.5085,
        longitude=47.7835,
        climate_zone="Hot Humid Subtropical",
        climate_zone_ar="حار رطب شبه استوائي",
        summer_peak_temp_c=50.2,
        winter_low_temp_c=6.5,
        summer_solar_altitude_deg=82.9,
        winter_solar_altitude_deg=36.0,
        prevailing_summer_wind="الشمالية الغربية والجنوبية الشرقية (الشرقي)",
        prevailing_winter_wind="الشمالية الغربية",
        relative_humidity_summer_pct=65.0,
        architectural_recommendation_ar="تهوية متقاطعة (Cross-Ventilation) واسعة، شناشيل خشبية مظللة لتقليل الرطوبة وحجب الإشعاع الشمسي الحاد.",
        architectural_recommendation_en="Extensive cross-ventilation, traditional wooden Shanashil screens to buffer high humidity and intense solar gain."
    ),
    "erbil": GovernorateClimate(
        name_ar="أربيل (إقليم كردستان)",
        name_en="Erbil",
        latitude=36.1911,
        longitude=44.0092,
        climate_zone="Semi-Arid / Highland",
        climate_zone_ar="شبه جاف / جبلي معتدل",
        summer_peak_temp_c=42.0,
        winter_low_temp_c=-1.5,
        summer_solar_altitude_deg=77.2,
        winter_solar_altitude_deg=30.3,
        prevailing_summer_wind="الشمالية الشرقية",
        prevailing_winter_wind="الشمالية الغربية الباردة",
        relative_humidity_summer_pct=28.0,
        architectural_recommendation_ar="توجيه الواجهات الرئيسية للجنوب لاكتساب الحرارة الشمسية شتاءً، عزل حراري فائق ومزدوج لمنع فقدان الطاقة.",
        architectural_recommendation_en="Orient main living zones South for direct winter passive solar gain, thick double-glazing and perimeter thermal insulation."
    ),
    "mosul": GovernorateClimate(
        name_ar="الموصل (نينوى)",
        name_en="Mosul",
        latitude=36.3400,
        longitude=43.1300,
        climate_zone="Semi-Arid Mediterranean",
        climate_zone_ar="شبه جاف متوسطي",
        summer_peak_temp_c=43.5,
        winter_low_temp_c=0.5,
        summer_solar_altitude_deg=77.1,
        winter_solar_altitude_deg=30.2,
        prevailing_summer_wind="الشمالية الغربية",
        prevailing_winter_wind="الشمالية الغربية",
        relative_humidity_summer_pct=26.0,
        architectural_recommendation_ar="نوافذ جنوبية متوازنة مع أفاريز متدرجة، كتل بنائية مدمجة للحماية من رياح الشتاء الباردة.",
        architectural_recommendation_en="Balanced southern fenestration with overhangs, compact building envelope to minimize winter exposure."
    ),
    "najaf": GovernorateClimate(
        name_ar="النجف الأشرف",
        name_en="Najaf",
        latitude=32.0000,
        longitude=44.3300,
        climate_zone="Hot Desert",
        climate_zone_ar="صحراوي حار شديد الجفاف",
        summer_peak_temp_c=49.0,
        winter_low_temp_c=5.0,
        summer_solar_altitude_deg=81.4,
        winter_solar_altitude_deg=34.5,
        prevailing_summer_wind="الشمالية الغربية (الشمالي)",
        prevailing_winter_wind="الشمالية الغربية",
        relative_humidity_summer_pct=18.0,
        architectural_recommendation_ar="سرداب / فناء داخلي مظلل (الحوش)، جدران سميكة بكتلة حرارية عالية لامتصاص تباين درجات الحرارة.",
        architectural_recommendation_en="Subterranean/courtyard microclimate (Sardab/Hosh), high thermal mass masonry to smooth diurnal temperature swings."
    ),
    "anbar": GovernorateClimate(
        name_ar="الأنبار (الرمادي)",
        name_en="Anbar / Ramadi",
        latitude=33.4200,
        longitude=43.3000,
        climate_zone="Extreme Continental Desert",
        climate_zone_ar="صحراوي قاري متباين",
        summer_peak_temp_c=48.8,
        winter_low_temp_c=2.0,
        summer_solar_altitude_deg=80.0,
        winter_solar_altitude_deg=33.1,
        prevailing_summer_wind="الشمالية الغربية والغربية",
        prevailing_winter_wind="الشمالية الغربية",
        relative_humidity_summer_pct=20.0,
        architectural_recommendation_ar="مصدات للرياح المغبرة، فتحات معمارية موجهة للداخل، عزل الأسطح والجدران الغربية المعرضة لشمس العصر.",
        architectural_recommendation_en="Dust wind baffles, inward-focused fenestration, heavy roof and west facade thermal barrier against late afternoon sun."
    ),
    "sulaymaniyah": GovernorateClimate(
        name_ar="السليمانية",
        name_en="Sulaymaniyah",
        latitude=35.5600,
        longitude=45.4300,
        climate_zone="Mountainous / Cool Winter",
        climate_zone_ar="جبلي معتدل صيفاً بارد شتاءً",
        summer_peak_temp_c=40.5,
        winter_low_temp_c=-2.0,
        summer_solar_altitude_deg=77.9,
        winter_solar_altitude_deg=30.9,
        prevailing_summer_wind="الشمالية والشمالية الشرقية",
        prevailing_winter_wind="الشمالية",
        relative_humidity_summer_pct=30.0,
        architectural_recommendation_ar="استغلال المنحدرات الطبوغرافية، كسب حراري شمسي مباشر شتوي، زجاج مزدوج Low-E.",
        architectural_recommendation_en="Maximize topography, direct passive winter solar gain, high-performance Low-E double glazing."
    ),
    "karbala": GovernorateClimate(
        name_ar="كربلاء المقدسة",
        name_en="Karbala",
        latitude=32.6160,
        longitude=44.0249,
        climate_zone="Hot Arid / Desert",
        climate_zone_ar="صحراوي حار وجاف",
        summer_peak_temp_c=48.6,
        winter_low_temp_c=4.5,
        summer_solar_altitude_deg=80.8,
        winter_solar_altitude_deg=33.9,
        prevailing_summer_wind="الشمالية الغربية",
        prevailing_winter_wind="الشمالية الغربية",
        relative_humidity_summer_pct=21.0,
        architectural_recommendation_ar="أفاريز تظليل عميقة، ملاقف هواء أو مناور تهوية لتسريع حركة الهواء وتبريد المبنى ليلاً.",
        architectural_recommendation_en="Deep shading eaves, natural stack ventilation shafts for night thermal purging."
    )
}

def calculate_solar_angles(latitude_deg: float, day_of_year: int, hour_solar: float = 12.0) -> Tuple[float, float]:
    lat_rad = math.radians(latitude_deg)
    declination = 23.45 * math.sin(math.radians(360 / 365 * (284 + day_of_year)))
    dec_rad = math.radians(declination)
    hour_angle = (hour_solar - 12.0) * 15.0
    hour_rad = math.radians(hour_angle)
    
    sin_altitude = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(lat_rad) * math.cos(dec_rad) * math.cos(hour_rad)
    altitude_deg = math.degrees(math.asin(max(-1.0, min(1.0, sin_altitude))))
    
    cos_azimuth = (math.sin(altitude_deg * math.pi / 180) * math.sin(lat_rad) - math.sin(dec_rad)) / (
        math.cos(altitude_deg * math.pi / 180) * math.cos(lat_rad) + 1e-6
    )
    azimuth_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_azimuth))))
    if hour_solar < 12.0:
        azimuth_deg = -azimuth_deg
        
    return round(altitude_deg, 1), round(azimuth_deg, 1)

def calculate_optimal_overhang_depth(window_height_m: float, solar_altitude_summer_deg: float) -> float:
    rad = math.radians(solar_altitude_summer_deg)
    tan_val = math.tan(rad)
    if tan_val <= 0.1:
        return 0.50
    depth = window_height_m / tan_val
    return round(depth, 2)

def evaluate_iraqi_privacy_and_climate(
    governorate_key: str,
    north_orientation_deg: float,
    rooms_data: List[Dict[str, Any]]
) -> Dict[str, Any]:
    gov = IRAQI_GOVERNORATES.get(governorate_key, IRAQI_GOVERNORATES["baghdad"])
    summer_alt, _ = calculate_solar_angles(gov.latitude, 172, 12.0)
    winter_alt, _ = calculate_solar_angles(gov.latitude, 355, 12.0)
    overhang_depth = calculate_optimal_overhang_depth(1.20, summer_alt)
    
    has_isolated_guest = any(r.get("key") == "guest_room" for r in rooms_data)
    has_courtyard = any(r.get("key") == "court_garden" for r in rooms_data)
    has_disabled_suite_buffer = any(r.get("key") == "disabled_bedroom" for r in rooms_data)
    
    privacy_score = 98.0 if (has_isolated_guest and has_courtyard and has_disabled_suite_buffer) else 90.0
    wind_alignment_delta = abs(((north_orientation_deg + 45) % 360) - 315)
    wind_cooling_score = round(max(75.0, 100.0 - (wind_alignment_delta * 0.15)), 1)
    
    return {
        "governorate": gov.name_ar,
        "governorate_en": gov.name_en,
        "climate_zone": gov.climate_zone_ar,
        "summer_peak_temp": f"{gov.summer_peak_temp_c}°C",
        "summer_noon_altitude": f"{summer_alt}° (حادة)",
        "winter_noon_altitude": f"{winter_alt}° (مائلة ومخترقة)",
        "overhang_depth_recommended": f"{overhang_depth} متر",
        "prevailing_summer_wind": gov.prevailing_summer_wind,
        "wind_cooling_efficiency": f"{wind_cooling_score}%",
        "visual_privacy_index": f"{privacy_score}% (فصل تام للضيوف وحرمة للجوار)",
        "architectural_recommendation": gov.architectural_recommendation_ar
    }
