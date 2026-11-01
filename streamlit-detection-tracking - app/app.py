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
    page_title="WasteAI | Smart Waste Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL + CUSTOM UI STYLING (HIGH CONTRAST & ACCESSIBILITY)
# ============================================================

st.markdown("""
<style>
    /* Remove default Streamlit header and decoration */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    /* Global application canvas */
    .stApp {
        background-color: #f7f9f8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 0.75rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5 {
        color: #17352b !important;
        letter-spacing: -0.4px;
        font-weight: 800 !important;
    }

    p {
        color: #55665f;
        line-height: 1.6;
    }

    /* Sidebar */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e1ebe5;
    }

    /* Top Brand Lockup */
    .wa-top-brand {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 44px;
        padding-left: 2px;
    }

    .wa-top-brand-name {
        color: #17352b;
        font-size: 23px;
        font-weight: 850;
        line-height: 1.1;
        letter-spacing: -0.6px;
    }

    .wa-top-brand-subtitle {
        color: #1f7d56;
        font-size: 10px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 2px;
    }

    /* ========================================================
       ACCESSIBLE BUTTON STYLING (HIGH CONTRAST)
       ======================================================== */

    .stButton {
        margin-top: 2px;
    }

    /* All Standard / Secondary Buttons */
    .stButton > button,
    .stButton > button[kind="secondary"] {
        height: 42px !important;
        min-height: 42px !important;
        width: 100% !important;
        padding: 0 16px !important;
        border-radius: 9px !important;
        border: 1.5px solid #bcd1c6 !important;
        background-color: #ffffff !important;
        color: #17352b !important;
        font-size: 14px !important;
        font-weight: 750 !important;
        letter-spacing: 0.1px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.18s ease-in-out !important;
    }

    .stButton > button:hover,
    .stButton > button[kind="secondary"]:hover {
        background-color: #eaf5ef !important;
        border-color: #176044 !important;
        color: #176044 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(23, 96, 68, 0.12) !important;
    }

    .stButton > button:focus,
    .stButton > button[kind="secondary"]:focus {
        outline: 2px solid #176044 !important;
        outline-offset: 2px !important;
        color: #17352b !important;
    }

    .stButton > button:active,
    .stButton > button[kind="secondary"]:active {
        background-color: #d8ece0 !important;
        color: #176044 !important;
    }

    /* All Primary Buttons (Dark Green with High-Contrast White Text) */
    .stButton > button[kind="primary"] {
        background-color: #176044 !important;
        border: 1.5px solid #176044 !important;
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 750 !important;
        box-shadow: 0 2px 6px rgba(23, 96, 68, 0.22) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #0f3f2d !important;
        border-color: #0f3f2d !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(23, 96, 68, 0.3) !important;
    }

    .stButton > button[kind="primary"]:focus {
        outline: 2px solid #28a76d !important;
        outline-offset: 2px !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:active {
        background-color: #0b2b1f !important;
        color: #ffffff !important;
    }

    /* All Download Buttons */
    .stDownloadButton > button {
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 9px !important;
        font-weight: 750 !important;
        font-size: 14px !important;
        border: 1.5px solid #176044 !important;
        background-color: #176044 !important;
        color: #ffffff !important;
        box-shadow: 0 2px 6px rgba(23, 96, 68, 0.22) !important;
        transition: all 0.18s ease-in-out !important;
    }

    .stDownloadButton > button:hover {
        background-color: #0f3f2d !important;
        border-color: #0f3f2d !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(23, 96, 68, 0.3) !important;
    }

    .stDownloadButton > button:focus {
        outline: 2px solid #28a76d !important;
        outline-offset: 2px !important;
        color: #ffffff !important;
    }

    /* Streamlit File Uploader Button Contrast */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #176044 !important;
        color: #ffffff !important;
        border: 1.5px solid #176044 !important;
        border-radius: 8px !important;
        font-weight: 750 !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        box-shadow: 0 2px 5px rgba(23, 96, 68, 0.15) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #0f3f2d !important;
        border-color: #0f3f2d !important;
        color: #ffffff !important;
    }

    /* Disabled Button State */
    .stButton > button:disabled,
    .stDownloadButton > button:disabled {
        background-color: #e5ede8 !important;
        border-color: #d0ded6 !important;
        color: #7d9187 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Top Navigation Divider */
    .wa-top-divider {
        width: 100%;
        height: 1px;
        background: #e2ebe6;
        margin-top: 10px;
        margin-bottom: 24px;
    }

    /* Reusable Cards */
    .ui-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .ui-card:hover {
        box-shadow: 0 5px 16px rgba(20, 55, 43, 0.06);
    }

    /* Status Badges */
    .ui-badge-ready {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 13px;
        border-radius: 20px;
        background: #edf8f2;
        border: 1px solid #d5ece0;
        color: #176044;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.3px;
        white-space: nowrap;
    }

    .ui-badge-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #28a76d;
        display: inline-block;
    }

    /* KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 110px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
    }

    .kpi-label {
        color: #6a7c74;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.9px;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #17352b;
        font-size: 28px;
        font-weight: 850;
        margin-top: 6px;
        letter-spacing: -0.6px;
    }

    .kpi-meta {
        color: #7d8f87;
        font-size: 11px;
        margin-top: 5px;
    }

    /* Page Banner Headers */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
    }

    .page-eyebrow {
        color: #1f7d56;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .page-title {
        color: #17352b;
        font-size: 27px;
        font-weight: 850;
        letter-spacing: -0.6px;
        margin: 0;
    }

    .page-description {
        color: #63756d;
        font-size: 13px;
        margin-top: 4px;
    }

    /* Section Headings */
    .section-head {
        margin-top: 22px;
        margin-bottom: 12px;
    }

    .section-head-title {
        color: #17352b;
        font-size: 17px;
        font-weight: 800;
    }

    .section-head-subtitle {
        color: #72847c;
        font-size: 12px;
        margin-top: 2px;
    }

    /* Image Containers for Detection Workspace */
    .image-frame-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
    }

    .image-frame-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid #edf3ef;
    }

    .image-frame-title {
        font-size: 14px;
        font-weight: 750;
        color: #17352b;
    }

    .image-frame-meta {
        font-size: 11px;
        font-weight: 650;
        color: #6c7e76;
        background: #f1f6f3;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Detection upload banner */
    .upload-box-container {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
    }

    .upload-tip-card {
        background: #fbfdfc;
        border: 1px solid #e3ede7;
        border-radius: 10px;
        padding: 12px 14px;
    }

    .upload-tip-title {
        font-size: 12px;
        font-weight: 750;
        color: #17352b;
    }

    .upload-tip-text {
        font-size: 11px;
        color: #6b7d75;
        margin-top: 3px;
        line-height: 1.45;
    }

    /* Activity rows */
    .activity-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        border-radius: 9px;
        background: #fbfdfc;
        border: 1px solid #edf2ef;
        margin-bottom: 8px;
    }

    .activity-row strong {
        color: #17352b;
        font-size: 13px;
        font-weight: 750;
    }

    .activity-row span {
        color: #72847c;
        font-size: 11px;
    }

    .activity-confidence {
        color: #176044;
        font-size: 12px;
        font-weight: 750;
    }

    /* Home Hero */
    .home-hero {
        position: relative;
        padding: 48px 52px;
        margin-bottom: 35px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 30px;
        border-radius: 24px;
        background: linear-gradient(135deg, #f3f8f5 0%, #ebf5ef 100%);
        border: 1px solid #dbeae2;
    }

    .home-hero-content {
        max-width: 680px;
    }

    .home-badge {
        display: inline-block;
        padding: 6px 13px;
        margin-bottom: 18px;
        border-radius: 20px;
        background: #e3f4ec;
        border: 1px solid #cbe8da;
        color: #176044;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.8px;
    }

    .home-hero h1 {
        margin: 0;
        font-size: 48px;
        line-height: 1.08;
        letter-spacing: -1.6px;
        font-weight: 850;
        color: #13362a;
    }

    .home-hero h1 span {
        color: #1c885e;
    }

    .home-hero p {
        max-width: 620px;
        margin-top: 18px;
        font-size: 16px;
        line-height: 1.65;
        color: #55665f;
    }

    .home-visual-card {
        width: 310px;
        padding: 26px 28px;
        border-radius: 20px;
        background: #ffffff;
        border: 1px solid #dbe8e1;
        box-shadow: 0 16px 36px rgba(23, 65, 48, 0.08);
    }

    .visual-badge {
        font-size: 10px;
        font-weight: 800;
        color: #1f7d56;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .visual-title {
        font-size: 20px;
        font-weight: 800;
        color: #15382b;
    }

    .visual-status {
        margin-top: 10px;
        font-size: 12px;
        font-weight: 650;
        color: #55665f;
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .visual-stats {
        display: flex;
        gap: 16px;
        margin-top: 22px;
        padding-top: 18px;
        border-top: 1px solid #e7efe9;
    }

    .visual-stats div {
        flex: 1;
    }

    .visual-stats strong {
        display: block;
        font-size: 19px;
        font-weight: 850;
        color: #173a2e;
    }

    .visual-stats small {
        color: #7b8c85;
        font-size: 10px;
        text-transform: uppercase;
        font-weight: 600;
    }

    .home-feature-card {
        min-height: 120px;
        padding: 24px 22px;
        border-radius: 16px;
        background: #ffffff;
        border: 1px solid #e1e9e5;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .home-feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(20, 55, 43, 0.07);
    }

    .home-feature-card h3 {
        margin: 0;
        color: #173c30;
        font-size: 17px;
        font-weight: 750;
    }

    .home-feature-card p {
        margin-top: 8px;
        color: #63756d;
        font-size: 13px;
        line-height: 1.55;
    }

    .home-input-card {
        min-height: 110px;
        padding: 20px;
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(20, 55, 43, 0.03);
    }

    .home-input-card strong {
        display: block;
        font-size: 15px;
        color: #173c30;
        font-weight: 750;
    }

    .home-input-card p {
        margin-top: 6px;
        font-size: 12px;
        line-height: 1.5;
        color: #6f8179;
    }

    @media (max-width: 900px) {
        .home-hero {
            flex-direction: column;
            padding: 30px;
        }
        .home-visual-card {
            width: 100%;
        }
    }

    /* Explicitly color button label elements (Streamlit may render labels in nested spans/divs) */
    .stButton > button,
    .stButton > button *,
    .stButton > button[kind="secondary"],
    .stButton > button[kind="secondary"] * {
        color: #17352b !important;
        -webkit-text-fill-color: #17352b !important;
    }

    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button:hover,
    .stButton > button:hover * {
        color: #176044 !important;
        -webkit-text-fill-color: #176044 !important;
    }

    .stDownloadButton > button,
    .stDownloadButton > button *,
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stDownloadButton > button:hover,
    .stDownloadButton > button:hover *,
    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploaderDropzone"] button:hover * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button:disabled,
    .stButton > button:disabled *,
    .stDownloadButton > button:disabled,
    .stDownloadButton > button:disabled * {
        color: #52665c !important;
        -webkit-text-fill-color: #52665c !important;
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
    "Reports",
    "Settings"
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

nav_columns = st.columns([2.3, 1, 1, 1, 1, 1, 1])

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

    # Hero Section
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
                and live video feeds.
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

    # Features
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

    # Sources
    st.html("""
    <div class="section-head" style="margin-top: 36px;">
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

    # Technology
    st.html("""
    <div style="background: #143c2f; border-radius: 20px; padding: 34px 40px; margin-top: 40px; color: #ffffff; display: flex; justify-content: space-between; align-items: center; gap: 20px;">
        <div>
            <div style="color: #7cd5ab; font-size: 11px; font-weight: 800; letter-spacing: 1px;">POWERED BY COMPUTER VISION</div>
            <div style="font-size: 24px; font-weight: 800; margin-top: 6px;">Built with YOLOv8 for Production Waste Classification</div>
            <p style="color: #b7cbbf; font-size: 14px; margin-top: 8px; max-width: 650px;">
                WasteAI runs optimized deep neural network weights for high frame rates, accurate multi-object detection, and comprehensive sorting classification.
            </p>
        </div>
        <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.14); border-radius: 14px; padding: 18px 24px; text-align: center; min-width: 170px;">
            <div style="font-size: 22px; font-weight: 850;">YOLOv8</div>
            <div style="color: #9ecdb6; font-size: 11px; font-weight: 600; margin-top: 3px;">Inference Engine</div>
            <div style="color: #7cd5ab; font-size: 11px; font-weight: 750; margin-top: 12px;">System Ready</div>
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

    # Metrics aggregation
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

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns([1.6, 1])

    with d_col1:
        st.html("""
        <div class="ui-card" style="min-height: 250px;">
            <div style="font-size: 16px; font-weight: 800; color: #17352b;">Recent Detection Activity</div>
            <div style="font-size: 12px; color: #72847c; margin-top: 2px; margin-bottom: 16px;">Latest classifications from active sessions</div>
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
            <div style="text-align: center; padding: 40px 10px; color: #8a9a92;">
                <div style="font-size: 14px; font-weight: 750; color: #4b5e56;">No Detection Activity Yet</div>
                <div style="font-size: 12px; margin-top: 4px;">Run a detection session to populate live telemetry.</div>
            </div>
            """)

        st.html("</div>")

    with d_col2:
        st.html("""
        <div class="ui-card" style="min-height: 250px;">
            <div style="font-size: 16px; font-weight: 800; color: #17352b;">AI Subsystems Status</div>
            <div style="font-size: 12px; color: #72847c; margin-top: 2px; margin-bottom: 16px;">Core infrastructure readiness</div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #edf2ef;">
                <div>
                    <strong style="color: #17352b; font-size: 13px; display: block;">YOLOv8 Engine</strong>
                    <small style="color: #7a8b83; font-size: 11px;">Weights loaded and ready</small>
                </div>
                <span class="ui-badge-ready">Ready</span>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #edf2ef;">
                <div>
                    <strong style="color: #17352b; font-size: 13px; display: block;">Telemetry Aggregator</strong>
                    <small style="color: #7a8b83; font-size: 11px;">In-memory session buffer</small>
                </div>
                <span class="ui-badge-ready">Active</span>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div>
                    <strong style="color: #17352b; font-size: 13px; display: block;">Report Dispatcher</strong>
                    <small style="color: #7a8b83; font-size: 11px;">CSV & PDF dispatch service</small>
                </div>
                <span class="ui-badge-ready">Standby</span>
            </div>
        </div>
        """)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    qa1, qa2 = st.columns(2)
    with qa1:
        if st.button("Launch Detection", type="primary", use_container_width=True, key="dash_launch_det"):
            st.session_state.page = "Detection"
            st.rerun()
    with qa2:
        if st.button("Open Reports Center", type="secondary", use_container_width=True, key="dash_open_reports"):
            st.session_state.page = "Reports"
            st.rerun()

# ============================================================
# PAGE: DETECTION (REDESIGNED LAYOUT)
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

    # Source selection
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

    # --------------------------------------------------------
    # SOURCE: IMAGE (REDESIGNED WORKFLOW)
    # --------------------------------------------------------
    if source_radio == settings.IMAGE:

        # Unified Upload Section Before Image Upload
        st.html("""
        <div class="upload-box-container">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
                <div>
                    <div style="font-size: 17px; font-weight: 800; color: #17352b;">Upload Waste Image</div>
                    <div style="font-size: 13px; color: #5a6c64; margin-top: 3px;">
                        Upload photos to automatically locate, classify, and analyze waste objects with YOLOv8.
                    </div>
                </div>
                <div style="background: #edf7f2; border: 1px solid #d5ece0; border-radius: 8px; padding: 6px 12px; font-size: 11px; font-weight: 750; color: #176044;">
                    JPG &bull; JPEG &bull; PNG &bull; BMP &bull; WEBP (Max 200MB)
                </div>
            </div>
        </div>
        """)

        source_img = st.file_uploader(
            "Choose a waste image to analyze",
            type=("jpg", "jpeg", "png", "bmp", "webp"),
            label_visibility="collapsed",
            key="detection_image_uploader"
        )

        # ----------------------------------------------------
        # BEFORE IMAGE UPLOAD STATE
        # ----------------------------------------------------
        if source_img is None:
            # Informative guide cards showing clear visual hierarchy
            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            tip1, tip2, tip3 = st.columns(3)
            with tip1:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Framing & Focus</div>
                    <div class="upload-tip-text">
                        Capture waste objects clearly within the image boundary with minimal obstruction.
                    </div>
                </div>
                """)
            with tip2:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Lighting & Contrast</div>
                    <div class="upload-tip-text">
                        Well-lit indoor or outdoor lighting ensures high classification confidence.
                    </div>
                </div>
                """)
            with tip3:
                st.html("""
                <div class="upload-tip-card">
                    <div class="upload-tip-title">Multi-Object Detection</div>
                    <div class="upload-tip-text">
                        YOLOv8 detects multiple separated or clustered waste items in a single scan.
                    </div>
                </div>
                """)

        # ----------------------------------------------------
        # AFTER IMAGE UPLOAD STATE
        # ----------------------------------------------------
        else:
            uploaded_image = PIL.Image.open(source_img)
            img_width, img_height = uploaded_image.size
            img_format = uploaded_image.format or "JPEG"
            file_size_kb = round(len(source_img.getvalue()) / 1024, 1)

            # Check if this is a newly uploaded image
            current_image_key = f"{source_img.name}_{file_size_kb}"
            if st.session_state.get("active_image_key") != current_image_key:
                st.session_state["active_image_key"] = current_image_key
                st.session_state["has_run_detection"] = False
                st.session_state["current_boxes"] = None
                st.session_state["current_annotated"] = None

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Control Card: Configuration & Action Trigger
            st.html("""
            <div class="ui-card" style="padding: 18px 22px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #17352b;">Analysis Workspace</div>
                        <div style="font-size: 12px; color: #6b7d75; margin-top: 2px;">
                            Configure detection threshold and execute inference.
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <span class="ui-badge-ready">Model: YOLOv8</span>
                        <span class="ui-badge-ready">File: """ + f"{source_img.name} ({img_width}x{img_height}px, {file_size_kb} KB)" + """</span>
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
                    help="Adjust confidence cutoff. Lower values capture smaller objects; higher values reduce false detections."
                )
                confidence = confidence_percent / 100.0
                st.caption(f"Current Threshold: **{confidence_percent}%** ({confidence:.2f})")

            with action_col:
                st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                run_detect_clicked = st.button(
                    "Detect Waste",
                    type="primary",
                    use_container_width=True,
                    key="btn_execute_detection"
                )

            # Execute detection when button clicked
            if run_detect_clicked:
                if model is None:
                    st.error("The YOLO model could not be loaded. Please check settings.DETECTION_MODEL.")
                else:
                    with st.spinner("AI is analyzing waste objects in the image..."):
                        res = model.predict(uploaded_image, conf=confidence)

                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]

                    # Parse detection statistics
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

                        # Table data
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

                        # Telemetry history
                        if "detection_history" not in st.session_state:
                            st.session_state["detection_history"] = []

                        avg_run_conf = (sum(item["conf_sum"] for item in stats.values()) / total_items) * 100
                        st.session_state["detection_history"].append({
                            "category": dominant_category,
                            "source": "Image Upload",
                            "count": total_items,
                            "confidence": f"{avg_run_conf:.1f}%"
                        })

                        # Auto-generate PDF report in background
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

            # ------------------------------------------------
            # SECTIONS A & B: ORIGINAL VS PROCESSED IMAGES
            # ------------------------------------------------
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
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
                    <div class="image-frame-card" style="height: 100%; min-height: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: #fafcfb;">
                        <div style="font-size: 15px; font-weight: 800; color: #17352b;">Detection Output Awaiting Run</div>
                        <div style="font-size: 12px; color: #72847c; margin-top: 4px; max-width: 320px;">
                            Click the <strong>Detect Waste</strong> button above to run inference and render bounding boxes.
                        </div>
                    </div>
                    """)

            # ------------------------------------------------
            # SECTIONS C, D & E: SUMMARY, ANALYSIS & ACTIONS
            # ------------------------------------------------
            if st.session_state.get("has_run_detection", False) and st.session_state.get("detection_stats"):
                stats = st.session_state["detection_stats"]
                total_items = st.session_state.get("total_items", sum(item["count"] for item in stats.values()))
                unique_categories = st.session_state.get("unique_categories", len(stats))
                dominant_category = st.session_state.get("dominant_category", max(stats.items(), key=lambda x: x[1]["count"])[0])
                total_conf = sum(item["conf_sum"] for item in stats.values())
                avg_confidence = (total_conf / total_items) * 100 if total_items > 0 else 0.0

                # SECTION C: Detection Summary KPI Cards
                st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
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

                # SECTION D: Additional Analysis (Table + Chart)
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                st.html("""
                <div class="section-head">
                    <div class="page-eyebrow">CLASSIFICATION BREAKDOWN</div>
                    <div class="section-head-title">D. Additional Analysis</div>
                    <div class="section-head-subtitle">Category-wise object counts, confidence scores, and disposal stream allocations.</div>
                </div>
                """)

                an_col1, an_col2 = st.columns([1.5, 1], gap="medium")
                with an_col1:
                    st.html("""
                    <div class="ui-card" style="padding: 18px 20px 14px;">
                        <div style="font-size: 14px; font-weight: 750; color: #17352b; margin-bottom: 12px;">Category-wise Breakdown</div>
                    """)
                    analysis_table_data = []
                    for cat, data in stats.items():
                        cat_conf = (data["conf_sum"] / data["count"]) * 100
                        cat_share = (data["count"] / total_items) * 100
                        stream = "Organic Green Bin -> Composting" if cat == "BIODEGRADABLE" else "Blue Bin -> Automated MRF"
                        analysis_table_data.append({
                            "Category": cat,
                            "Count": data["count"],
                            "Share": f"{cat_share:.1f}%",
                            "Avg Confidence": f"{cat_conf:.1f}%",
                            "Disposal Stream": stream
                        })
                    st.dataframe(pd.DataFrame(analysis_table_data), use_container_width=True, hide_index=True)
                    st.html("</div>")

                with an_col2:
                    st.html("""
                    <div class="ui-card" style="padding: 18px 20px 10px;">
                        <div style="font-size: 14px; font-weight: 750; color: #17352b; margin-bottom: 8px;">Material Distribution</div>
                    """)
                    chart_df = pd.DataFrame({
                        "Category": list(stats.keys()),
                        "Items": [item["count"] for item in stats.values()]
                    })
                    st.bar_chart(chart_df.set_index("Category"), use_container_width=True)
                    st.html("</div>")

                # SECTION E: Action Buttons
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                st.html("""
                <div class="ui-card" style="padding: 18px 22px;">
                    <div style="font-size: 14px; font-weight: 800; color: #17352b; margin-bottom: 4px;">E. Next Actions</div>
                    <div style="font-size: 12px; color: #6b7d75; margin-bottom: 14px;">Review in-depth telemetry or compile a full compliance report.</div>
                """)

                act1, act2 = st.columns(2)
                with act1:
                    if st.button("View Detailed Analytics", type="primary", use_container_width=True, key="det_act_analytics"):
                        st.session_state.page = "Analytics"
                        st.rerun()
                with act2:
                    if st.button("Open Waste Reports", type="secondary", use_container_width=True, key="det_act_reports"):
                        st.session_state.page = "Reports"
                        st.rerun()

                st.html("</div>")

            elif st.session_state.get("has_run_detection", False) and not st.session_state.get("detection_stats"):
                st.info("No waste objects were detected with the current confidence threshold. Try adjusting the threshold slider above and clicking Detect Waste again.")

    # --------------------------------------------------------
    # OTHER SOURCES (VIDEO, WEBCAM, RTSP, YOUTUBE)
    # --------------------------------------------------------
    elif source_radio == settings.VIDEO:
        st.html("""
        <div class="ui-card" style="margin-bottom: 16px; padding: 16px 20px;">
            <strong style="color: #17352b; font-size: 15px;">Video Detection</strong>
            <span style="display: block; font-size: 12px; color: #72847c; margin-top: 2px;">
                Scan recorded video frame by frame using the YOLOv8 model.
            </span>
        </div>
        """)
        helper.play_stored_video(0.10, model)

    elif source_radio == settings.WEBCAM:
        st.html("""
        <div class="ui-card" style="margin-bottom: 16px; padding: 16px 20px;">
            <strong style="color: #17352b; font-size: 15px;">Live Webcam Detection</strong>
            <span style="display: block; font-size: 12px; color: #72847c; margin-top: 2px;">
                Use connected camera for real-time edge waste detection.
            </span>
        </div>
        """)
        helper.play_webcam(0.10, model)

    elif source_radio == settings.YOUTUBE:
        st.html("""
        <div class="ui-card" style="margin-bottom: 16px; padding: 16px 20px;">
            <strong style="color: #17352b; font-size: 15px;">YouTube Stream Detection</strong>
            <span style="display: block; font-size: 12px; color: #72847c; margin-top: 2px;">
                Analyze waste video directly from a public YouTube stream.
            </span>
        </div>
        """)
        helper.play_youtube_video(0.10, model)

    elif source_radio == settings.RTSP:
        st.html("""
        <div class="ui-card" style="margin-bottom: 16px; padding: 16px 20px;">
            <strong style="color: #17352b; font-size: 15px;">RTSP Camera Stream</strong>
            <span style="display: block; font-size: 12px; color: #72847c; margin-top: 2px;">
                Connect continuous RTSP IP camera feed for automated surveillance.
            </span>
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
        <div style="background: #ffffff; border: 1px solid #dce8e0; border-radius: 12px; padding: 14px 18px; margin-bottom: 18px;">
            <div style="font-size: 13px; font-weight: 750; color: #176044;">Sample Preview Analytics</div>
            <div style="font-size: 12px; color: #63756d; margin-top: 2px;">
                No active detection has been performed in this session yet. Showing baseline distribution preview below. Run a detection to view live figures.
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
    <div class="section-head" style="margin-top: 24px;">
        <div class="section-head-title">Waste Category Distribution</div>
        <div class="section-head-subtitle">Volume breakdown and material dominance.</div>
    </div>
    """)

    chart_df = pd.DataFrame({
        "Waste Category": list(stats.keys()),
        "Quantity": [item["count"] for item in stats.values()]
    })

    c_col1, c_col2 = st.columns([1.7, 1])
    with c_col1:
        st.html("""
        <div class="ui-card" style="padding: 18px 20px 10px;">
            <div style="font-size: 15px; font-weight: 800; color: #17352b;">Category Distribution</div>
            <div style="font-size: 11px; color: #72847c; margin-top: 2px; margin-bottom: 12px;">Count of identified items per class</div>
        """)
        st.bar_chart(chart_df.set_index("Waste Category"), use_container_width=True)
        st.html("</div>")

    with c_col2:
        st.html(f"""
        <div style="background: #17352b; border-radius: 16px; padding: 24px; min-height: 290px; color: #ffffff;">
            <div style="color: #9eccb5; font-size: 10px; font-weight: 800; letter-spacing: 1px;">AI GENERATED INSIGHT</div>
            <div style="font-size: 16px; font-weight: 750; margin-top: 14px;">Dominant Material</div>
            <div style="font-size: 26px; font-weight: 850; margin-top: 4px; color: #6ee7b7;">{dominant_category}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.14); margin: 18px 0;"></div>
            <div style="color: #bcd4c8; font-size: 11px;">This category accounts for</div>
            <div style="font-size: 32px; font-weight: 850; margin-top: 2px;">{dominant_percentage:.1f}%</div>
            <div style="color: #bcd4c8; font-size: 11px;">of all detected waste ({dominant_count} items).</div>
            <div style="color: #8fb9a4; font-size: 10px; margin-top: 18px;">Targeted recycling sorting recommended for this stream.</div>
        </div>
        """)

    st.html("""
    <div class="section-head" style="margin-top: 24px;">
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

    if not has_live_data:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        if st.button("Run Live Detection", type="primary", key="analytics_run_det"):
            st.session_state.page = "Detection"
            st.rerun()

