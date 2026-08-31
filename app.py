"""
===================================================================================
ArchAccess AI: Generative Architectural Accessibility & Bioclimatic Design Platform
Developed & Designed by: Dr. Ahmed Louay
Streamlit Cloud Deployment & Web Application Portal
===================================================================================
"""

import os
import sys
import json
import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="ArchAccess AI | منصة التصميم التوليدي والامتثال الحركي",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM STREAMLIT STYLING (Zero Margins for Maximum CAD Canvas Area)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    .stApp {
        background-color: #0b1120;
        color: #f8fafc;
    }

    /* ELIMINATE STREAMLIT DEFAULT PADDING & MARGINS */
    .block-container {
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
        max-width: 100% !important;
    }

    .main .block-container {
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
        max-width: 100% !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding: 0 !important;
    }

    /* Streamlit Components IFrame Full Width */
    iframe {
        width: 100% !important;
        min-width: 100% !important;
        border: none !important;
        display: block !important;
    }
    
    /* Header Bar */
    .arch-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 8px;
        padding: 10px 18px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    
    .arch-title {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .arch-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 2px;
    }
    
    .author-badge {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.75rem;
        color: #38bdf8;
        font-weight: 600;
    }
    
    /* Metrics Grid */
    .metric-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 10px 12px;
        text-align: center;
    }
    
    .metric-val {
        font-size: 1.25rem;
        font-weight: 800;
        color: #38bdf8;
    }
    
    .metric-lbl {
        font-size: 0.72rem;
        color: #94a3b8;
    }
    
    /* Hide Streamlit Header/Footer Clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. HELPER TO BUNDLE WEB APPLICATION
@st.cache_data
def get_bundled_html():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(base_dir, "web")
    
    html_path = os.path.join(web_dir, "index.html")
    css_path = os.path.join(web_dir, "styles.css")
    js_path = os.path.join(web_dir, "app.js")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
        
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
        
    # Replace external links with inlined content for 100% self-contained cloud execution
    html_content = html_content.replace(
        '<link rel="stylesheet" href="styles.css">',
        f'<style>\n{css_content}\n</style>'
    )
    
    # Replace script tag using function replacement (safe from backslash escapes in JS)
    import re
    html_content = re.sub(
        r'<script src="app\.js[^"]*"></script>',
        lambda m: f'<script>\n{js_content}\n</script>',
        html_content
    )
    
    return html_content

# 4. SIDEBAR CONTROLS & SCIENTIFIC SPECIFICATIONS
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 14px;">
        <h2 style="color: #38bdf8; font-weight: 800; font-size: 1.3rem; margin: 0;">🏛️ ArchAccess AI</h2>
        <span style="font-size: 0.75rem; color: #94a3b8;">Universal Design & Bioclimatic Engine</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 المؤشرات المعمارية الأساسية")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-val">100%</div>
            <div class="metric-lbl">امتثال AGCR ADA</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-val">65-75%</div>
            <div class="metric-lbl">نسبة التغطية BCR</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 📐 محددات كود البناء والتصميم الشامل")
    st.markdown("""
    - 🚗 **موقف السيارة:** $\\ge 5.0\\text{m} \\times 2.0\\text{m}$ مع خلوص 30 سم ومسار نزول 1.80م.
    - ♿ **منحدر الوصول:** ميل $1:12$ وعرض $\\ge 1.20\\text{m}$ مباشر لصالة المعيشة.
    - 🚪 **الأبواب:** فتحة صافية $\\ge 1.00\\text{m}$ بكتف ركني $\\le 20\\text{cm}$.
    - 🧱 **الجدران:** سماكة موحدة $25\\text{cm}$ (Single 250mm).
    - 🚿 **الحمام المهيأ:** $\\ge 3.0\\text{m} \\times 3.0\\text{m}$ بدوران $\\varnothing 1.50\\text{m}$ وشاور بدون عتبة.
    - 🍳 **المطبخ وغرفة النوم:** $\\ge 3.0\\text{m} \\times 4.0\\text{m}$.
    - 🛋️ **فضاء المعيشة وغرفة الضيوف:** العرض الصافي $\\ge 4.00\\text{m}$.
    - 🌿 **الموزع المركزي:** العرض الصافي $\\ge 1.50\\text{m}$.
    - ☀️ **المناخ العراقي:** محاكاة حركة الشمس، الرياح السائدة ($315^\\circ\\text{ NW}$)، وعزل غرفة الضيوف $100\\%$.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; font-size: 0.75rem; color: #64748b; line-height: 1.5;">
        Developed and Designed by<br>
        <strong style="color: #38bdf8; font-size: 0.85rem;">Dr Ahmed Louay</strong><br>
        ArchAccess AI Research & Universal Design
    </div>
    """, unsafe_allow_html=True)

# 5. MAIN PAGE RENDERER
st.markdown("""
<div class="arch-header">
    <div>
        <h1 class="arch-title">🏛️ ArchAccess AI — منصة التصميم التوليدي والامتثال الحركي</h1>
        <div class="arch-subtitle">توليد المخططات المعمارية السكنية التكيفية وفق معايير الوصول الشامل (ADA) والمحددات المناخية العراقية</div>
    </div>
    <div class="author-badge">
        👨‍🏫 Developed by Dr Ahmed Louay
    </div>
</div>
""", unsafe_allow_html=True)

# Render Full Interactive Self-Contained Platform
html_app = get_bundled_html()
components.html(html_app, height=1050, scrolling=True)
