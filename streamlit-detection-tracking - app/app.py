import sys
import os
from pathlib import Path
import PIL.Image
import PIL.ExifTags
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

try:
    import email_service
except ImportError:
    email_service = None

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

    /* Standard & Primary Button Styling */
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
    }

    .stDownloadButton > button {
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 9px !important;
        font-weight: 750 !important;
        font-size: 14px !important;
        border: 1.5px solid #176044 !important;
        background-color: #176044 !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background-color: #176044 !important;
        color: #ffffff !important;
        border: 1.5px solid #176044 !important;
        border-radius: 8px !important;
        font-weight: 750 !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
    }

    .wa-top-divider {
        width: 100%;
        height: 1px;
        background: #e2ebe6;
        margin-top: 10px;
        margin-bottom: 24px;
    }

    .ui-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
    }

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
    }

    .ui-badge-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #28a76d;
        display: inline-block;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 110px;
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
    }

    .kpi-meta {
        color: #7d8f87;
        font-size: 11px;
        margin-top: 5px;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 22px;
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
        margin: 0;
    }

    .page-description {
        color: #63756d;
        font-size: 13px;
        margin-top: 4px;
    }

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

    .image-frame-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    }

    .image-frame-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
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

    .activity-confidence {
        color: #176044;
        font-size: 12px;
        font-weight: 750;
    }

    .home-hero {
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

    .home-hero h1 {
        margin: 0;
        font-size: 48px;
        font-weight: 850;
        color: #13362a;
    }

    .home-hero h1 span {
        color: #1c885e;
    }

    .home-visual-card {
        width: 310px;
        padding: 26px 28px;
        border-radius: 20px;
        background: #ffffff;
        border: 1px solid #dbe8e1;
    }

    .home-feature-card {
        min-height: 120px;
        padding: 24px 22px;
        border-radius: 16px;
        background: #ffffff;
        border: 1px solid #e1e9e5;
    }

    .home-input-card {
        min-height: 110px;
        padding: 20px;
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 14px;
    }

    /* Force high contrast text on buttons */
    .stButton > button, .stButton > button * { color: #17352b !important; }
    .stButton > button[kind="primary"], .stButton > button[kind="primary"] * { color: #ffffff !important; }
    .stDownloadButton > button, .stDownloadButton > button * { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP NAVIGATION (PREMIUM FLOATING NAVBAR + MOBILE TOGGLER)
# ============================================================

pages = ["Home", "Dashboard", "Detection", "Analytics", "Settings"]

if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Home"

if "mobile_menu_open" not in st.session_state:
    st.session_state.mobile_menu_open = False

# --- DESKTOP NAVBAR (FLOATING GLASSMORPHIC STRIP) ---
st.html('<div class="nav-desktop-marker"></div>')
d_nav_cols = st.columns([2.6, 1, 1, 1, 1, 1])

with nav_columns[0]:
    st.html("""
    <div class="wa-top-brand">
        <div class="wa-logo-badge">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
                <path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/>
                <path d="m14 14 3-3 3 3"/>
                <path d="m11 5 3-3 3 3"/>
                <path d="M14 2v6"/>
                <path d="m6 16-3 3 3 3"/>
            </svg>
        </div>
        <div>
            <div style="display: flex; align-items: center;">
                <span class="wa-top-brand-name">WasteAI</span>
                <span class="wa-brand-pill">PRO</span>
            </div>
            <div class="wa-top-brand-subtitle">Smart Waste Intelligence</div>
        </div>
    </div>
    """)

for i, page_name in enumerate(pages):
    with nav_columns[i + 1]:
        is_active = (st.session_state.page == page_name)
        button_type = "primary" if is_active else "secondary"
        if st.button(page_name, key=f"top_nav_{page_name.lower()}", type=button_type):
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

    st.html("""
    <div class="home-hero">
        <div>
            <div class="ui-badge-ready" style="margin-bottom: 16px;">
                WASTEAI &bull; AI-POWERED WASTE INTELLIGENCE
            </div>
            <h1>Smarter Waste.<br><span>Cleaner Future.</span></h1>
            <p>WasteAI uses advanced computer vision to automatically detect, classify, and analyze waste across images, recorded video, and live video feeds.</p>
        </div>
        <div class="home-visual-card">
            <div style="font-size: 10px; font-weight: 800; color: #1f7d56; text-transform: uppercase;">SYSTEM STATUS</div>
            <div style="font-size: 20px; font-weight: 800; color: #15382b; margin-top: 4px;">AI Waste Detection</div>
            <div style="margin-top: 10px; font-size: 12px; color: #55665f; display: flex; align-items: center; gap: 7px;">
                <span class="ui-badge-dot"></span> YOLOv8 Engine Ready
            </div>
        </div>
    </div>
    """)

    hero_col1, hero_col2 = st.columns(2)
    with hero_col1:
        if st.button("Start Waste Detection", type="primary", key="home_btn_detect"):
            st.session_state.page = "Detection"
            st.rerun()
    with hero_col2:
        if st.button("View Dashboard", type="secondary", key="home_btn_dash"):
            st.session_state.page = "Dashboard"
            st.rerun()
    with hero_cta3:
        if st.button("Analytics & Reporting", type="secondary", use_container_width=True, key="home_btn_analytics"):
            st.session_state.page = "Analytics"
            st.rerun()

    st.html("""
    <div class="section-head" style="margin-top: 30px;">
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
                <h3 style="margin:0; font-size: 17px; color:#173c30;">{title}</h3>
                <p style="margin-top: 8px; font-size: 13px; color:#63756d;">{desc}</p>
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
            <span class="ui-badge-dot"></span> System Online
        </div>
    </div>
    """)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.html("""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL INFERENCES</div>
            <div class="kpi-value">12</div>
            <div class="kpi-meta">Recorded sessions</div>
        </div>
        """)
    with k2:
        st.html("""
        <div class="kpi-card">
            <div class="kpi-label">ITEMS IDENTIFIED</div>
            <div class="kpi-value">48</div>
            <div class="kpi-meta">Waste objects logged</div>
        </div>
        """)
    with k3:
        st.html("""
        <div class="kpi-card">
            <div class="kpi-label">AVG CONFIDENCE</div>
            <div class="kpi-value">88.4%</div>
            <div class="kpi-meta">Model prediction score</div>
        </div>
        """)
    with k4:
        st.html("""
        <div class="kpi-card">
            <div class="kpi-label">TOP CATEGORY</div>
            <div class="kpi-value" style="font-size: 22px;">PLASTIC</div>
            <div class="kpi-meta">Most frequent classification</div>
        </div>
        """)

# ============================================================
# PAGE: DETECTION (WITH LOCATION & DIMENSIONS WORKFLOW)
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
            <span class="ui-badge-dot"></span> YOLOv8 Ready
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

    # --------------------------------------------------------
    # SOURCE: IMAGE & CAMERA CLICK
    # --------------------------------------------------------
    if source_radio == settings.IMAGE:

        st.html("""
        <div class="section-head" style="margin-top: 10px;">
            <div class="section-head-title">Photo Input Method</div>
            <div class="section-head-subtitle">Choose whether to upload an image file or capture directly using your camera.</div>
        </div>
        """)

        input_mode = st.radio(
            "Photo Input Method",
            ["Upload Image File", "Capture Photo with Camera"],
            horizontal=True,
            label_visibility="collapsed"
        )

        uploaded_file = None
        is_camera = False

        if input_mode == "Upload Image File":
            uploaded_file = st.file_uploader(
                "Upload a waste image...", 
                type=["jpg", "jpeg", "png", "webp", "bmp"]
            )
        else:
            uploaded_file = st.camera_input("Click photo using webcam")
            is_camera = True

if uploaded_file is not None:
        # 1. Load Image & Extract Dimensions
        uploaded_image = PIL.Image.open(uploaded_file)
        img_w, img_h = helper.get_image_dimensions(uploaded_image)

        # 2. Location & Metadata Header
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.subheader("📍 Image Metadata & Location Tracking")

        dim_col, loc_col = st.columns([1, 2])

        with dim_col:
            st.info(f"**Image Dimensions:**  \n`{img_w} px` (W) × `{img_h} px` (H)")

        final_location = "Location Not Specified"

        with loc_col:
            if is_camera:
                st.markdown("**Device Live GPS Tracker:**")
                # Trigger browser HTML5 Geolocation
                live_gps_val = helper.get_live_device_location()

                # Dynamic coordinates parsing or fallback
                default_gps = live_gps_val if isinstance(live_gps_val, str) else "GPS: 15.53648°, 79.96853°"

                final_location = st.text_input(
                    "Disposal Site / Location Tag:",
                    value=default_gps,
                    placeholder="E.g., Sector 4 Disposal Yard / Bin A",
                    help="Auto-detected live coordinates or enter custom facility address."
                )

                # Render compact map widget below text field
                coords = helper.parse_gps_coords(final_location)
                if coords:
                    lat, lon = coords
                    map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
                    st.markdown("**🗺️ Live Location Map:**")
                    map_col, _ = st.columns([1, 1])
                    with map_col:
                        st.map(map_data, zoom=14, height=200)
            else:
                # File Upload Mode: Check EXIF or leave empty for user entry
                auto_location = helper.extract_exif_location(uploaded_image)

                if auto_location:
                    st.success(f"**Auto-Detected EXIF GPS:** `{auto_location}`")
                    final_location = st.text_input(
                        "Disposal Site / Location Tag:",
                        value=auto_location,
                        placeholder="E.g., Recycling Yard B",
                        help="Pre-filled from EXIF metadata. Edit if needed."
                    )
                else:
                    st.warning("No EXIF GPS metadata found in file.")
                    final_location = st.text_input(
                        "Enter Disposal Site / Location Tag Manually:",
                        value="",
                        placeholder="E.g., Main Facility Sterilization Unit, Bin 3"
                    )

        # 3. Perform Object Detection
        if st.button("Run Waste Detection", type="primary"):
            col1, col2 = st.columns(2)

            with col1:
                st.html("""
                <div class="image-frame-card">
                    <div class="image-frame-header">
                        <span class="image-frame-title">Original Source Photo</span>
                        <span class="image-frame-meta">Raw Input</span>
                    </div>
                </div>
                """)
                st.image(uploaded_image)

            if model is not None:
                res = model.predict(uploaded_image, conf=0.25)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]

                with col2:
                    st.html("""
                    <div class="image-frame-card">
                        <div class="image-frame-header">
                            <span class="image-frame-title">AI Detection Output</span>
                            <span class="image-frame-meta">Processed</span>
                        </div>
                    </div>
                    """)
                    st.image(res_plotted)

                # 4. Compile Detection Table with Dimensions & Location Data
                detected_items = []
                if boxes is not None and len(boxes) > 0:
                    for idx, box in enumerate(boxes):
                        cls_id = int(box.cls[0].item())
                        cls_name = model.names[cls_id]
                        conf_score = float(box.conf[0].item())

                        detected_items.append({
                            "Item ID": f"ITEM-{idx+1:02d}",
                            "Category": cls_name,
                            "Confidence": f"{conf_score * 100:.1f}%",
                            "Dimensions": f"{img_w} x {img_h} px",
                            "Location": final_location or "N/A"
                        })

                    st.markdown("### 📊 Detection Metadata Breakdown")
                    df_detected = pd.DataFrame(detected_items)
                    st.dataframe(df_detected)

                    # 5. Trigger PDF/CSV Report Generation
                    if generate_report is not None:
                        if st.button("Export Full PDF Report & CSV Log"):
                            report_data = [{
                                "Item_ID": item["Item ID"],
                                "Category": item["Category"],
                                "Confidence": float(item["Confidence"].replace("%", "")) / 100.0,
                                "Type": "Waste Item",
                                "Width": img_w,
                                "Height": img_h,
                                "Location": final_location
                            } for item in detected_items]

                            generate_report.generate_user_waste_report(
                                detected_items=report_data,
                                image_name=getattr(uploaded_file, "name", "clicked_photo.jpg"),
                                output_folder="results"
                            )
                            st.success("Report successfully exported to `results/` directory!")
                else:
                    st.info("No waste items detected in this photo.")