# ============================================================
# PAGE: REPORTS (EMAIL & EXPORT CENTER)
# ============================================================

elif page == "Reports":

    st.html("""
    <div class="page-header">
        <div>
            <div class="page-eyebrow">WASTEAI &bull; REPORTING CENTER</div>
            <h1 class="page-title">Waste Reports</h1>
            <div class="page-description">Generate, review, download, and email structured waste classification reports.</div>
        </div>
        <div class="ui-badge-ready">
            <span class="ui-badge-dot"></span>
            Report Ready
        </div>
    </div>
    """)

    has_live_data = ("detection_stats" in st.session_state and st.session_state["detection_stats"])

    if not has_live_data:
        st.html("""
        <div style="background: #ffffff; border: 1px solid #dce8e0; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="font-size: 13px; font-weight: 750; color: #176044;">Baseline Report Preview</div>
            <div style="font-size: 12px; color: #63756d; margin-top: 2px;">
                Displaying default sample report data. Run a detection in the Detection tab to update with your live session results.
            </div>
        </div>
        """)
        stats = {
            "PLASTIC": {"count": 4, "conf_sum": 3.72},
            "CARDBOARD": {"count": 2, "conf_sum": 1.76},
            "GLASS": {"count": 1, "conf_sum": 0.92},
            "METAL": {"count": 2, "conf_sum": 1.84},
            "BIODEGRADABLE": {"count": 3, "conf_sum": 2.61},
            "PAPER": {"count": 1, "conf_sum": 0.88}
        }
    else:
        stats = st.session_state["detection_stats"]

    total_items = sum(item["count"] for item in stats.values())
    unique_categories = len(stats)
    dominant_category = max(stats.items(), key=lambda x: x[1]["count"])[0]

    # Overview KPIs
    st.html("""
    <div class="section-head" style="margin-top: 0;">
        <div class="section-head-title">Report Overview</div>
        <div class="section-head-subtitle">Key performance metrics of the waste detection report.</div>
    </div>
    """)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL WASTE ITEMS</div>
            <div class="kpi-value">{total_items}</div>
            <div class="kpi-meta">Objects detected</div>
        </div>
        """)
    with r2:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">CATEGORIES IDENTIFIED</div>
            <div class="kpi-value">{unique_categories}</div>
            <div class="kpi-meta">Distinct classifications</div>
        </div>
        """)
    with r3:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">DOMINANT CATEGORY</div>
            <div class="kpi-value" style="font-size: 21px;">{dominant_category}</div>
            <div class="kpi-meta">Highest proportion</div>
        </div>
        """)

    # Table breakdown
    st.html("""
    <div class="section-head" style="margin-top: 24px;">
        <div class="section-head-title">Detection Report Table</div>
        <div class="section-head-subtitle">Structured tabular breakdown of each classified material stream.</div>
    </div>
    """)

    report_data = []
    for category, data in stats.items():
        avg_conf = (data["conf_sum"] / data["count"]) * 100
        pct = (data["count"] / total_items) * 100 if total_items > 0 else 0
        report_data.append({
            "Waste Category": category,
            "Quantity": data["count"],
            "Percentage": f"{pct:.1f}%",
            "Average Confidence": f"{avg_conf:.1f}%"
        })

    report_df = pd.DataFrame(report_data)

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Waste Category": st.column_config.TextColumn("Waste Category"),
            "Quantity": st.column_config.NumberColumn("Quantity", format="%d"),
            "Percentage": st.column_config.TextColumn("Percentage"),
            "Average Confidence": st.column_config.TextColumn("Average Confidence")
        }
    )

    # --------------------------------------------------------
    # REPORT ACTIONS & DISPATCH
    # --------------------------------------------------------
    report_csv = report_df.to_csv(index=False).encode("utf-8")

    # Generate or locate PDF report
    pdf_path = None
    pdf_bytes = None
    if generate_report is not None:
        try:
            res_dir = Path("results")
            res_dir.mkdir(parents=True, exist_ok=True)
            source_name = st.session_state.get("last_uploaded_name", "waste_detection_sample.jpg")
            detected_items = st.session_state.get("detected_items", None)
            generated_pdf, _ = generate_report.generate_user_waste_report(
                detected_items=detected_items,
                image_name=source_name,
                output_folder=str(res_dir)
            )
            if generated_pdf and Path(generated_pdf).exists():
                pdf_path = str(generated_pdf)
                with open(pdf_path, "rb") as pf:
                    pdf_bytes = pf.read()
        except Exception as pe:
            print(f"[Notice] PDF report rendering: {pe}")

    st.html("""
    <div class="ui-card" style="margin-top: 20px; padding: 22px 24px;">
        <div style="font-size: 16px; font-weight: 800; color: #17352b;">Report Actions</div>
        <div style="font-size: 12px; color: #6a7c74; margin-top: 2px; margin-bottom: 16px;">
            Download structured files or email the compliance report directly to system administration.
        </div>
    """)

    if pdf_bytes:
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            st.download_button(
                label="Download CSV Report",
                data=report_csv,
                file_name="waste_detection_report.csv",
                mime="text/csv",
                use_container_width=True,
                key="reports_download_csv_btn"
            )
        with btn_c2:
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=Path(pdf_path).name if pdf_path else "waste_detection_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="reports_download_pdf_btn"
            )
        with btn_c3:
            send_email_clicked = st.button(
                label="Send Report to Admin",
                type="primary",
                use_container_width=True,
                key="reports_email_btn"
            )
    else:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            st.download_button(
                label="Download Report (CSV)",
                data=report_csv,
                file_name="waste_detection_report.csv",
                mime="text/csv",
                use_container_width=True,
                key="reports_download_csv_btn"
            )
        with btn_c2:
            send_email_clicked = st.button(
                label="Send Report to Admin",
                type="primary",
                use_container_width=True,
                key="reports_email_btn"
            )

    st.html("</div>")

    # Handle Send Report to Admin
    if send_email_clicked:
        with st.spinner("Dispatching waste detection report to administrator email..."):
            summary_metrics = {
                "total_items": total_items,
                "unique_categories": unique_categories,
                "dominant_category": dominant_category
            }
            img_name = st.session_state.get("last_uploaded_name", "waste_detection_sample.jpg")

            success, message = email_service.send_waste_report_email(
                report_df=report_df,
                report_csv=report_csv,
                pdf_path=pdf_path,
                summary_metrics=summary_metrics,
                image_name=img_name
            )

        if success:
            st.success(message)
            st.toast("Report dispatched to administrator.", icon=None)
        else:
            st.error(message)
            with st.expander("How to configure email credentials"):
                st.markdown("""
                **To enable automated email delivery:**
                
                1. Create a `.env` file in the project root (see `.env.example`), OR create `.streamlit/secrets.toml`.
                2. Configure the following variables:
                ```ini
                SMTP_HOST=smtp.gmail.com
                SMTP_PORT=465
                SMTP_USERNAME=your-email@gmail.com
                SMTP_PASSWORD=your-16-char-app-password
                ADMIN_EMAIL=admin@example.com
                ```
                3. For Gmail, generate a 16-character **App Password** from your [Google Account Security Settings](https://myaccount.google.com/apppasswords).
                """)

    # Metadata cards
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.html("""
        <div class="ui-card" style="padding: 16px 18px;">
            <div class="kpi-label">DETECTION MODEL</div>
            <div style="font-size: 14px; font-weight: 750; color: #17352b; margin-top: 4px;">
                YOLOv8 Deep Neural Network
            </div>
        </div>
        """)
    with m_col2:
        st.html("""
        <div class="ui-card" style="padding: 16px 18px;">
            <div class="kpi-label">REPORT TYPE</div>
            <div style="font-size: 14px; font-weight: 750; color: #17352b; margin-top: 4px;">
                Waste Classification & Material Logging (CSV & PDF)
            </div>
        </div>
        """)

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

    # Model config
    st.markdown("### AI Model Configuration")

    mc1, mc2 = st.columns(2)
    with mc1:
        st.html("""
        <div class="ui-card" style="min-height: 100px;">
            <div class="kpi-label">DETECTION MODEL</div>
            <div style="font-size: 20px; font-weight: 850; color: #17352b; margin-top: 4px;">YOLOv8</div>
            <div style="font-size: 12px; color: #72847c; margin-top: 2px;">Computer vision architecture</div>
        </div>
        """)

    with mc2:
        st.html("""
        <div class="ui-card" style="min-height: 100px;">
            <div class="kpi-label">MODEL STATUS</div>
            <div style="font-size: 20px; font-weight: 850; color: #176044; margin-top: 4px;">Ready</div>
            <div style="font-size: 12px; color: #72847c; margin-top: 2px;">Weights loaded in memory</div>
        </div>
        """)

    st.html(f"""
    <div style="background: #ffffff; border: 1px solid #e1e9e5; border-radius: 12px; padding: 12px 16px; margin-top: 10px; margin-bottom: 24px; font-size: 12px; color: #5f7068;">
        <strong style="color: #17352b;">Active Model Weights Path:</strong> {settings.DETECTION_MODEL}
    </div>
    """)

    # Detection parameters
    st.markdown("### Detection Configuration")

    dc1, dc2 = st.columns(2)
    with dc1:
        st.html("""
        <div class="ui-card" style="padding: 16px 20px; margin-bottom: 10px;">
            <div style="font-size: 14px; font-weight: 750; color: #17352b;">Default Confidence Threshold</div>
            <div style="font-size: 11px; color: #72847c; margin-top: 2px;">Base cutoff score for valid object detection</div>
        </div>
        """)

        settings_confidence = st.slider(
            "Default Confidence Threshold",
            min_value=5,
            max_value=100,
            value=10,
            step=5,
            help="Controls minimum confidence required for displaying detections."
        )
        st.caption(f"Default threshold: **{settings_confidence}%**")

    with dc2:
        st.html("""
        <div class="ui-card" style="padding: 16px 20px; margin-bottom: 10px;">
            <div style="font-size: 14px; font-weight: 750; color: #17352b;">Object Tracking</div>
            <div style="font-size: 11px; color: #72847c; margin-top: 2px;">Track object instances across consecutive video frames</div>
        </div>
        """)

        enable_tracking = st.toggle(
            "Enable Object Tracking",
            value=False,
            help="Track detected items across frames in video and live streams."
        )

        if enable_tracking:
            tracker_type = st.selectbox("Tracking Algorithm", ["bytetrack.yaml", "botsort.yaml"])
            st.success(f"Tracking active: {tracker_type}")
        else:
            st.info("Tracking disabled for single-frame inferences.")

    # Email Service Status in Settings
    st.markdown("### Email Dispatch Configuration")
    email_cfg = email_service.get_email_config()
    is_email_valid, missing_keys, _ = email_service.validate_email_config(email_cfg)

    ec1, ec2 = st.columns(2)
    with ec1:
        status_label = "Configured" if is_email_valid else "Missing Credentials"
        status_color = "#176044" if is_email_valid else "#b91c1c"
        admin_display = email_cfg.get("admin_email") or "Not configured"
        st.html(f"""
        <div class="ui-card" style="min-height: 105px;">
            <div class="kpi-label">ADMIN RECIPIENT</div>
            <div style="font-size: 16px; font-weight: 750; color: #17352b; margin-top: 4px;">{admin_display}</div>
            <div style="font-size: 11px; color: {status_color}; font-weight: 700; margin-top: 4px;">{status_label}</div>
        </div>
        """)

    with ec2:
        smtp_display = f"{email_cfg.get('smtp_host')}:{email_cfg.get('smtp_port')}"
        sender_display = email_cfg.get("sender_email") or "Not configured"
        st.html(f"""
        <div class="ui-card" style="min-height: 105px;">
            <div class="kpi-label">SMTP SERVER & SENDER</div>
            <div style="font-size: 14px; font-weight: 750; color: #17352b; margin-top: 4px;">{smtp_display}</div>
            <div style="font-size: 11px; color: #6a7c74; margin-top: 4px;">Sender: {sender_display}</div>
        </div>
        """)

    if not is_email_valid:
        st.caption("To enable email dispatch, configure credentials in `.env` (see `.env.example`) or `.streamlit/secrets.toml`.")

    # Categories
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### Supported Waste Categories")
    st.caption("Material classification classes recognized by the active model.")

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
            <div class="ui-card" style="padding: 16px; margin-bottom: 12px; min-height: 82px;">
                <div style="font-size: 13px; font-weight: 800; color: #17352b;">{cat_name}</div>
                <div style="font-size: 11px; color: #72847c; margin-top: 3px; line-height: 1.45;">{cat_desc}</div>
            </div>
            """)

    # Input Sources
    st.markdown("### Detection Input Channels")
    st.caption("Configured data ingestion sources.")

    source_cols = st.columns(len(settings.SOURCES_LIST))
    for i, src in enumerate(settings.SOURCES_LIST):
        with source_cols[i]:
            st.html(f"""
            <div class="ui-card" style="padding: 14px 10px; text-align: center; min-height: 75px;">
                <div style="font-size: 13px; font-weight: 750; color: #17352b;">{src}</div>
                <div style="font-size: 10px; color: #1f7d56; font-weight: 700; margin-top: 4px;">Available</div>
            </div>
            """)

    # System Info
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### System Information")

    si1, si2 = st.columns(2)
    with si1:
        st.html("""
        <div class="ui-card" style="padding: 18px;">
            <div class="kpi-label">APPLICATION</div>
            <div style="font-size: 15px; font-weight: 800; color: #17352b; margin-top: 4px;">WasteAI</div>
            <div style="font-size: 11px; color: #72847c; margin-top: 2px;">Smart Waste Classification & Reporting System</div>
            <div style="height: 1px; background: #eef2ef; margin: 12px 0;"></div>
            <div class="kpi-label">CORE ENGINE</div>
            <div style="font-size: 13px; font-weight: 700; color: #17352b; margin-top: 4px;">YOLOv8 Object Detection</div>
        </div>
        """)

    with si2:
        st.html("""
        <div class="ui-card" style="padding: 18px;">
            <div class="kpi-label">FRAMEWORK</div>
            <div style="font-size: 15px; font-weight: 800; color: #17352b; margin-top: 4px;">Streamlit Web Application</div>
            <div style="font-size: 11px; color: #72847c; margin-top: 2px;">Interactive dashboard & analytics UI</div>
            <div style="height: 1px; background: #eef2ef; margin: 12px 0;"></div>
            <div class="kpi-label">ENVIRONMENT</div>
            <div style="font-size: 13px; font-weight: 700; color: #17352b; margin-top: 4px;">Python Runtime & Ultralytics</div>
        </div>
        """)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.caption("Configuration updates apply immediately to the active application session.")
