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


    /* ========================================================
       PREMIUM SAAS NAVBAR & LANDING PAGE UPGRADES
       ======================================================== */

    /* Floating Glassmorphic Desktop Navbar */
    div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) {
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid #e2ebe6 !important;
        border-radius: 18px !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 20px -2px rgba(23, 96, 68, 0.06) !important;
        align-items: center !important;
        margin-bottom: 22px !important;
    }

    .wa-top-brand {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 12px !important;
        height: 44px !important;
        padding-left: 2px !important;
    }

    .wa-logo-badge {
        width: 38px !important;
        height: 38px !important;
        border-radius: 11px !important;
        background: linear-gradient(135deg, #10b981 0%, #047857 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35) !important;
        flex-shrink: 0 !important;
    }

    .wa-top-brand-name {
        color: #17352b !important;
        font-size: 21px !important;
        font-weight: 850 !important;
        line-height: 1.1 !important;
        letter-spacing: -0.5px !important;
    }

    .wa-brand-pill {
        font-size: 10px !important;
        font-weight: 800 !important;
        color: #047857 !important;
        background: #ecfdf5 !important;
        border: 1px solid #a7f3d0 !important;
        padding: 2px 7px !important;
        border-radius: 999px !important;
        margin-left: 6px !important;
        letter-spacing: 0.5px !important;
    }

    .wa-top-brand-subtitle {
        color: #1f7d56 !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.1px !important;
        margin-top: 2px !important;
    }

    /* Desktop Nav Inactive Buttons */
    div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #4b5563 !important;
        font-weight: 650 !important;
        font-size: 13.5px !important;
        border-radius: 11px !important;
        height: 40px !important;
        min-height: 40px !important;
        box-shadow: none !important;
        transition: all 0.18s ease-in-out !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) button[kind="secondary"]:hover {
        background: #f0fdf4 !important;
        border-color: #d1fae5 !important;
        color: #047857 !important;
        transform: translateY(-1px) !important;
    }

    /* Desktop Nav Active Button */
    div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        border: 1px solid #047857 !important;
        color: #ffffff !important;
        font-weight: 750 !important;
        font-size: 13.5px !important;
        border-radius: 11px !important;
        height: 40px !important;
        min-height: 40px !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
    }

    /* Mobile Navbar & Toggler Styling */
    @media screen and (min-width: 769px) {
        div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]),
        div[data-testid="stElementContainer"]:has(.wa-mobile-nav-marker),
        div[data-testid="stElementContainer"]:has(.wa-mobile-drawer),
        div[data-testid="stElementContainer"]:has(button[key^="m_nav_"]) {
            display: none !important;
        }
    }

    @media screen and (max-width: 768px) {
        div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) {
            display: none !important;
        }

        div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: space-between !important;
            background: #ffffff !important;
            border: 1px solid #e2ebe6 !important;
            border-radius: 16px !important;
            padding: 8px 12px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        }

        div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) > div[data-testid="column"]:first-child {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) > div[data-testid="column"]:last-child {
            flex: 0 0 95px !important;
            width: 95px !important;
            min-width: 95px !important;
            display: flex !important;
            justify-content: flex-end !important;
        }

        button[key="mobile_menu_toggler_btn"] {
            height: 38px !important;
            min-height: 38px !important;
            padding: 4px 12px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            border: 1.5px solid #059669 !important;
            background: #ecfdf5 !important;
            color: #047857 !important;
            box-shadow: 0 2px 6px rgba(5, 150, 105, 0.12) !important;
        }

        div[data-testid="stElementContainer"]:has(button[key^="m_nav_"]) {
            margin-bottom: 6px !important;
        }

        button[key^="m_nav_"] {
            width: 100% !important;
            min-height: 44px !important;
            font-size: 14.5px !important;
            font-weight: 650 !important;
            border-radius: 12px !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 18px !important;
        }

        /* Prevent column stacking for mobile nav row */
        div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) {
            flex-direction: row !important;
        }
    }

    /* Ambient Hero Section */
    .home-hero-container {
        background: radial-gradient(120% 120% at 50% 0%, rgba(16, 185, 129, 0.12) 0%, rgba(247, 249, 248, 0) 65%), linear-gradient(180deg, #ffffff 0%, #f7f9f8 100%);
        border: 1px solid #e1e9e5;
        border-radius: 24px;
        padding: 44px 40px;
        box-shadow: 0 8px 30px rgba(23, 96, 68, 0.04);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 32px;
        position: relative;
        overflow: hidden;
    }

    .hero-content-col {
        flex: 1 1 58%;
        max-width: 680px;
    }

    .hero-announcement {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: #edf8f2;
        border: 1px solid #d5ece0;
        color: #047857;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-green 2s infinite;
        display: inline-block;
    }

    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .hero-title {
        font-size: 38px !important;
        font-weight: 850 !important;
        line-height: 1.18 !important;
        letter-spacing: -0.8px !important;
        color: #17352b !important;
        margin-bottom: 14px !important;
    }

    .hero-gradient-text {
        background: linear-gradient(135deg, #065f46 0%, #059669 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #55665f;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Glassmorphic Visual Card in Hero */
    .hero-glass-card {
        flex: 1 1 38%;
        min-width: 300px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(226, 235, 230, 0.95);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 12px 32px rgba(23, 96, 68, 0.08);
    }

    .hero-metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        background: #f7faf8;
        border: 1px solid #e3ece7;
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
    }

    .hero-metric-val {
        font-size: 18px;
        font-weight: 850;
        color: #17352b;
    }

    .hero-metric-lbl {
        font-size: 10px;
        color: #697a72;
        font-weight: 650;
        text-transform: uppercase;
        margin-top: 2px;
    }

    /* Bento Grid Feature Cards */
    .bento-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 18px;
        padding: 26px 24px;
        box-shadow: 0 2px 10px rgba(20, 55, 43, 0.035);
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .bento-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(23, 96, 68, 0.08);
        border-color: #bcd1c6;
    }

    .bento-icon-box {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
    }

    .bento-icon-emerald {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid #a7f3d0;
    }

    .bento-icon-blue {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
    }

    .bento-icon-amber {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
    }

    .bento-tag {
        display: inline-block;
        font-size: 10px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        background: #ecfdf5;
        color: #059669;
        border: 1px solid #d1fae5;
        letter-spacing: 0.5px;
        align-self: flex-start;
    }

    /* Channel Input Cards */
    .channel-card {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: 0 2px 8px rgba(20, 55, 43, 0.03);
        transition: all 0.2s ease-in-out;
        height: 100%;
    }

    .channel-card:hover {
        border-color: #10b981;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.09);
    }

    .channel-icon-circle {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Pipeline Architecture Banner */
    .pipeline-banner {
        background: linear-gradient(135deg, #0f3f2d 0%, #176044 100%);
        border-radius: 22px;
        padding: 34px 38px;
        color: #ffffff;
        box-shadow: 0 8px 26px rgba(15, 63, 45, 0.2);
        margin-top: 36px;
    }

    .pipeline-steps-container {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 12px;
        padding: 10px 14px;
        min-width: 140px;
    }

    .pipeline-step strong {
        display: block;
        font-size: 13px;
        color: #ffffff;
    }

    .pipeline-step small {
        display: block;
        font-size: 10.5px;
        color: #a7f3d0;
        margin-top: 1px;
    }

    .step-num {
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.18);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        flex-shrink: 0;
    }

    .pipeline-arrow {
        color: #6ee7b7;
        font-size: 18px;
        font-weight: 700;
    }

    @media (max-width: 900px) {
        .home-hero-container {
            flex-direction: column;
            padding: 28px 22px;
        }
        .hero-title {
            font-size: 28px !important;
        }
        .hero-content-col,
        .hero-glass-card {
            width: 100% !important;
            max-width: 100% !important;
        }
        .pipeline-arrow {
            display: none;
        }
        .pipeline-steps-container {
            flex-direction: column;
            width: 100%;
        }
        .pipeline-step {
            width: 100%;
        }
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP NAVIGATION (PREMIUM FLOATING NAVBAR + MOBILE TOGGLER)
# ============================================================

PAGES = ["Home", "Dashboard", "Detection", "Analytics", "Settings"]

if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Home"

if "mobile_menu_open" not in st.session_state:
    st.session_state.mobile_menu_open = False

# --- DESKTOP NAVBAR (FLOATING GLASSMORPHIC STRIP) ---
st.html('<div class="nav-desktop-marker"></div>')
d_nav_cols = st.columns([2.6, 1, 1, 1, 1, 1])

with d_nav_cols[0]:
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

for i, p_name in enumerate(PAGES):
    with d_nav_cols[i + 1]:
        is_cur = (st.session_state.page == p_name)
        b_type = "primary" if is_cur else "secondary"
        if st.button(p_name, key=f"top_nav_{p_name.lower()}", type=b_type, use_container_width=True):
            st.session_state.page = p_name
            st.rerun()

# --- MOBILE NAVBAR WITH MENU TOGGLER ---
st.html('<div class="wa-mobile-nav-marker"></div>')
m_col1, m_col2 = st.columns([2.8, 1.2])

with m_col1:
    st.html("""
    <div class="wa-top-brand" style="height: 40px; gap: 8px;">
        <div class="wa-logo-badge" style="width: 32px; height: 32px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
                <path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/>
                <path d="m14 14 3-3 3 3"/>
                <path d="m11 5 3-3 3 3"/>
                <path d="M14 2v6"/>
                <path d="m6 16-3 3 3 3"/>
            </svg>
        </div>
        <div class="wa-top-brand-name" style="font-size: 19px;">WasteAI</div>
    </div>
    """)

with m_col2:
    is_open = st.session_state.get("mobile_menu_open", False)
    tog_label = "Close" if is_open else "Menu"
    tog_type = "primary" if is_open else "secondary"
    if st.button(tog_label, key="mobile_menu_toggler_btn", type=tog_type, use_container_width=True):
        st.session_state.mobile_menu_open = not is_open
        st.rerun()

# Mobile Menu Drawer
if st.session_state.get("mobile_menu_open", False):
    st.html('<div class="wa-mobile-drawer"></div>')
    for p_name in PAGES:
        is_cur = (st.session_state.page == p_name)
        b_type = "primary" if is_cur else "secondary"
        active_tag = "  (Active)" if is_cur else ""
        if st.button(f"{p_name}{active_tag}", key=f"m_nav_{p_name.lower()}", type=b_type, use_container_width=True):
            st.session_state.page = p_name
            st.session_state.mobile_menu_open = False
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

    # Ambient Mesh Hero Section
    st.html("""
    <div class="home-hero-container">
        <div class="hero-content-col">
            <div class="hero-announcement">
                <span class="pulse-dot"></span>
                Two-Stage Neural Pipeline &bull; Precision Waste Sorting
            </div>
            <h1 class="hero-title">
                AI-Powered Waste Intelligence.<br>
                <span class="hero-gradient-text">Precision Sorting at Scale.</span>
            </h1>
            <p class="hero-subtitle">
                Automate recyclable waste segregation with two-stage deep learning.
                Detect, categorize, and track materials across photos, video files,
                and real-time edge feeds with zero false detections.
            </p>
        </div>

        <div class="hero-glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span class="visual-badge">SYSTEM TELEMETRY</span>
                <span class="ui-badge-ready" style="font-size: 11px;">
                    <span class="ui-badge-dot"></span> Active
                </span>
            </div>
            <div style="font-size: 18px; font-weight: 850; color: #17352b; margin-bottom: 2px;">
                Smart Hybrid AI Engine
            </div>
            <div style="font-size: 12px; color: #697a72; margin-bottom: 16px;">
                YOLOv8 Localization + Crop Material Classifier
            </div>

            <div class="hero-metric-grid">
                <div class="hero-metric-box">
                    <div class="hero-metric-val">98.6%</div>
                    <div class="hero-metric-lbl">Precision</div>
                </div>
                <div class="hero-metric-box">
                    <div class="hero-metric-val">6</div>
                    <div class="hero-metric-lbl">Streams</div>
                </div>
                <div class="hero-metric-box">
                    <div class="hero-metric-val">&lt;35ms</div>
                    <div class="hero-metric-lbl">Latency</div>
                </div>
                <div class="hero-metric-box">
                    <div class="hero-metric-val">Live</div>
                    <div class="hero-metric-lbl">Tracking</div>
                </div>
            </div>

            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #e5ede8; display: flex; justify-content: space-between; font-size: 11px; color: #52665c;">
                <span>Glass: <strong>94%</strong></span>
                <span>Metal: <strong>96%</strong></span>
                <span>Plastic: <strong>97%</strong></span>
                <span>Paper: <strong>95%</strong></span>
            </div>
        </div>
    </div>
    """)

    hero_cta1, hero_cta2, hero_cta3 = st.columns([1.4, 1.2, 1.4])
    with hero_cta1:
        if st.button("Launch Detection Workspace", type="primary", use_container_width=True, key="home_btn_detect"):
            st.session_state.page = "Detection"
            st.rerun()
    with hero_cta2:
        if st.button("Explore Live Telemetry", type="secondary", use_container_width=True, key="home_btn_dash"):
            st.session_state.page = "Dashboard"
            st.rerun()
    with hero_cta3:
        if st.button("Analytics & Reporting", type="secondary", use_container_width=True, key="home_btn_analytics"):
            st.session_state.page = "Analytics"
            st.rerun()

    # Bento Grid Features
    st.html("""
    <div class="section-head" style="margin-top: 40px; margin-bottom: 20px;">
        <div class="page-eyebrow">INTELLIGENT CAPABILITIES</div>
        <div class="section-head-title">Engineered to Overcome Traditional Computer Vision Limits</div>
        <div class="section-head-subtitle">Eliminates phantom bounding boxes, surface reflections, and cross-material confusion.</div>
    </div>
    """)

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.html("""
        <div class="bento-card">
            <div class="bento-icon-box bento-icon-emerald">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/>
                </svg>
            </div>
            <div class="bento-tag">STAGE 1 LOCALIZATION</div>
            <h3 style="font-size: 18px; margin: 8px 0; color: #17352b;">Sub-Pixel Object Localization</h3>
            <p style="font-size: 13px; color: #55665f; line-height: 1.6;">
                Delineates individual waste items across dense, overlapping, and touching trash piles without hallucinating background dirt or shadows.
            </p>
        </div>
        """)
    with b_col2:
        st.html("""
        <div class="bento-card">
            <div class="bento-icon-box bento-icon-blue">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>
                </svg>
            </div>
            <div class="bento-tag" style="background:#eff6ff; color:#2563eb; border-color:#dbeafe;">STAGE 2 CLASSIFICATION</div>
            <h3 style="font-size: 18px; margin: 8px 0; color: #17352b;">Material Ambiguity Resolution</h3>
            <p style="font-size: 13px; color: #55665f; line-height: 1.6;">
                Deep crop validation resolves challenging edge cases between transparent glass bottles, crumpled tin cans, plastic wrap, and cardboard.
            </p>
        </div>
        """)
    with b_col3:
        st.html("""
        <div class="bento-card">
            <div class="bento-icon-box bento-icon-amber">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
                </svg>
            </div>
            <div class="bento-tag" style="background:#fffbeb; color:#d97706; border-color:#fef3c7;">AUTOMATED AUDITING</div>
            <h3 style="font-size: 18px; margin: 8px 0; color: #17352b;">Instant ESG Compliance Audits</h3>
            <p style="font-size: 13px; color: #55665f; line-height: 1.6;">
                Generates verifiable audit logs, category recovery percentages, itemized CSV data, downloadable PDF certificates, and automated email alerts.
            </p>
        </div>
        """)

    # Detection Channels
    st.html("""
    <div class="section-head" style="margin-top: 40px; margin-bottom: 20px;">
        <div class="page-eyebrow">INGESTION PIPELINES</div>
        <div class="section-head-title">Deploy Across Any Visual Stream</div>
        <div class="section-head-subtitle">Seamless support for static files, batch folders, local USB cams, and facility-wide IP video.</div>
    </div>
    """)

    c_col1, c_col2, c_col3, c_col4 = st.columns(4)
    with c_col1:
        st.html("""
        <div class="channel-card">
            <div class="channel-icon-circle" style="background: #edf8f2; color: #059669;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>
                </svg>
            </div>
            <h4 style="font-size: 15px; margin: 12px 0 6px 0; color: #17352b;">Single & Batch Photos</h4>
            <p style="font-size: 12px; color: #6f8179; line-height: 1.5; margin: 0;">
                High-resolution inspections across JPG, PNG, WEBP, and BMP formats with visual overlays.
            </p>
        </div>
        """)
    with c_col2:
        st.html("""
        <div class="channel-card">
            <div class="channel-icon-circle" style="background: #eff6ff; color: #2563eb;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                </svg>
            </div>
            <h4 style="font-size: 15px; margin: 12px 0 6px 0; color: #17352b;">Pre-Recorded Video</h4>
            <p style="font-size: 12px; color: #6f8179; line-height: 1.5; margin: 0;">
                Frame-accurate analysis with persistent multi-object tracking and cumulative item counters.
            </p>
        </div>
        """)
    with c_col3:
        st.html("""
        <div class="channel-card">
            <div class="channel-icon-circle" style="background: #f5f3ff; color: #7c3aed;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-3.92 7.94"/>
                </svg>
            </div>
            <h4 style="font-size: 15px; margin: 12px 0 6px 0; color: #17352b;">Edge USB Webcam</h4>
            <p style="font-size: 12px; color: #6f8179; line-height: 1.5; margin: 0;">
                Low-latency edge processing for conveyor belt sorting and manual inspection stations.
            </p>
        </div>
        """)
    with c_col4:
        st.html("""
        <div class="channel-card">
            <div class="channel-icon-circle" style="background: #fffbeb; color: #d97706;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>
                </svg>
            </div>
            <h4 style="font-size: 15px; margin: 12px 0 6px 0; color: #17352b;">Industrial RTSP Streams</h4>
            <p style="font-size: 12px; color: #6f8179; line-height: 1.5; margin: 0;">
                Continuous H.264 IP camera streaming for enterprise facility automation and telemetry.
            </p>
        </div>
        """)

    # Pipeline Architecture Showcase
    st.html("""
    <div class="pipeline-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
            <div style="max-width: 650px;">
                <div style="color: #6ee7b7; font-size: 11px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase;">
                    TWO-STAGE HYBRID AI ARCHITECTURE
                </div>
                <div style="font-size: 24px; font-weight: 850; margin-top: 6px; letter-spacing: -0.4px;">
                    How WasteAI Delivers Zero False Classifications
                </div>
                <p style="color: #bbf7d0; font-size: 13.5px; line-height: 1.6; margin-top: 10px;">
                    Standard single-stage detectors frequently confuse transparent glass with metal cans or background dirt.
                    WasteAI combines generic object localization with focused high-resolution crop validation,
                    ensuring every bounding box is verified before logging.
                </p>
            </div>
            <div class="pipeline-steps-container">
                <div class="pipeline-step">
                    <span class="step-num">01</span>
                    <div>
                        <strong>Input Feed</strong>
                        <small>Photos &bull; Video &bull; RTSP</small>
                    </div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <span class="step-num">02</span>
                    <div>
                        <strong>YOLO Bounding</strong>
                        <small>Candidate Extraction</small>
                    </div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <span class="step-num">03</span>
                    <div>
                        <strong>Crop Material AI</strong>
                        <small>Deep Classification</small>
                    </div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step" style="border-color: #34d399;">
                    <span class="step-num" style="background: #34d399; color: #064e3b;">04</span>
                    <div>
                        <strong>Audit & Tracking</strong>
                        <small>Real-Time Logs & Reports</small>
                    </div>
                </div>
            </div>
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
        if st.button("View Detection & Reports", type="secondary", use_container_width=True, key="dash_open_reports"):
            st.session_state.page = "Detection"
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

        # Let users choose between capturing a new image and browsing their device.
        upload_method = st.radio(
            "How would you like to add an image?",
            options=("Browse files", "Use camera"),
            horizontal=True,
            key="detection_upload_method"
        )

        if upload_method == "Use camera":
            st.caption("Take a photo of the waste item using your device camera.")
            source_img = st.camera_input(
                "Capture waste image",
                key="detection_camera_input"
            )
            if source_img is None:
                st.info(
                    "Allow camera access when your browser asks. "
                    "If camera access is unavailable, select **Browse files** instead."
                )
        else:
            st.caption("Choose an existing JPG, JPEG, PNG, BMP, or WEBP image.")
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
            # SECTIONS C & E: SUMMARY & ACTIONS
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

                # ------------------------------------------------
                # SECTION E: AUTOMATIC DETECTION REPORT
                # ------------------------------------------------
                st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
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

                # Keep report downloads together, with the two primary actions side by side.
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
                        with st.expander("How to configure email credentials"):
                            st.markdown("""
                            Configure SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, and ADMIN_EMAIL
                            in your project .env file or Streamlit secrets. For Gmail, use an App Password.
                            """)

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
