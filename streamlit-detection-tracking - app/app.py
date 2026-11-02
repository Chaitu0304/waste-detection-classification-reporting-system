import sys
import os
from pathlib import Path
import PIL
import pandas as pd
import streamlit as st

# Setup sys.path to resolve local and root modules seamlessly
_app_dir = Path(__file__).resolve().parent
_root_dir = _app_dir.parent
for _p in [str(_app_dir), str(_root_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import settings
import helper
import email_service

try:
    import generate_report
except ImportError:
    generate_report = None

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WasteAI | Smart Waste Intelligence Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL + CUSTOM UI STYLING (CREATIVE CYBER-COMMAND SYSTEM)
# ============================================================

st.markdown("""
<style>
    /* CSS Keyframes & Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 12px rgba(16, 185, 129, 0.25), inset 0 0 12px rgba(16, 185, 129, 0.1); }
        50% { box-shadow: 0 0 24px rgba(16, 185, 129, 0.55), inset 0 0 18px rgba(16, 185, 129, 0.25); }
    }

    @keyframes floatHero {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(0.5deg); }
    }

    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(1000%); }
    }

    /* Remove Streamlit Header Defaults */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    /* Global Canvas Styling */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a251b 0%, #030a08 60%, #010403 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #f1f5f9;
        animation: fadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .main .block-container {
        max-width: 1540px;
        padding-top: 1.2rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        padding-bottom: 4rem !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background-color: #04120c;
        border-right: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Top Brand Header Lockup */
    .wa-top-brand {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 46px;
    }

    .wa-top-brand-name {
        color: #ffffff;
        font-size: 26px;
        font-weight: 900;
        line-height: 1.0;
        letter-spacing: -0.8px;
        text-shadow: 0 0 16px rgba(16, 185, 129, 0.4);
    }

    .wa-top-brand-subtitle {
        color: #34d399;
        font-size: 9.5px;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-top: 3px;
    }

    /* ========================================================
       CREATIVE INTERACTIVE BUTTON STYLING
       ======================================================== */

    .stButton > button,
    .stButton > button[kind="secondary"] {
        height: 44px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        background: rgba(6, 26, 18, 0.7) !important;
        color: #e2e8f0 !important;
        font-size: 13.5px !important;
        font-weight: 800 !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stButton > button:hover,
    .stButton > button[kind="secondary"]:hover {
        background: rgba(16, 185, 129, 0.2) !important;
        border-color: #34d399 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid #34d399 !important;
        color: #022c22 !important;
        font-size: 14px !important;
        font-weight: 900 !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.35) !important;
        animation: pulseGlow 3s infinite ease-in-out;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 28px rgba(16, 185, 129, 0.55) !important;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        height: 44px !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 13.5px !important;
        border: 1px solid #34d399 !important;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #022c22 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.25s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 26px rgba(16, 185, 129, 0.5) !important;
    }

    /* Top Divider */
    .wa-top-divider {
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, rgba(16,185,129,0) 0%, rgba(52,211,153,0.4) 50%, rgba(16,185,129,0) 100%);
        margin-top: 14px;
        margin-bottom: 28px;
    }

    /* Creative Translucent Cards */
    .ui-card {
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .ui-card:hover {
        border-color: rgba(52, 211, 153, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 14px 36px rgba(16, 185, 129, 0.15);
    }

    /* Status Badges */
    .ui-badge-ready {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 20px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #34d399;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 0.5px;
    }

    .ui-badge-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        display: inline-block;
        box-shadow: 0 0 10px #10b981;
    }

    /* KPI Display Cards */
    .kpi-card {
        background: rgba(6, 22, 16, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 18px;
        padding: 22px 24px;
        min-height: 125px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: #34d399;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
    }

    .kpi-label {
        color: #94a3b8;
        font-size: 10.5px;
        font-weight: 850;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 900;
        margin-top: 6px;
        letter-spacing: -0.8px;
        text-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
    }

    .kpi-meta {
        color: #34d399;
        font-size: 11px;
        margin-top: 6px;
        font-weight: 700;
    }

    /* Page Banner Headers */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 26px 32px;
        margin-bottom: 28px;
        backdrop-filter: blur(14px);
    }

    .page-eyebrow {
        color: #34d399;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .page-title {
        color: #ffffff;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: -0.8px;
        margin: 0;
    }

    .page-description {
        color: #94a3b8;
        font-size: 13.5px;
        margin-top: 6px;
    }

    /* Environmental Impact Card Widget */
    .impact-widget {
        background: linear-gradient(135deg, rgba(6, 30, 20, 0.8) 0%, rgba(2, 14, 9, 0.9) 100%);
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 20px;
        padding: 24px;
        margin-top: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .impact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .impact-metric {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }

    .impact-val {
        font-size: 24px;
        font-weight: 900;
        color: #34d399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
    }

    .impact-lbl {
        font-size: 10.5px;
        color: #cbd5e1;
        font-weight: 800;
        text-transform: uppercase;
        margin-top: 3px;
    }

    /* Image Frame Cards */
    .image-frame-card {
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 18px;
        padding: 18px;
    }

    .image-frame-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }

    .image-frame-title {
        font-size: 14.5px;
        font-weight: 850;
        color: #ffffff;
    }

    .image-frame-meta {
        font-size: 11px;
        font-weight: 750;
        color: #34d399;
        background: rgba(16, 185, 129, 0.15);
        padding: 5px 10px;
        border-radius: 8px;
    }

    /* Upload Box Container */
    .upload-box-container {
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(14px);
    }

    .upload-tip-card {
        background: rgba(2, 14, 9, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 14px;
        padding: 16px 18px;
        height: 100%;
        transition: all 0.3s ease;
    }

    .upload-tip-card:hover {
        border-color: #34d399;
        transform: translateY(-2px);
    }

    .upload-tip-title {
        font-size: 13px;
        font-weight: 850;
        color: #ffffff;
    }

    .upload-tip-text {
        font-size: 11.5px;
        color: #94a3b8;
        margin-top: 5px;
        line-height: 1.55;
    }

    /* Activity Stream Rows */
    .activity-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px 18px;
        border-radius: 12px;
        background: rgba(2, 14, 9, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 10px;
        transition: all 0.25s ease;
    }

    .activity-row:hover {
        transform: translateX(4px);
        border-color: #34d399;
        background: rgba(16, 185, 129, 0.1);
    }

    .activity-row strong {
        color: #ffffff;
        font-size: 13.5px;
        font-weight: 850;
    }

    .activity-row span {
        color: #94a3b8;
        font-size: 11.5px;
    }

    .activity-confidence {
        color: #34d399;
        font-size: 12.5px;
        font-weight: 850;
    }

    /* Home Hero Block */
    .home-hero {
        position: relative;
        padding: 56px 60px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 36px;
        border-radius: 26px;
        background: radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.3) 0%, rgba(3, 14, 9, 0.95) 100%);
        border: 1px solid rgba(52, 211, 153, 0.4);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
    }

    .home-hero-content {
        max-width: 700px;
    }

    .home-badge {
        display: inline-block;
        padding: 6px 14px;
        margin-bottom: 20px;
        border-radius: 20px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #34d399;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1px;
    }

    .home-hero h1 {
        margin: 0;
        font-size: 52px;
        line-height: 1.07;
        letter-spacing: -1.8px;
        font-weight: 900;
        color: #ffffff;
    }

    .home-hero h1 span {
        color: #34d399;
        text-shadow: 0 0 20px rgba(52, 211, 153, 0.5);
    }

    .home-hero p {
        max-width: 630px;
        margin-top: 20px;
        font-size: 16.5px;
        line-height: 1.7;
        color: #cbd5e1;
    }

    .home-visual-card {
        width: 330px;
        padding: 30px 32px;
        border-radius: 22px;
        background: rgba(4, 18, 12, 0.85);
        border: 1px solid rgba(52, 211, 153, 0.4);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.7);
        animation: floatHero 4s ease-in-out infinite;
    }

    .visual-badge {
        font-size: 10.5px;
        font-weight: 900;
        color: #34d399;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .visual-title {
        font-size: 21px;
        font-weight: 850;
        color: #ffffff;
    }

    .visual-status {
        margin-top: 10px;
        font-size: 12.5px;
        font-weight: 750;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .visual-stats {
        display: flex;
        gap: 18px;
        margin-top: 26px;
        padding-top: 20px;
        border-top: 1px solid rgba(16, 185, 129, 0.2);
    }

    .visual-stats div {
        flex: 1;
    }

    .visual-stats strong {
        display: block;
        font-size: 21px;
        font-weight: 900;
        color: #ffffff;
    }

    .visual-stats small {
        color: #34d399;
        font-size: 10px;
        text-transform: uppercase;
        font-weight: 800;
    }

    .home-feature-card {
        min-height: 140px;
        padding: 28px 26px;
        border-radius: 18px;
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.25);
        transition: all 0.3s ease;
    }

    .home-feature-card:hover {
        transform: translateY(-4px);
        border-color: #34d399;
        box-shadow: 0 10px 28px rgba(16, 185, 129, 0.15);
    }

    .home-feature-card h3 {
        margin: 0;
        color: #ffffff;
        font-size: 18px;
        font-weight: 850;
    }

    .home-feature-card p {
        margin-top: 10px;
        color: #94a3b8;
        font-size: 13.5px;
        line-height: 1.65;
    }

    .home-input-card {
        min-height: 125px;
        padding: 24px;
        background: rgba(6, 22, 16, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 18px;
        transition: all 0.3s ease;
    }

    .home-input-card:hover {
        transform: translateY(-4px);
        border-color: #34d399;
        box-shadow: 0 10px 28px rgba(16, 185, 129, 0.15);
    }

    .home-input-card strong {
        display: block;
        font-size: 15.5px;
        color: #ffffff;
        font-weight: 850;
    }

    .home-input-card p {
        margin-top: 7px;
        font-size: 12.5px;
        line-height: 1.6;
        color: #94a3b8;
    }

    /* Streamlit Input Labels Overrides */
    .stSelectbox label, .stSlider label, .stRadio label {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(6, 26, 18, 0.8) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
        color: #ffffff !important;
    }

    @media (max-width: 900px) {
        .home-hero {
            flex-direction: column;
            padding: 34px;
        }
        .home-visual-card {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP NAVIGATION
# ============================================================

pages = [
    "Home",
    "Dashboard",
    "Detection",
    "Analytics",
    "Settings"
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

nav_columns = st.columns([2.3, 1, 1, 1, 1, 1])

# Brand Lockup
with nav_columns[0]:
    st.html("""
    <div class="wa-top-brand">
        <div class="wa-top-brand-name">WasteAI</div>
        <div class="wa-top-brand-subtitle">Smart Waste Intelligence</div>
    </div>
    """)

# Navigation buttons with active state highlighting
for i, page_name in enumerate(pages):
    with nav_columns[i + 1]:
        is_active = (st.session_state.page == page_name)
        button_type = "primary" if is_active else "secondary"
        if st.button(
            page_name,
            key=f"top_nav_{page_name.lower()}",
            type=button_type,
            use_container_width=True
        ):
            st.session_state.page = page_name
            st.rerun()

st.html("<div class='wa-top-divider'></div>")

page = st.session_state.page

# ============================================================
# LOAD MODEL
# ============================================================

model_path = Path(settings.DETECTION_MODEL)

try:
    model = helper.load_model(model_path)
    st.sidebar.caption(f"Model: `{model_path.name}`")
except Exception as ex:
    model = None
    st.error(f"Unable to load model: {model_path}")
    st.error(ex)

# ============================================================
# PAGE: HOME
# ============================================================

if page == "Home":

    # Hero Banner
    st.html("""
    <div class="home-hero">
        <div class="home-hero-content">
            <div class="home-badge">
                WASTEAI &bull; AI-POWERED WASTE INTELLIGENCE
            </div>
            <h1>
                Smarter Waste.<br>
                <span>Cleaner Future.</span>
            </h1>
            <p>
                WasteAI uses advanced computer vision to automatically detect,
                classify, and analyze waste across images, recorded video,
                and live video feeds with industry-leading precision.
            </p>
        </div>

        <div class="home-visual-card">
            <div class="visual-badge">SYSTEM STATUS</div>
            <div class="visual-title">AI Waste Detection</div>
            <div class="visual-status">
                <span class="ui-badge-dot"></span>
                YOLOv8 Engine Ready
            </div>
            <div class="visual-stats">
                <div>
                    <strong>6+</strong>
                    <small>Classes</small>
                </div>
                <div>
                    <strong>4</strong>
                    <small>Sources</small>
                </div>
                <div>
                    <strong>AI</strong>
                    <small>YOLOv8</small>
                </div>
            </div>
        </div>
    </div>
    """)

    hero_col1, hero_col2 = st.columns(2)
    with hero_col1:
        if st.button("Start Waste Detection", type="primary", use_container_width=True, key="home_btn_detect"):
            st.session_state.page = "Detection"
            st.rerun()
    with hero_col2:
        if st.button("View Dashboard", type="secondary", use_container_width=True, key="home_btn_dash"):
            st.session_state.page = "Dashboard"
            st.rerun()

    # Capabilities
    st.html("""
    <div class="section-head">
        <div class="page-eyebrow">WHAT WASTEAI DOES</div>
        <div class="section-head-title">Intelligent waste analysis in one unified platform</div>
        <div class="section-head-subtitle">Detect waste materials, categorize recyclables, and produce instant reports.</div>
    </div>
    """)

    f_col1, f_col2, f_col3 = st.columns(3)
    features = [
        ("Detect Waste", "Identify waste objects automatically with precise bounding boxes and confidence metrics using YOLOv8."),
        ("Classify Materials", "Distinguish between key waste categories including plastic, cardboard, glass, metal, paper, and organics."),
        ("Generate Reports", "Instantly aggregate detection metrics, review category breakdowns, export CSV/PDF files, and notify administrators.")
    ]

    for col, (title, desc) in zip([f_col1, f_col2, f_col3], features):
        with col:
            st.html(f"""
            <div class="home-feature-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """)

    # Input Channels
    st.html("""
    <div class="section-head" style="margin-top: 40px;">
        <div class="page-eyebrow">DETECTION CHANNELS</div>
        <div class="section-head-title">Analyze waste from multiple input streams</div>
        <div class="section-head-subtitle">Support for static imagery and real-time continuous video analysis.</div>
    </div>
    """)

    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    sources = [
        ("Images", "Upload and analyze high-resolution photos in JPG, PNG, and WEBP formats."),
        ("Videos", "Scan recorded video clips frame by frame with object detection."),
        ("Live Webcam", "Connect standard local webcams for real-time edge processing."),
        ("Live Streams", "Process continuous network RTSP cameras and streaming URLs.")
    ]

    for col, (title, desc) in zip([s_col1, s_col2, s_col3, s_col4], sources):
        with col:
            st.html(f"""
            <div class="home-input-card">
                <strong>{title}</strong>
                <p>{desc}</p>
            </div>
            """)

    # Technology Banner
    st.html("""
    <div style="background: radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.25) 0%, rgba(5, 20, 14, 0.9) 100%); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 22px; padding: 40px 46px; margin-top: 44px; color: #ffffff; display: flex; justify-content: space-between; align-items: center; gap: 26px; box-shadow: 0 14px 35px rgba(0,0,0,0.5);">
        <div>
            <div style="color: #34d399; font-size: 11.5px; font-weight: 900; letter-spacing: 1.4px;">POWERED BY COMPUTER VISION</div>
            <div style="font-size: 26px; font-weight: 900; margin-top: 6px;">Built with YOLOv8 for Production Waste Classification</div>
            <p style="color: #cbd5e1; font-size: 14.5px; margin-top: 8px; max-width: 680px;">
                WasteAI runs optimized deep neural network weights for high frame rates, accurate multi-object detection, and comprehensive sorting classification.
            </p>
        </div>
        <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(52,211,153,0.3); border-radius: 16px; padding: 22px 28px; text-align: center; min-width: 190px; backdrop-filter: blur(8px);">
            <div style="font-size: 25px; font-weight: 900;">YOLOv8</div>
            <div style="color: #34d399; font-size: 11px; font-weight: 800; margin-top: 3px;">Inference Engine</div>
            <div style="color: #a7f3d0; font-size: 11px; font-weight: 850; margin-top: 12px;">System Ready</div>
        </div>
    </div>
    """)

# ============================================================
# PAGE: DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.html("""
    <div class="page-header">
        <div>
            <div class="page-eyebrow">WASTEAI &bull; SYSTEM OVERVIEW</div>
            <h1 class="page-title">Dashboard</h1>
            <div class="page-description">Real-time operational status, key metrics, and recent detection logs.</div>
        </div>
        <div class="ui-badge-ready">
            <span class="ui-badge-dot"></span>
            System Online
        </div>
    </div>
    """)

    total_detections = 0
    total_items = 0
    avg_confidence = 0.0
    top_category = "--"

    if "detection_stats" in st.session_state and st.session_state["detection_stats"]:
        stats = st.session_state["detection_stats"]
        total_detections = st.session_state.get("total_runs", 1)
        total_items = sum(item["count"] for item in stats.values())
        conf_sum = sum(item["conf_sum"] for item in stats.values())
        avg_confidence = (conf_sum / total_items * 100) if total_items > 0 else 0.0
        top_category = max(stats.items(), key=lambda x: x[1]["count"])[0]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL INFERENCES</div>
            <div class="kpi-value">{total_detections:,}</div>
            <div class="kpi-meta">Recorded sessions</div>
        </div>
        """)
    with k2:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">ITEMS IDENTIFIED</div>
            <div class="kpi-value">{total_items:,}</div>
            <div class="kpi-meta">Waste objects logged</div>
        </div>
        """)
    with k3:
        conf_display = f"{avg_confidence:.1f}%" if avg_confidence > 0 else "--"
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">AVG CONFIDENCE</div>
            <div class="kpi-value">{conf_display}</div>
            <div class="kpi-meta">Model prediction score</div>
        </div>
        """)
    with k4:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">TOP CATEGORY</div>
            <div class="kpi-value" style="font-size: 22px;">{top_category}</div>
            <div class="kpi-meta">Most frequent classification</div>
        </div>
        """)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns([1.6, 1])

    with d_col1:
        st.html("""
        <div class="ui-card" style="min-height: 280px;">
            <div style="font-size: 16.5px; font-weight: 850; color: #ffffff;">Recent Detection Activity</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 3px; margin-bottom: 18px;">Latest classifications from active sessions</div>
        """)

        history = st.session_state.get("detection_history", [])
        if history:
            for item in history[-5:][::-1]:
                st.html(f"""
                <div class="activity-row">
                    <div>
                        <strong>{item.get('category', 'Waste Item')}</strong>
                        <span style="display: block; margin-top: 2px;">{item.get('source', 'Image')} &bull; {item.get('count', 1)} item(s)</span>
                    </div>
                    <div class="activity-confidence">{item.get('confidence', '90%')}</div>
                </div>
                """)
        else:
            st.html("""
            <div style="text-align: center; padding: 50px 10px; color: #94a3b8;">
                <div style="font-size: 14.5px; font-weight: 850; color: #cbd5e1;">No Detection Activity Yet</div>
                <div style="font-size: 12px; margin-top: 5px;">Run a detection session to populate live telemetry.</div>
            </div>
            """)

        st.html("</div>")

    with d_col2:
        st.html("""
        <div class="ui-card" style="min-height: 280px;">
            <div style="font-size: 16.5px; font-weight: 850; color: #ffffff;">AI Subsystems Status</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 3px; margin-bottom: 18px;">Core infrastructure readiness</div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(16, 185, 129, 0.2);">
                <div>
                    <strong style="color: #ffffff; font-size: 13.5px; display: block; font-weight: 850;">YOLOv8 Engine</strong>
                    <small style="color: #94a3b8; font-size: 11px;">Weights loaded and ready</small>
                </div>
                <span class="ui-badge-ready">Ready</span>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(16, 185, 129, 0.2);">
                <div>
                    <strong style="color: #ffffff; font-size: 13.5px; display: block; font-weight: 850;">Telemetry Aggregator</strong>
                    <small style="color: #94a3b8; font-size: 11px;">In-memory session buffer</small>
                </div>
                <span class="ui-badge-ready">Active</span>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 0;">
                <div>
                    <strong style="color: #ffffff; font-size: 13.5px; display: block; font-weight: 850;">Report Dispatcher</strong>
                    <small style="color: #94a3b8; font-size: 11px;">CSV & PDF dispatch service</small>
                </div>
                <span class="ui-badge-ready">Standby</span>
            </div>
        </div>
        """)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    qa1, qa2 = st.columns(2)
    with qa1:
        if st.button("Launch Detection", type="primary", use_container_width=True, key="dash_launch_det"):
            st.session_state.page = "Detection"
            st.rerun()
    with qa2:
        if st.button("View Detection & Reports", type="secondary", use_container_width=True, key="dash_open_reports"):
            st.session_state.page = "Detection"
            st.rerun()

# ============================================================
# PAGE: DETECTION
# ============================================================

elif page == "Detection":

    st.html("""
    <div class="page-header">
        <div>
            <div class="page-eyebrow">WASTEAI &bull; COMPUTER VISION ENGINE</div>
            <h1 class="page-title">Waste Detection</h1>
            <div class="page-description">Run object detection and multi-class classification on photos, video, and streams.</div>
        </div>
        <div class="ui-badge-ready">
            <span class="ui-badge-dot"></span>
            YOLOv8 Ready
        </div>
    </div>
    """)

    st.html("""
    <div class="section-head" style="margin-top: 0;">
        <div class="section-head-title">Select Detection Input Source</div>
        <div class="section-head-subtitle">Choose the data channel for the AI to analyze.</div>
    </div>
    """)

    source_radio = st.selectbox(
        "Detection Source",
        settings.SOURCES_LIST,
        key="detection_source",
        label_visibility="collapsed"
    )

    # IMAGE SOURCE INGESTION
    if source_radio == settings.IMAGE:

        st.html("""
        <div class="upload-box-container">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
                <div>
                    <div style="font-size: 18px; font-weight: 900; color: #ffffff;">Upload Waste Image</div>
                    <div style="font-size: 13.5px; color: #94a3b8; margin-top: 4px;">
                        Upload photos to automatically locate, classify, and analyze waste objects with YOLOv8.
                    </div>
                </div>
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 10px; padding: 8px 16px; font-size: 11.5px; font-weight: 850; color: #34d399;">
                    JPG &bull; JPEG &bull; PNG &bull; BMP &bull; WEBP (Max 200MB)
                </div>
            </div>
        </div>
        """)

        upload_method = st.radio(
            "How would you like to add an image?",
            options=("Browse files", "Use camera"),
            horizontal=True,
            key="detection_upload_method"
        )

        if upload_method == "Use camera":
            st.caption("Take a photo of the waste item using your device camera.")
            source_img = st.camera_input("Capture waste image", key="detection_camera_input")
            if source_img is None:
                st.info("Allow camera access when prompted. If unavailable, select Browse files instead.")
        else:
            st.caption("Choose an existing JPG, JPEG, PNG, BMP, or WEBP image.")
            source_img = st.file_uploader(
                "Choose a waste image to analyze",
                type=("jpg", "jpeg", "png", "bmp", "webp"),
                label_visibility="collapsed",
                key="detection_image_uploader"
            )

        if source_img is None:
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            tip1, tip2, tip3 = st.columns(3)
            with tip1:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Framing & Focus</div>
                    <div class="upload-tip-text">Capture waste objects clearly within the image boundary with minimal obstruction.</div>
                </div>
                """)
            with tip2:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Lighting & Contrast</div>
                    <div class="upload-tip-text">Well-lit indoor or outdoor lighting ensures high classification confidence.</div>
                </div>
                """)
            with tip3:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Multi-Object Detection</div>
                    <div class="upload-tip-text">YOLOv8 detects multiple separated or clustered waste items in a single scan.</div>
                </div>
                """)

        else:
            uploaded_image = PIL.Image.open(source_img)
            img_width, img_height = uploaded_image.size
            img_format = uploaded_image.format or "JPEG"
            file_size_kb = round(len(source_img.getvalue()) / 1024, 1)

            current_image_key = f"{source_img.name}_{file_size_kb}"
            if st.session_state.get("active_image_key") != current_image_key:
                st.session_state["active_image_key"] = current_image_key
                st.session_state["has_run_detection"] = False
                st.session_state["current_boxes"] = None
                st.session_state["current_annotated"] = None

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            st.html(f"""
            <div class="ui-card" style="padding: 22px 26px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <div style="font-size: 16.5px; font-weight: 900; color: #ffffff;">Analysis Workspace</div>
                        <div style="font-size: 12.5px; color: #94a3b8; margin-top: 3px;">
                            Configure detection threshold and execute inference.
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <span class="ui-badge-ready">Model: YOLOv8</span>
                        <span class="ui-badge-ready">File: {source_img.name} ({img_width}x{img_height}px, {file_size_kb} KB)</span>
                    </div>
                </div>
            </div>
            """)

            cfg_col, action_col = st.columns([2.2, 1], gap="medium")
            with cfg_col:
                confidence_percent = st.slider(
                    "Confidence Threshold",
                    min_value=5,
                    max_value=100,
                    value=10,
                    step=5,
                    key="image_conf_slider",
                    help="Adjust confidence cutoff score."
                )
                confidence = confidence_percent / 100.0
                st.caption(f"Current Threshold: **{confidence_percent}%** ({confidence:.2f})")

            with action_col:
                st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                run_detect_clicked = st.button("Detect Waste", type="primary", use_container_width=True, key="btn_execute_detection")

            if run_detect_clicked:
                if model is None:
                    st.error("The YOLO model could not be loaded. Check settings.DETECTION_MODEL.")
                else:
                    with st.spinner("AI is analyzing waste objects in the image..."):
                        res = model.predict(uploaded_image, conf=confidence)

                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]

                    stats = {}
                    detected_items = []
                    for idx, box in enumerate(boxes):
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf_score = float(box.conf[0])

                        if class_name not in stats:
                            stats[class_name] = {"count": 0, "conf_sum": 0.0}

                        stats[class_name]["count"] += 1
                        stats[class_name]["conf_sum"] += conf_score

                        dest_type = "Organic / Wet Compost" if class_name == "BIODEGRADABLE" else "Recyclable (Dry Waste)"
                        detected_items.append({
                            "Item_ID": f"ITEM-{idx+1:02d}",
                            "Category": class_name,
                            "Confidence": round(conf_score, 2),
                            "Type": dest_type
                        })

                    st.session_state["has_run_detection"] = True
                    st.session_state["current_annotated"] = res_plotted
                    st.session_state["detection_stats"] = stats
                    st.session_state["detected_items"] = detected_items
                    st.session_state["last_uploaded_name"] = source_img.name

                    if stats:
                        total_items = sum(item["count"] for item in stats.values())
                        unique_categories = len(stats)
                        dominant_category = max(stats.items(), key=lambda x: x[1]["count"])[0]

                        table_data = []
                        for category, data in stats.items():
                            avg_conf = (data["conf_sum"] / data["count"]) * 100
                            pct = (data["count"] / total_items) * 100
                            table_data.append({
                                "Waste Category": category,
                                "Quantity": data["count"],
                                "Share": f"{pct:.1f}%",
                                "Avg Confidence": f"{avg_conf:.1f}%"
                            })

                        st.session_state["detection_table"] = table_data
                        st.session_state["total_items"] = total_items
                        st.session_state["unique_categories"] = unique_categories
                        st.session_state["dominant_category"] = dominant_category
                        st.session_state["total_runs"] = st.session_state.get("total_runs", 0) + 1

                        if "detection_history" not in st.session_state:
                            st.session_state["detection_history"] = []

                        avg_run_conf = (sum(item["conf_sum"] for item in stats.values()) / total_items) * 100
                        st.session_state["detection_history"].append({
                            "category": dominant_category,
                            "source": "Image Upload",
                            "count": total_items,
                            "confidence": f"{avg_run_conf:.1f}%"
                        })

                        if generate_report is not None:
                            try:
                                res_dir = Path("results")
                                res_dir.mkdir(parents=True, exist_ok=True)
                                pdf_p, _ = generate_report.generate_user_waste_report(
                                    detected_items=detected_items,
                                    image_name=source_img.name,
                                    output_folder=str(res_dir)
                                )
                                if pdf_p.exists():
                                    st.session_state["last_pdf_path"] = str(pdf_p)
                            except Exception as pe:
                                print(f"[Notice] PDF auto-generation: {pe}")

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            col_orig, col_proc = st.columns(2, gap="medium")

            with col_orig:
                st.html(f"""
                <div class="image-frame-card">
                    <div class="image-frame-header">
                        <span class="image-frame-title">A. Original Source Image</span>
                        <span class="image-frame-meta">{img_width} x {img_height} px &bull; {img_format}</span>
                    </div>
                </div>
                """)
                st.image(uploaded_image, use_container_width=True)

            with col_proc:
                has_results = st.session_state.get("has_run_detection", False)
                if has_results and st.session_state.get("current_annotated") is not None:
                    st.html("""
                    <div class="image-frame-card">
                        <div class="image-frame-header">
                            <span class="image-frame-title">B. YOLOv8 Detection Results</span>
                            <span class="ui-badge-ready">Inference Complete</span>
                        </div>
                    </div>
                    """)
                    st.image(st.session_state["current_annotated"], use_container_width=True)
                else:
                    st.html("""
                    <div class="image-frame-card" style="height: 100%; min-height: 320px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: rgba(6, 24, 16, 0.4);">
                        <div style="font-size: 15.5px; font-weight: 850; color: #ffffff;">Detection Output Awaiting Run</div>
                        <div style="font-size: 12px; color: #94a3b8; margin-top: 5px; max-width: 330px;">
                            Click the <strong style="color: #34d399;">Detect Waste</strong> button above to run inference and render bounding boxes.
                        </div>
                    </div>
                    """)

            if st.session_state.get("has_run_detection", False) and st.session_state.get("detection_stats"):
                stats = st.session_state["detection_stats"]
                total_items = st.session_state.get("total_items", sum(item["count"] for item in stats.values()))
                unique_categories = st.session_state.get("unique_categories", len(stats))
                dominant_category = st.session_state.get("dominant_category", max(stats.items(), key=lambda x: x[1]["count"])[0])
                total_conf = sum(item["conf_sum"] for item in stats.values())
                avg_confidence = (total_conf / total_items) * 100 if total_items > 0 else 0.0

                st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
                st.html("""
                <div class="section-head">
                    <div class="page-eyebrow">DETECTION METRICS</div>
                    <div class="section-head-title">C. Detection Summary</div>
                    <div class="section-head-subtitle">Aggregated values returned by the YOLOv8 model for this image.</div>
                </div>
                """)

                sc1, sc2, sc3, sc4 = st.columns(4)
                with sc1:
                    st.html(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">TOTAL WASTE ITEMS</div>
                        <div class="kpi-value">{total_items}</div>
                        <div class="kpi-meta">Objects detected</div>
                    </div>
                    """)
                with sc2:
                    st.html(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">CATEGORIES IDENTIFIED</div>
                        <div class="kpi-value">{unique_categories}</div>
                        <div class="kpi-meta">Distinct material classes</div>
                    </div>
                    """)
                with sc3:
                    st.html(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">DOMINANT CATEGORY</div>
                        <div class="kpi-value" style="font-size: 21px;">{dominant_category}</div>
                        <div class="kpi-meta">Highest object count</div>
                    </div>
                    """)
                with sc4:
                    st.html(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">AVERAGE CONFIDENCE</div>
                        <div class="kpi-value">{avg_confidence:.1f}%</div>
                        <div class="kpi-meta">Overall detection score</div>
                    </div>
                    """)

                # Environmental Impact Widget
                co2_saved = round(total_items * 0.42, 2)
                water_saved = round(total_items * 1.8, 1)
                energy_saved = round(total_items * 0.15, 2)

                st.html(f"""
                <div class="impact-widget">
                    <div style="font-size: 11px; font-weight: 900; color: #34d399; letter-spacing: 1.3px; text-transform: uppercase;">ENVIRONMENTAL IMPACT CALCULATOR</div>
                    <div style="font-size: 18px; font-weight: 850; color: #ffffff; margin-top: 4px;">Estimated Offset from Recognized Recyclables</div>
                    <div class="impact-grid">
                        <div class="impact-metric">
                            <div class="impact-val">-{co2_saved} kg</div>
                            <div class="impact-lbl">Est. CO₂ Offset</div>
                        </div>
                        <div class="impact-metric">
                            <div class="impact-val">{water_saved} L</div>
                            <div class="impact-lbl">Water Preserved</div>
                        </div>
                        <div class="impact-metric">
                            <div class="impact-val">{energy_saved} kWh</div>
                            <div class="impact-lbl">Energy Saved</div>
                        </div>
                    </div>
                </div>
                """)

                st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
                st.html("""
                <div class="section-head">
                    <div class="page-eyebrow">AUTOMATIC REPORT</div>
                    <div class="section-head-title">E. Detection Report</div>
                    <div class="section-head-subtitle">This report is generated automatically from the latest YOLO detection.</div>
                </div>
                """)

                report_data = []
                for category, data in stats.items():
                    cat_count = data["count"]
                    avg_conf = (data["conf_sum"] / cat_count) * 100 if cat_count else 0
                    share = (cat_count / total_items) * 100 if total_items else 0
                    report_data.append({
                        "Waste Category": category,
                        "Quantity": cat_count,
                        "Percentage": f"{share:.1f}%",
                        "Average Confidence": f"{avg_conf:.1f}%"
                    })
                report_df = pd.DataFrame(report_data)
                st.dataframe(report_df, use_container_width=True, hide_index=True)

                report_csv = report_df.to_csv(index=False).encode("utf-8")
                pdf_path = st.session_state.get("last_pdf_path")
                pdf_bytes = None
                if pdf_path and Path(pdf_path).exists():
                    try:
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                    except OSError as pdf_error:
                        st.warning(f"The PDF report could not be opened: {pdf_error}")

                if not pdf_bytes and generate_report is not None:
                    try:
                        results_dir = Path("results")
                        results_dir.mkdir(parents=True, exist_ok=True)
                        generated_pdf, _ = generate_report.generate_user_waste_report(
                            detected_items=st.session_state.get("detected_items", []),
                            image_name=st.session_state.get("last_uploaded_name", "waste_detection.jpg"),
                            output_folder=str(results_dir)
                        )
                        if generated_pdf and Path(generated_pdf).exists():
                            pdf_path = str(generated_pdf)
                            st.session_state["last_pdf_path"] = pdf_path
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                    except Exception as report_error:
                        st.warning(f"PDF report generation failed: {report_error}")

                report_actions = st.columns(4 if pdf_bytes else 3)
                with report_actions[0]:
                    st.download_button(
                        "Download CSV Report", data=report_csv,
                        file_name="waste_detection_report.csv", mime="text/csv",
                        use_container_width=True, key="detection_download_csv_btn"
                    )
                if pdf_bytes:
                    with report_actions[1]:
                        st.download_button(
                            "Download PDF Report", data=pdf_bytes,
                            file_name=Path(pdf_path).name if pdf_path else "waste_detection_report.pdf",
                            mime="application/pdf", use_container_width=True,
                            key="detection_download_pdf_btn"
                        )
                    email_column = report_actions[2]
                    analytics_column = report_actions[3]
                else:
                    email_column = report_actions[1]
                    analytics_column = report_actions[2]
                    st.caption("PDF report is not available right now; the CSV report is ready to download.")

                with email_column:
                    send_email_clicked = st.button(
                        "Send Report to Admin", type="primary",
                        use_container_width=True, key="detection_email_report_btn"
                    )
                with analytics_column:
                    if st.button(
                        "View Detailed Analytics", type="secondary",
                        use_container_width=True, key="det_act_analytics"
                    ):
                        st.session_state.page = "Analytics"
                        st.rerun()

                if send_email_clicked:
                    with st.spinner("Sending the detection report to the administrator..."):
                        summary_metrics = {
                            "total_items": total_items,
                            "unique_categories": unique_categories,
                            "dominant_category": dominant_category
                        }
                        success, message = email_service.send_waste_report_email(
                            report_df=report_df,
                            report_csv=report_csv,
                            pdf_path=pdf_path,
                            summary_metrics=summary_metrics,
                            image_name=st.session_state.get("last_uploaded_name", "waste_detection.jpg")
                        )
                    if success:
                        st.success(message)
                        st.toast("Report sent to administrator.")
                    else:
                        st.error(message)

    # VIDEO / STREAMING SOURCES
    elif source_radio == settings.VIDEO:
        st.html("""
        <div class="ui-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <strong style="color: #ffffff; font-size: 15.5px; font-weight: 850;">Video Detection</strong>
            <span style="display: block; font-size: 12px; color: #94a3b8; margin-top: 3px;">Scan recorded video frame by frame using YOLOv8.</span>
        </div>
        """)
        helper.play_stored_video(0.10, model)

    elif source_radio == settings.WEBCAM:
        st.html("""
        <div class="ui-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <strong style="color: #ffffff; font-size: 15.5px; font-weight: 850;">Live Webcam Detection</strong>
            <span style="display: block; font-size: 12px; color: #94a3b8; margin-top: 3px;">Use connected camera for real-time edge waste detection.</span>
        </div>
        """)
        helper.play_webcam(0.10, model)

    elif source_radio == settings.YOUTUBE:
        st.html("""
        <div class="ui-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <strong style="color: #ffffff; font-size: 15.5px; font-weight: 850;">YouTube Stream Detection</strong>
            <span style="display: block; font-size: 12px; color: #94a3b8; margin-top: 3px;">Analyze waste video directly from a public YouTube stream.</span>
        </div>
        """)
        helper.play_youtube_video(0.10, model)

    elif source_radio == settings.RTSP:
        st.html("""
        <div class="ui-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <strong style="color: #ffffff; font-size: 15.5px; font-weight: 850;">RTSP Camera Stream</strong>
            <span style="display: block; font-size: 12px; color: #94a3b8; margin-top: 3px;">Connect continuous RTSP IP camera feed for automated surveillance.</span>
        </div>
        """)
        helper.play_rtsp_stream(0.10, model)

