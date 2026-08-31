"""
===================================================================================
ArchAccess AI: Generative Architectural Accessibility & Bioclimatic Design Platform
Developed & Designed by: Dr. Ahmed Louay
Streamlit Cloud Deployment & Web Application Portal
===================================================================================
"""

import os
import sys
import re
import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION - FULL WIDTH EDGE-TO-EDGE
st.set_page_config(
    page_title="ArchAccess AI | منصة التصميم التوليدي والامتثال الحركي",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. STRICT ZERO-MARGIN CSS TO MAXIMIZE CANVAS VIEWPORT
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ELIMINATE ALL STREAMLIT SIDE GUTTERS AND PADDING */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .main {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stElementContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Full-screen Edge-to-Edge Embedded CAD Canvas Viewport */
    iframe {
        width: 100% !important;
        min-width: 100% !important;
        height: 100vh !important;
        min-height: 980px !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
    }
    
    /* Hide Streamlit Header/Footer and Menu */
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
</style>
""", unsafe_allow_html=True)

import time

# 3. HELPER TO BUNDLE WEB APPLICATION (FRESH DIRECT LOAD - NO STALE CACHE)
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
        
    # Inject cache-busting build timestamp
    timestamp = int(time.time())
    html_content = html_content.replace(
        '<head>',
        f'<head>\n    <!-- ArchAccess Build Version: {timestamp} -->'
    )

    # Replace external styles with inlined CSS
    html_content = html_content.replace(
        '<link rel="stylesheet" href="styles.css">',
        f'<style>\n{css_content}\n</style>'
    )
    
    # Replace external scripts with inlined JavaScript
    html_content = re.sub(
        r'<script src="app\.js[^"]*"></script>',
        lambda m: f'<script>\n{js_content}\n</script>',
        html_content
    )
    
    return html_content

# 4. RENDER FULL INTERACTIVE PLATFORM
html_app = get_bundled_html()
components.html(html_app, height=1020, scrolling=True)