# ============================================================
# PAGE: ANALYTICS
# ============================================================

elif page == "Analytics":

    st.html("""
    <div class="page-header">
        <div>
            <div class="page-eyebrow">WASTEAI &bull; INTELLIGENCE CENTER</div>
            <h1 class="page-title">Waste Analytics</h1>
            <div class="page-description">Visual distributions, material proportions, and model performance metrics.</div>
        </div>
        <div class="ui-badge-ready">
            <span class="ui-badge-dot"></span>
            Analytics Active
        </div>
    </div>
    """)

    has_live_data = ("detection_stats" in st.session_state and st.session_state["detection_stats"])

    if not has_live_data:
        st.html("""
        <div style="background: rgba(6, 26, 18, 0.7); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 16px; padding: 18px 22px; margin-bottom: 22px;">
            <div style="font-size: 13.5px; font-weight: 850; color: #34d399;">Sample Preview Analytics</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 3px;">
                No active detection has been performed in this session yet. Showing baseline distribution preview below.
            </div>
        </div>
        """)
        stats = {
            "PLASTIC": {"count": 5, "conf_sum": 4.65},
            "CARDBOARD": {"count": 3, "conf_sum": 2.67},
            "GLASS": {"count": 2, "conf_sum": 1.82},
            "METAL": {"count": 2, "conf_sum": 1.78},
            "BIODEGRADABLE": {"count": 4, "conf_sum": 3.52},
            "PAPER": {"count": 2, "conf_sum": 1.62}
        }
    else:
        stats = st.session_state["detection_stats"]

    total_items = sum(item["count"] for item in stats.values())
    unique_categories = len(stats)
    dominant_category = max(stats.items(), key=lambda x: x[1]["count"])[0]
    total_conf = sum(item["conf_sum"] for item in stats.values())
    average_confidence = (total_conf / total_items) * 100 if total_items > 0 else 0.0
    dominant_count = stats[dominant_category]["count"]
    dominant_percentage = (dominant_count / total_items) * 100 if total_items > 0 else 0.0

    st.html("""
    <div class="section-head" style="margin-top: 0;">
        <div class="section-head-title">Detection Overview</div>
        <div class="section-head-subtitle">Summary metrics of classified waste items.</div>
    </div>
    """)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL WASTE</div>
            <div class="kpi-value">{total_items}</div>
            <div class="kpi-meta">Objects detected</div>
        </div>
        """)
    with k2:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">CATEGORIES</div>
            <div class="kpi-value">{unique_categories}</div>
            <div class="kpi-meta">Waste types identified</div>
        </div>
        """)
    with k3:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">AVG CONFIDENCE</div>
            <div class="kpi-value">{average_confidence:.1f}%</div>
            <div class="kpi-meta">Model prediction score</div>
        </div>
        """)
    with k4:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">DOMINANT WASTE</div>
            <div class="kpi-value" style="font-size: 21px;">{dominant_category}</div>
            <div class="kpi-meta">{dominant_percentage:.1f}% of total items</div>
        </div>
        """)

    st.html("""
    <div class="section-head" style="margin-top: 28px;">
        <div class="section-head-title">Waste Category Distribution</div>
        <div class="section-head-subtitle">Volume breakdown and material dominance.</div>
    </div>
    """)

    chart_df = pd.DataFrame({
        "Waste Category": list(stats.keys()),
        "Quantity": [item["count"] for item in stats.values()]
    })

    c_col1, c_col2 = st.columns([1.7, 1], gap="medium")
    with c_col1:
        st.html("""
        <div class="ui-card" style="padding: 22px 24px 14px;">
            <div style="font-size: 16.5px; font-weight: 850; color: #ffffff;">Category Distribution</div>
            <div style="font-size: 11.5px; color: #94a3b8; margin-top: 3px; margin-bottom: 16px;">Count of identified items per class</div>
        """)
        st.bar_chart(chart_df.set_index("Waste Category"), use_container_width=True)
        st.html("</div>")

    with c_col2:
        st.html(f"""
        <div style="background: radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.3) 0%, rgba(4, 18, 12, 0.95) 100%); border: 1px solid rgba(52, 211, 153, 0.4); border-radius: 18px; padding: 28px; min-height: 320px; color: #ffffff; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="color: #34d399; font-size: 10.5px; font-weight: 900; letter-spacing: 1.3px;">AI GENERATED INSIGHT</div>
            <div style="font-size: 18px; font-weight: 850; margin-top: 14px;">Dominant Material</div>
            <div style="font-size: 29px; font-weight: 900; margin-top: 4px; color: #a7f3d0;">{dominant_category}</div>
            <div style="height: 1px; background: rgba(16, 185, 129, 0.2); margin: 20px 0;"></div>
            <div style="color: #cbd5e1; font-size: 11.5px;">This category accounts for</div>
            <div style="font-size: 35px; font-weight: 900; margin-top: 2px;">{dominant_percentage:.1f}%</div>
            <div style="color: #cbd5e1; font-size: 11.5px;">of all detected waste ({dominant_count} items).</div>
            <div style="color: #34d399; font-size: 11.5px; font-weight: 700; margin-top: 20px;">Targeted recycling sorting recommended for this stream.</div>
        </div>
        """)

    st.html("""
    <div class="section-head" style="margin-top: 28px;">
        <div class="section-head-title">Detailed Category Analysis</div>
        <div class="section-head-subtitle">Granular breakdown by individual material category.</div>
    </div>
    """)

    table_data = []
    for cat, data in stats.items():
        cat_conf = (data["conf_sum"] / data["count"]) * 100
        cat_pct = (data["count"] / total_items) * 100
        table_data.append({
            "Waste Category": cat,
            "Quantity": data["count"],
            "Share": f"{cat_pct:.1f}%",
            "Avg Confidence": f"{cat_conf:.1f}%"
        })

    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

# ============================================================
# PAGE: SETTINGS
# ============================================================

elif page == "Settings":

    st.html("""
    <div class="page-header">
        <div>
            <div class="page-eyebrow">WASTEAI &bull; SYSTEM CONFIGURATION</div>
            <h1 class="page-title">Configuration Center</h1>
            <div class="page-description">Inspect AI model parameters, tracking algorithms, and supported category definitions.</div>
        </div>
        <div class="ui-badge-ready">
            <span class="ui-badge-dot"></span>
            System Ready
        </div>
    </div>
    """)

    st.markdown("### AI Model Configuration")

    mc1, mc2 = st.columns(2)
    with mc1:
        st.html("""
        <div class="ui-card" style="min-height: 115px;">
            <div class="kpi-label">DETECTION MODEL</div>
            <div style="font-size: 22px; font-weight: 900; color: #ffffff; margin-top: 4px;">YOLOv8</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 3px;">Computer vision architecture</div>
        </div>
        """)

    with mc2:
        st.html("""
        <div class="ui-card" style="min-height: 115px;">
            <div class="kpi-label">MODEL STATUS</div>
            <div style="font-size: 22px; font-weight: 900; color: #34d399; margin-top: 4px;">Ready</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 3px;">Weights loaded in memory</div>
        </div>
        """)

    st.html(f"""
    <div style="background: rgba(6, 26, 18, 0.7); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 16px; padding: 16px 20px; margin-top: 14px; margin-bottom: 28px; font-size: 12.5px; color: #94a3b8;">
        <strong style="color: #ffffff;">Active Model Weights Path:</strong> {settings.DETECTION_MODEL}
    </div>
    """)

    st.markdown("### Detection Configuration")

    dc1, dc2 = st.columns(2)
    with dc1:
        st.html("""
        <div class="ui-card" style="padding: 20px 24px; margin-bottom: 14px;">
            <div style="font-size: 14.5px; font-weight: 850; color: #ffffff;">Default Confidence Threshold</div>
            <div style="font-size: 11.5px; color: #94a3b8; margin-top: 3px;">Base cutoff score for valid object detection</div>
        </div>
        """)

        settings_confidence = st.slider(
            "Default Confidence Threshold",
            min_value=5,
            max_value=100,
            value=10,
            step=5,
            help="Controls minimum confidence score."
        )
        st.caption(f"Default threshold: **{settings_confidence}%**")

    with dc2:
        st.html("""
        <div class="ui-card" style="padding: 20px 24px; margin-bottom: 14px;">
            <div style="font-size: 14.5px; font-weight: 850; color: #ffffff;">Object Tracking</div>
            <div style="font-size: 11.5px; color: #94a3b8; margin-top: 3px;">Track object instances across consecutive video frames</div>
        </div>
        """)

        enable_tracking = st.toggle(
            "Enable Object Tracking",
            value=False,
            help="Track detected items across video frames."
        )

        if enable_tracking:
            tracker_type = st.selectbox("Tracking Algorithm", ["bytetrack.yaml", "botsort.yaml"])
            st.success(f"Tracking active: {tracker_type}")

    st.markdown("### Supported Waste Categories")
    categories = [
        ("CARDBOARD", "Dry clean cardboard and packing boxes"),
        ("GLASS", "Glass bottles, jars, and containers"),
        ("METAL", "Beverage cans, tin food cans, and scrap metals"),
        ("PAPER", "Clean office paper, newspapers, and flyers"),
        ("PLASTIC", "Bottles, food packaging, and rigid plastics"),
        ("BIODEGRADABLE", "Organic waste, food scraps, and compostables")
    ]

    cat_cols = st.columns(3)
    for i, (cat_name, cat_desc) in enumerate(categories):
        with cat_cols[i % 3]:
            st.html(f"""
            <div class="ui-card" style="padding: 20px; margin-bottom: 16px; min-height: 95px;">
                <div style="font-size: 13.5px; font-weight: 900; color: #ffffff;">{cat_name}</div>
                <div style="font-size: 11.5px; color: #94a3b8; margin-top: 4px; line-height: 1.55;">{cat_desc}</div>
            </div>
            """)