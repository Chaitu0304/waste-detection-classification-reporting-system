from pathlib import Path
import PIL
import pandas as pd
import streamlit as st

import settings
import helper


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WasteAI | Smart Waste Detection",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL + CUSTOM UI STYLING
# ============================================================

st.markdown("""
<style>
    /*  ========================================================
        REMOVE STREAMLIT TOP HEADER
        ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* ========================================================
       GLOBAL APPLICATION
       ======================================================== */

    .stApp {
        background-color: #f7f9f8;
    }

    .main .block-container {
        padding-top: 0rem !important;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    h1,
    h2,
    h3 {
        color: #17352b !important;
        letter-spacing: -0.4px;
    }

    h1 {
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 700 !important;
    }

    h3 {
        font-weight: 650 !important;
    }

    p {
        color: #68736e;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e4ebe7;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }
    /*  ========================================================
        HOME PAGE - FULL WIDTH
        ======================================================== */

    body:has(.home-hero) section[data-testid="stSidebar"] {
        display: none !important;
    }

    body:has(.home-hero) .main .block-container {
        max-width: 1400px;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px;
        min-height: 44px;
        font-weight: 650;
        border: 1px solid #dce7e1;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            background 0.2s ease,
            border-color 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #287653;
        box-shadow: 0 4px 12px rgba(23, 96, 68, 0.10);
    }


    /* Primary buttons */

    .stButton > button[kind="primary"] {
        background: #176044 !important;
        border-color: #176044 !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #0f3d2e !important;
        border-color: #0f3d2e !important;
    }


    /* Download buttons */

    .stDownloadButton > button {
        border-radius: 10px;
        min-height: 44px;
        font-weight: 650;
        border: 1px solid #dce7e1;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        border-color: #287653;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 10px;
        border-color: #dce7e1;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #287653;
        box-shadow: 0 0 0 1px #287653;
    }


    /* Select boxes */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #dce7e1;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 1px dashed #cbd5d0;
        border-radius: 14px;
        padding: 10px;
    }

    [data-testid="stFileUploaderDropzone"] {
        border-radius: 12px;
        background: #fbfdfc;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e4ebe7;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.035);
    }


    /* ========================================================
       DATAFRAMES
       ======================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #e4ebe7;
        border-radius: 12px;
        overflow: hidden;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: none;
        border-top: 1px solid #e4ebe7;
    }


    /* ========================================================
       GENERAL DASHBOARD CARDS
       ======================================================== */

    .dashboard-card {
        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 16px;
        padding: 20px;
        min-height: 130px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.035);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(0, 0, 0, 0.055);
    }

    .card-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 13px;
        font-weight: 650;
        color: #68736e;
        margin-bottom: 5px;
    }

    .card-value {
        font-size: 26px;
        font-weight: 750;
        color: #17352b;
    }


    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 16px;
        padding: 22px;
        min-height: 160px;
        text-align: center;

        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.065);
    }

    .feature-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 650;
        color: #17352b;
        margin-top: 8px;
    }

    .feature-description {
        color: #68736e;
        font-size: 14px;
        margin-top: 8px;
        line-height: 1.5;
    }


    /* ========================================================
       PAGE TITLES
       ======================================================== */

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #17352b;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .main-subtitle {
        font-size: 17px;
        color: #68736e;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #17352b;
        margin-top: 30px;
        margin-bottom: 15px;
    }


    /* ========================================================
       STATUS BADGE
       ======================================================== */

    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        background-color: #eaf7ef;
        color: #237a45;
        font-size: 13px;
        font-weight: 650;
    }


    /*  ========================================================
        DASHBOARD HERO
        ======================================================== */

    .dashboard-hero {
        background: #ffffff;
        border: 1px solid #e1e9e5;
        border-radius: 20px;

        padding: 32px 36px;
        margin-bottom: 18px;

        color: #17352b;
        min-height: 210px;

        display: flex;
        align-items: center;

        box-shadow: 0 6px 20px rgba(23, 53, 43, 0.06);
    }

    .hero-brand {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.8px;

        color: #2f9d73;

        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 38px;
        line-height: 1.08;
        font-weight: 800;

        letter-spacing: -1.2px;

        margin-bottom: 10px;

        color: #17352b;
    }

    .hero-description {
        font-size: 16px;
        line-height: 1.6;

        max-width: 680px;

        color: #68736e;
    }

    .hero-tags {
        display: flex;
        gap: 8px;

        margin-top: 18px;

        flex-wrap: wrap;
    }

    .hero-tags span {
        background: #eef8f3;

        border: 1px solid #d7ebe2;

        border-radius: 20px;

        padding: 6px 12px;

        font-size: 12px;
        font-weight: 600;

        color: #277a5b;
    }


    /*  ========================================================
        DASHBOARD WELCOME
        ======================================================== */

    .dashboard-welcome {
        padding: 4px 0 6px 0;
    }

    .welcome-label {
        font-size: 11px;
        font-weight: 800;

        letter-spacing: 1.2px;
        text-transform: uppercase;

        color: #2f8d68;

        margin-bottom: 6px;
    }

    .welcome-title {
        font-size: 25px;
        line-height: 1.2;

        font-weight: 750;

        color: #17352b;

        margin-top: 0;
        margin-bottom: 5px;
    }

    .welcome-text {
        color: #71807a;

        font-size: 14px;
        line-height: 1.5;

        margin-top: 0;
    }

    /* ========================================================
       DASHBOARD STAT CARDS
       ======================================================== */

    .stat-card {
        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;

        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.035);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(0, 0, 0, 0.055);
    }

    .stat-icon {
        font-size: 22px;
        margin-bottom: 10px;
    }

    .stat-value {
        font-size: 25px;
        font-weight: 750;
        color: #17352b;
    }

    .stat-category {
        font-size: 20px;
        text-transform: capitalize;
    }

    .stat-label {
        color: #7a8580;
        font-size: 12px;
        margin-top: 4px;
    }


    /* ========================================================
       DETECTION SOURCE CARDS
       ======================================================== */

    .source-card {
        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 14px;

        padding: 20px;
        min-height: 145px;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .source-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
    }

    .source-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .source-title {
        font-size: 16px;
        font-weight: 700;
        color: #17352b;
        margin-bottom: 6px;
    }

    .source-description {
        font-size: 13px;
        line-height: 1.5;
        color: #75817b;
    }


    /* ========================================================
       RECENT ANALYSIS
       ======================================================== */

    .analysis-row {
        display: flex;
        align-items: center;
        justify-content: space-between;

        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 10px;

        padding: 14px 18px;
        margin-bottom: 8px;
    }

    .analysis-row strong {
        display: block;
        font-size: 14px;
        text-transform: capitalize;
        color: #17352b;
    }

    .analysis-row span {
        display: block;
        color: #7a8580;
        font-size: 12px;
        margin-top: 3px;
    }

    .confidence {
        font-weight: 700;
        font-size: 13px;
        color: #287653;
    }


    /* ========================================================
       EMPTY STATES
       ======================================================== */

    .empty-card {
        background: #ffffff;
        border: 1px dashed #ccd9d3;
        border-radius: 14px;

        padding: 35px 20px;
        text-align: center;
    }

    .empty-icon {
        font-size: 30px;
    }

    .empty-title {
        font-size: 16px;
        font-weight: 700;
        color: #17352b;
        margin-top: 8px;
    }

    .empty-text {
        color: #7a8580;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ========================================================
       CATEGORY PANEL
       ======================================================== */

    .category-panel {
        background: #ffffff;
        border: 1px solid #e4ebe7;
        border-radius: 14px;
        padding: 8px;
    }

    .category-item {
        display: flex;
        align-items: center;

        padding: 11px 12px;

        border-bottom: 1px solid #eef2f0;

        font-size: 14px;
        font-weight: 600;
        color: #30433b;
    }

    .category-item:last-child {
        border-bottom: none;
    }

    .category-icon {
        font-size: 20px;
        width: 38px;
    }


    /* ========================================================
       RESPONSIVE ADJUSTMENTS
       ======================================================== */

    @media (max-width: 900px) {

        .main-title {
            font-size: 34px;
        }

        .hero-title {
            font-size: 32px;
        }

        .dashboard-hero {
            padding: 30px;
        }

    }


    @media (max-width: 600px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .dashboard-hero {
            padding: 25px;
            border-radius: 16px;
        }

        .hero-title {
            font-size: 28px;
        }

        .hero-description {
            font-size: 14px;
        }

        .main-title {
            font-size: 30px;
        }

        .main-subtitle {
            font-size: 15px;
        }

    }
/* ============================================================
   WASTEAI — TOP NAVIGATION
   ============================================================ */

/* ------------------------------------------------------------
   STREAMLIT CLEANUP
   ------------------------------------------------------------ */

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

/* Hide old sidebar */
section[data-testid="stSidebar"] {
    display: none !important;
}


/* ============================================================
   MAIN APPLICATION
   ============================================================ */

.stApp {
    background: #f7f9f8;
}

.main .block-container {
    max-width: 1500px;

    padding-top: 0.5rem !important;
    padding-bottom: 3rem !important;
}


/* ============================================================
   WASTEAI BRAND
   ============================================================ */

.wa-top-brand {
    display: flex;

    align-items: center;

    gap: 12px;

    height: 56px;

    padding-left: 4px;
}


.wa-top-logo {
    width: 42px;
    height: 42px;

    display: flex;

    align-items: center;
    justify-content: center;

    flex-shrink: 0;

    border-radius: 12px;

    background: #e9f6ef;

    border: 1px solid #d5e9de;

    color: #176044;

    font-size: 24px;

    font-weight: 800;
}


.wa-top-brand-text {
    display: flex;

    flex-direction: column;

    justify-content: center;
}


.wa-top-brand-name {
    color: #17352b;

    font-size: 21px;

    font-weight: 800;

    line-height: 1.1;

    letter-spacing: -0.4px;
}


.wa-top-brand-subtitle {
    color: #7a8782;

    font-size: 10px;

    font-weight: 500;

    margin-top: 4px;

    line-height: 1.1;
}


/* ============================================================
   NAVIGATION BUTTON AREA
   ============================================================ */

/*
   The navigation uses:

   st.columns(
       [2.4, 1, 1, 1, 1, 1, 1]
   )

   First column = WasteAI
   Remaining columns = navigation buttons
*/


/* Navigation buttons */

.stButton {
    margin-top: 5px;
}


.stButton > button {

    height: 42px;

    min-height: 42px;

    width: 100%;

    padding: 0 10px;

    border-radius: 10px;

    border: 1px solid transparent !important;

    background: transparent !important;

    color: #64736c !important;

    font-size: 13px;

    font-weight: 650;

    letter-spacing: 0;

    box-shadow: none !important;

    transition:
        background 0.18s ease,
        color 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease;
}


/* ------------------------------------------------------------
   NAVIGATION HOVER
   ------------------------------------------------------------ */

.stButton > button:hover {

    background: #eaf5ef !important;

    border-color: #d7e9df !important;

    color: #176044 !important;

    transform: translateY(-1px);

    box-shadow: none !important;
}


/* ------------------------------------------------------------
   NAVIGATION FOCUS
   ------------------------------------------------------------ */

.stButton > button:focus {

    outline: none !important;

    box-shadow:
        0 0 0 2px rgba(23, 96, 68, 0.12) !important;
}


/* ============================================================
   NAVIGATION DIVIDER
   ============================================================ */

.wa-top-divider {

    width: 100%;

    height: 1px;

    background: #e1e9e5;

    margin-top: 7px;

    margin-bottom: 28px;
}


/* ============================================================
   GENERAL PRIMARY BUTTONS
   ============================================================ */

/*
   Keep primary buttons separate from navigation styling.
*/

.stButton > button[kind="primary"] {

    background: #176044 !important;

    border-color: #176044 !important;

    color: #ffffff !important;
}


.stButton > button[kind="primary"]:hover {

    background: #0f3d2e !important;

    border-color: #0f3d2e !important;

    color: #ffffff !important;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {

    background: #ffffff;

    border: 1px solid #e3ebe7;

    border-radius: 15px;

    padding: 20px;

    box-shadow:
        0 3px 12px rgba(20, 55, 43, 0.04);
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

    .main .block-container {

        padding-left: 1.2rem !important;

        padding-right: 1.2rem !important;
    }


    .wa-top-brand-name {

        font-size: 19px;
    }


    .wa-top-brand-subtitle {

        display: none;
    }


    .stButton > button {

        font-size: 12px;

        padding-left: 5px;

        padding-right: 5px;
    }
}


@media (max-width: 750px) {

    .main .block-container {

        padding-left: 0.8rem !important;

        padding-right: 0.8rem !important;
    }


    .wa-top-logo {

        width: 36px;

        height: 36px;

        font-size: 20px;
    }


    .wa-top-brand-name {

        font-size: 17px;
    }


    .stButton > button {

        font-size: 11px;

        padding-left: 2px;

        padding-right: 2px;
    }
}
/* ========================================================
   HOME PAGE
   ======================================================== */

.home-hero {
    position: relative;
    min-height: 460px;
    padding: 58px 60px;
    margin-bottom: 55px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-radius: 28px;

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(48, 173, 116, 0.16),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #f4faf7 0%,
            #eef7f2 100%
        );

    border: 1px solid #dcebe4;
    overflow: hidden;
}


.home-hero-content {
    max-width: 700px;
    position: relative;
    z-index: 2;
}


.home-badge {
    display: inline-block;

    padding: 8px 14px;
    margin-bottom: 22px;

    border-radius: 30px;

    background: #e5f5ed;
    border: 1px solid #cfe9dc;

    color: #16704f;

    font-size: 12px;
    font-weight: 750;
    letter-spacing: 0.7px;
}


.home-hero h1 {
    margin: 0;

    font-size: 54px;
    line-height: 1.04;

    letter-spacing: -2px;

    font-weight: 800;

    color: #12382d;
}


.home-hero h1 span {
    color: #1c8a61;
}


.home-hero p {
    max-width: 650px;

    margin-top: 22px;

    font-size: 18px;
    line-height: 1.7;

    color: #61716b;
}


.home-actions {
    display: flex;
    gap: 14px;

    margin-top: 30px;
}


.home-primary,
.home-secondary {
    padding: 13px 22px;

    border-radius: 10px;

    font-size: 14px;
    font-weight: 700;

    cursor: pointer;
}


.home-primary {
    background: #176b4d;
    color: white;
}


.home-secondary {
    background: white;
    color: #176b4d;

    border: 1px solid #cfe2d9;
}


.home-visual {
    width: 340px;

    display: flex;
    justify-content: center;

    position: relative;
    z-index: 2;
}


.home-visual-card {
    width: 300px;

    padding: 30px;

    border-radius: 22px;

    background: rgba(255,255,255,0.92);

    border: 1px solid #dce9e3;

    box-shadow:
        0 20px 45px rgba(25, 76, 57, 0.10);
}


.visual-icon {
    width: 62px;
    height: 62px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;

    background: #e8f7ef;

    font-size: 30px;

    margin-bottom: 20px;
}


.visual-title {
    font-size: 20px;
    font-weight: 800;

    color: #14382d;
}


.visual-status {
    margin-top: 12px;

    font-size: 13px;
    color: #64736e;
}


.visual-status span {
    display: inline-block;

    width: 9px;
    height: 9px;

    margin-right: 7px;

    border-radius: 50%;

    background: #32aa72;
}


.visual-stats {
    display: flex;

    gap: 15px;

    margin-top: 28px;
    padding-top: 20px;

    border-top: 1px solid #e6eeea;
}


.visual-stats div {
    flex: 1;
}


.visual-stats strong {
    display: block;

    font-size: 20px;

    color: #163c30;
}


.visual-stats small {
    color: #8a9692;

    font-size: 10px;
}


/* ========================================================
   HOME SECTION HEADINGS
   ======================================================== */

.home-section-heading {
    margin-bottom: 25px;
}


.home-eyebrow {
    margin-bottom: 8px;

    color: #25805f;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.2px;
}


.home-section-heading h2 {
    margin: 0;

    font-size: 30px;
    font-weight: 800;

    color: #143a2e;
}


.home-section-heading p {
    margin-top: 8px;

    color: #7a8782;

    font-size: 15px;
}


.home-input-heading {
    margin-top: 55px;
}


/* ========================================================
   HOME FEATURE CARDS
   ======================================================== */

.home-feature-card {
    min-height: 190px;

    padding: 28px;

    border-radius: 18px;

    background: white;

    border: 1px solid #e0eae5;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.home-feature-card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 14px 30px rgba(26, 76, 57, 0.09);
}


.home-feature-icon {
    width: 50px;
    height: 50px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 20px;

    border-radius: 14px;

    background: #edf8f3;

    font-size: 25px;
}


.home-feature-card h3 {
    margin: 0;

    color: #173c30;

    font-size: 18px;
    font-weight: 750;
}


.home-feature-card p {
    margin-top: 9px;

    color: #78857f;

    font-size: 13px;
    line-height: 1.6;
}


/* ========================================================
   HOME INPUT CARDS
   ======================================================== */

.home-input-card {
    min-height: 150px;

    padding: 24px;

    background: white;

    border: 1px solid #e0eae5;

    border-radius: 17px;
}


.home-input-icon {
    font-size: 27px;

    margin-bottom: 15px;
}


.home-input-card strong {
    display: block;

    font-size: 16px;

    color: #173c30;
}


.home-input-card p {
    margin-top: 7px;

    font-size: 12px;
    line-height: 1.5;

    color: #82908a;
}


/* ========================================================
   HOME TECHNOLOGY SECTION
   ======================================================== */

.home-tech {
    margin-top: 60px;
    margin-bottom: 40px;

    padding: 38px 42px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-radius: 22px;

    background: #123d30;

    color: white;
}


.home-tech h2 {
    margin: 0;

    max-width: 650px;

    font-size: 28px;
    line-height: 1.2;
}


.home-tech p {
    max-width: 650px;

    margin-top: 12px;

    color: #bdd0c8;

    line-height: 1.6;
}


.home-tech .home-eyebrow {
    color: #76c9a3;
}


.home-tech-badge {
    min-width: 190px;

    padding: 24px;

    border-radius: 16px;

    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.12);
}


.tech-model {
    font-size: 25px;
    font-weight: 800;
}


.tech-label {
    margin-top: 5px;

    font-size: 12px;

    color: #a9c1b7;
}


.tech-status {
    margin-top: 20px;

    font-size: 12px;

    color: #7bd0a5;
}
/* ============================================================
   DASHBOARD
   ============================================================ */

.dashboard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 24px;
}

.dashboard-eyebrow {
    color: #4d8a70;

    font-size: 11px;
    font-weight: 750;

    letter-spacing: 1.4px;

    margin-bottom: 5px;
}

.dashboard-header h1 {
    margin: 0;

    color: #17352b;

    font-size: 32px;
    font-weight: 800;

    letter-spacing: -0.8px;
}

.dashboard-header p {
    margin: 6px 0 0;

    color: #75817c;

    font-size: 14px;
}

.dashboard-online {
    display: flex;
    align-items: center;
    gap: 8px;

    padding: 9px 14px;

    border-radius: 20px;

    background: #edf8f2;

    border: 1px solid #d9eee2;

    color: #176044;

    font-size: 12px;
    font-weight: 700;
}

.dashboard-status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #35a56f;

    display: inline-block;

    box-shadow: 0 0 0 3px rgba(53, 165, 111, 0.12);
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.dashboard-kpi {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 20px 21px;

    min-height: 125px;

    box-shadow:
        0 3px 14px rgba(20, 55, 43, 0.04);
}

.dashboard-kpi-label {
    color: #7b8782;

    font-size: 10px;
    font-weight: 750;

    letter-spacing: 1px;
}

.dashboard-kpi-value {
    color: #17352b;

    font-size: 29px;
    font-weight: 800;

    margin-top: 10px;

    letter-spacing: -0.7px;
}

.dashboard-category {
    font-size: 22px;
}

.dashboard-kpi-meta {
    color: #9aa49f;

    font-size: 11px;

    margin-top: 7px;
}


/* ============================================================
   SECTION CARDS
   ============================================================ */

.dashboard-section-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 20px;

    box-shadow:
        0 3px 14px rgba(20, 55, 43, 0.04);
}

.dashboard-section-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 750;
}

.dashboard-section-subtitle {
    color: #87918c;

    font-size: 12px;

    margin-top: 4px;

    margin-bottom: 18px;
}


/* ============================================================
   ACTIVITY
   ============================================================ */

.dashboard-activity-row {
    display: flex;

    align-items: center;

    gap: 12px;

    padding: 12px 0;

    border-top: 1px solid #edf1ef;
}

.dashboard-activity-icon {
    width: 34px;
    height: 34px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background: #edf7f2;

    color: #176044;

    font-size: 17px;
}

.dashboard-activity-info {
    flex: 1;
}

.dashboard-activity-title {
    color: #30433b;

    font-size: 13px;
    font-weight: 700;
}

.dashboard-activity-source {
    color: #929d98;

    font-size: 11px;

    margin-top: 2px;
}

.dashboard-activity-confidence {
    color: #176044;

    font-size: 12px;
    font-weight: 700;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.dashboard-empty {
    text-align: center;

    padding: 35px 10px;
}

.dashboard-empty-icon {
    color: #b1bcb6;

    font-size: 30px;
}

.dashboard-empty-title {
    color: #52615a;

    font-size: 13px;
    font-weight: 700;

    margin-top: 8px;
}

.dashboard-empty-text {
    color: #9aa49f;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   SYSTEM STATUS
   ============================================================ */

.dashboard-status-item {
    display: flex;

    align-items: center;

    gap: 10px;

    padding: 13px 0;

    border-top: 1px solid #edf1ef;
}

.dashboard-status-item > div {
    flex: 1;
}

.dashboard-status-item strong {
    display: block;

    color: #30433b;

    font-size: 12px;
}

.dashboard-status-item small {
    display: block;

    color: #929d98;

    font-size: 10px;

    margin-top: 2px;
}

.dashboard-status-ready {
    color: #176044;

    font-size: 10px;
    font-weight: 750;
}


/* ============================================================
   QUICK ACTIONS
   ============================================================ */

.dashboard-quick-title {
    color: #17352b;

    font-size: 16px;
    font-weight: 750;

    margin-top: 25px;
    margin-bottom: 10px;
}
/* ============================================================
   DETECTION PAGE
   ============================================================ */

.detection-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    background: #ffffff;

    border: 1px solid #e1e9e5;
    border-radius: 18px;

    padding: 24px 28px;

    margin-bottom: 22px;

    box-shadow:
        0 4px 16px rgba(20,55,43,.04);
}

.detection-eyebrow {
    color: #4d8a70;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.4px;
}

.detection-title {
    color: #17352b;

    font-size: 30px;
    font-weight: 800;

    letter-spacing: -.7px;

    margin-top: 5px;
}

.detection-description {
    color: #75817b;

    font-size: 13px;

    margin-top: 5px;
}

.detection-engine-status {
    display: flex;
    align-items: center;
    gap: 8px;

    padding: 9px 13px;

    border-radius: 999px;

    background: #edf7f1;

    border: 1px solid #d7ecdf;

    color: #287653;

    font-size: 11px;
    font-weight: 750;

    white-space: nowrap;
}

.detection-engine-status span,
.detection-model-status span {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #35a56f;

    display: inline-block;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.detection-section-heading {
    margin-bottom: 10px;
}

.detection-section-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 750;
}

.detection-section-subtitle {
    color: #87918c;

    font-size: 12px;

    margin-top: 3px;
}


/* ============================================================
   CONFIGURATION
   ============================================================ */

.detection-config-card,
.detection-model-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.detection-config-card {
    display: flex;

    align-items: center;

    gap: 12px;

    padding: 16px 18px 4px;
}

.detection-config-icon {
    width: 38px;
    height: 38px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: #edf7f1;

    font-size: 19px;
}

.detection-config-title {
    color: #30433b;

    font-size: 13px;
    font-weight: 750;
}

.detection-config-description {
    color: #8a9590;

    font-size: 11px;

    margin-top: 2px;
}


/* ============================================================
   MODEL
   ============================================================ */

.detection-model-card {
    padding: 17px;

    min-height: 91px;
}

.detection-model-icon {
    font-size: 20px;
}

.detection-model-name {
    color: #17352b;

    font-size: 14px;
    font-weight: 750;

    margin-top: 5px;
}

.detection-model-status {
    display: flex;

    align-items: center;

    gap: 6px;

    color: #287653;

    font-size: 10px;
    font-weight: 700;

    margin-top: 4px;
}


/* ============================================================
   WORKSPACE
   ============================================================ */

.detection-workspace-header {
    display: flex;

    align-items: center;
    justify-content: space-between;

    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 19px 22px;

    margin-top: 14px;
    margin-bottom: 14px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.detection-workspace-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 800;
}

.detection-workspace-description {
    color: #7d8984;

    font-size: 12px;

    margin-top: 4px;
}

.detection-workspace-badge {
    background: #edf7f1;

    border: 1px solid #d7ecdf;

    color: #287653;

    border-radius: 999px;

    padding: 6px 10px;

    font-size: 10px;
    font-weight: 700;

    white-space: nowrap;
}


/* ============================================================
   UPLOAD
   ============================================================ */

.detection-upload-card {
    background: #ffffff;

    border: 1.5px dashed #b9ccc2;

    border-radius: 18px;

    padding: 50px 25px;

    text-align: center;

    margin-top: 8px;
}

.detection-upload-icon {
    width: 66px;
    height: 66px;

    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 17px;

    background: #edf7f1;

    font-size: 30px;
}

.detection-upload-title {
    color: #17352b;

    font-size: 18px;
    font-weight: 800;

    margin-top: 13px;
}

.detection-upload-description {
    color: #7d8984;

    font-size: 12px;

    margin-top: 5px;
}

.detection-upload-formats {
    color: #a0aaa5;

    font-size: 10px;

    margin-top: 10px;
}


/* ============================================================
   ANALYSIS WORKSPACE
   ============================================================ */

.detection-analysis-heading {
    color: #17352b;

    font-size: 16px;
    font-weight: 750;

    margin-top: 18px;
    margin-bottom: 10px;
}

.detection-panel-label {
    color: #30433b;

    font-size: 12px;
    font-weight: 700;

    margin-bottom: 7px;
}

.detection-image-panel {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 10px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.detection-analysis-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 25px;

    min-height: 300px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.detection-analysis-icon {
    width: 54px;
    height: 54px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    background: #edf7f1;

    font-size: 26px;
}

.detection-analysis-title {
    color: #17352b;

    font-size: 19px;
    font-weight: 800;

    margin-top: 17px;
}

.detection-analysis-text {
    color: #7b8782;

    font-size: 12px;

    line-height: 1.6;

    margin-top: 6px;
}

.detection-threshold-box {
    display: flex;

    justify-content: space-between;

    align-items: center;

    background: #f5f9f7;

    border-radius: 10px;

    padding: 11px 13px;

    margin-top: 18px;

    color: #68736e;

    font-size: 11px;
}

.detection-threshold-box strong {
    color: #287653;

    font-size: 12px;
}


/* ============================================================
   RESULTS
   ============================================================ */

.detection-result-header {
    display: flex;

    align-items: center;
    justify-content: space-between;

    margin-top: 18px;

    margin-bottom: 10px;
}

.detection-result-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 800;
}

.detection-result-subtitle {
    color: #87918c;

    font-size: 11px;

    margin-top: 3px;
}

.detection-result-badge {
    background: #edf7f1;

    border: 1px solid #d7ecdf;

    color: #287653;

    border-radius: 999px;

    padding: 6px 10px;

    font-size: 10px;
    font-weight: 700;
}

.detection-result-image {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 16px;

    padding: 10px;

    box-shadow:
        0 4px 15px rgba(20,55,43,.04);
}


/* ============================================================
   SUMMARY
   ============================================================ */

.detection-summary-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 800;

    margin-bottom: 10px;
}

.detection-summary-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 18px;

    min-height: 112px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.detection-summary-icon {
    font-size: 21px;
}

.detection-summary-label {
    color: #7a8580;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   PRIMARY DETECTION BUTTON
   ============================================================ */

.stButton > button[kind="primary"] {
    background: #176044 !important;

    border-color: #176044 !important;

    color: #ffffff !important;

    min-height: 44px;

    border-radius: 10px;

    font-weight: 700;
}

.stButton > button[kind="primary"]:hover {
    background: #0f3d2e !important;

    border-color: #0f3d2e !important;
}
/* ============================================================
   ANALYTICS PAGE
   ============================================================ */

.analytics-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    background: #ffffff;

    border: 1px solid #e1e9e5;
    border-radius: 18px;

    padding: 25px 28px;

    margin-bottom: 22px;

    box-shadow:
        0 4px 16px rgba(20,55,43,.04);
}

.analytics-eyebrow {
    color: #4d8a70;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.4px;
}

.analytics-title {
    color: #17352b;

    font-size: 30px;
    font-weight: 800;

    margin-top: 5px;

    letter-spacing: -.7px;
}

.analytics-description {
    color: #75817b;

    font-size: 13px;

    margin-top: 5px;
}

.analytics-status {
    display: flex;
    align-items: center;
    gap: 7px;

    background: #edf7f1;

    border: 1px solid #d7ecdf;

    border-radius: 999px;

    padding: 8px 12px;

    color: #287653;

    font-size: 11px;
    font-weight: 750;
}

.analytics-status span {
    width: 7px;
    height: 7px;

    background: #35a56f;

    border-radius: 50%;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.analytics-empty {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 18px;

    padding: 55px 30px;

    text-align: center;

    box-shadow:
        0 4px 16px rgba(20,55,43,.035);
}

.analytics-empty-icon {
    width: 70px;
    height: 70px;

    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #edf7f1;

    border-radius: 20px;

    font-size: 32px;
}

.analytics-empty-title {
    color: #17352b;

    font-size: 21px;
    font-weight: 800;

    margin-top: 17px;
}

.analytics-empty-text {
    color: #7b8782;

    font-size: 13px;

    max-width: 520px;

    margin: 7px auto 0;

    line-height: 1.6;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.analytics-section-heading {
    margin-bottom: 11px;
}

.analytics-spacing {
    margin-top: 24px;
}

.analytics-section-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 800;
}

.analytics-section-subtitle {
    color: #87918c;

    font-size: 12px;

    margin-top: 3px;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.analytics-kpi {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 17px;

    min-height: 135px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.analytics-kpi-icon {
    font-size: 21px;
}

.analytics-kpi-label {
    color: #7b8782;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .7px;

    margin-top: 9px;
}

.analytics-kpi-value {
    color: #17352b;

    font-size: 28px;
    font-weight: 850;

    margin-top: 2px;
}

.analytics-kpi-category {
    color: #287653;

    font-size: 18px;
    font-weight: 850;

    margin-top: 5px;

    overflow-wrap: anywhere;
}

.analytics-kpi-subtext {
    color: #9aa39f;

    font-size: 10px;

    margin-top: 2px;
}


/* ============================================================
   CHART CARD
   ============================================================ */

.analytics-chart-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 18px 20px 8px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.analytics-card-title {
    color: #17352b;

    font-size: 15px;
    font-weight: 800;
}

.analytics-card-description {
    color: #87918c;

    font-size: 11px;

    margin-top: 3px;
}


/* ============================================================
   AI INSIGHT
   ============================================================ */

.analytics-insight {
    background: #17352b;

    border-radius: 16px;

    padding: 22px;

    min-height: 285px;

    box-shadow:
        0 6px 18px rgba(20,55,43,.10);
}

.analytics-insight-label {
    color: #a9c5b7;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1px;
}

.analytics-insight-title {
    color: #ffffff;

    font-size: 17px;
    font-weight: 750;

    margin-top: 18px;
}

.analytics-insight-category {
    color: #ffffff;

    font-size: 26px;
    font-weight: 850;

    margin-top: 5px;

    overflow-wrap: anywhere;
}

.analytics-insight-divider {
    height: 1px;

    background: rgba(255,255,255,.14);

    margin: 20px 0;
}

.analytics-insight-small {
    color: #b6c9c0;

    font-size: 11px;
}

.analytics-insight-percentage {
    color: #ffffff;

    font-size: 31px;
    font-weight: 850;

    margin-top: 2px;
}

.analytics-insight-footer {
    color: #8faea0;

    font-size: 10px;

    margin-top: 17px;
}


/* ============================================================
   CONFIDENCE
   ============================================================ */

.analytics-confidence-card {
    display: flex;
    align-items: center;

    gap: 14px;

    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 17px 20px;

    margin-top: 18px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.analytics-confidence-icon {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #edf7f1;

    border-radius: 11px;

    font-size: 21px;
}

.analytics-confidence-title {
    color: #17352b;

    font-size: 13px;
    font-weight: 800;
}

.analytics-confidence-text {
    color: #7b8782;

    font-size: 11px;

    margin-top: 3px;
}

.analytics-confidence-text strong {
    color: #287653;
}
/* ============================================================
   REPORTS PAGE
   ============================================================ */

.reports-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    background: #ffffff;

    border: 1px solid #e1e9e5;
    border-radius: 18px;

    padding: 25px 28px;

    margin-bottom: 22px;

    box-shadow:
        0 4px 16px rgba(20,55,43,.04);
}

.reports-eyebrow {
    color: #4d8a70;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.4px;
}

.reports-title {
    color: #17352b;

    font-size: 30px;
    font-weight: 800;

    letter-spacing: -.7px;

    margin-top: 5px;
}

.reports-description {
    color: #75817b;

    font-size: 13px;

    margin-top: 5px;
}

.reports-status {
    display: flex;
    align-items: center;

    gap: 7px;

    padding: 8px 12px;

    background: #edf7f1;

    border: 1px solid #d7ecdf;

    border-radius: 999px;

    color: #287653;

    font-size: 11px;
    font-weight: 750;
}

.reports-status span {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #35a56f;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.reports-empty {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 18px;

    padding: 55px 30px;

    text-align: center;

    box-shadow:
        0 4px 16px rgba(20,55,43,.035);
}

.reports-empty-icon {
    width: 70px;
    height: 70px;

    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #edf7f1;

    border-radius: 20px;

    font-size: 31px;
}

.reports-empty-title {
    color: #17352b;

    font-size: 21px;
    font-weight: 800;

    margin-top: 17px;
}

.reports-empty-text {
    color: #7b8782;

    font-size: 13px;

    line-height: 1.6;

    max-width: 520px;

    margin: 7px auto 0;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.reports-section-heading {
    margin-bottom: 11px;
}

.reports-spacing {
    margin-top: 25px;
}

.reports-section-title {
    color: #17352b;

    font-size: 17px;
    font-weight: 800;
}

.reports-section-subtitle {
    color: #87918c;

    font-size: 12px;

    margin-top: 3px;
}


/* ============================================================
   SUMMARY CARDS
   ============================================================ */

.reports-summary-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 18px;

    min-height: 130px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.reports-summary-icon {
    font-size: 21px;
}

.reports-summary-label {
    color: #7b8782;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .7px;

    margin-top: 9px;
}

.reports-summary-value {
    color: #17352b;

    font-size: 28px;
    font-weight: 850;

    margin-top: 3px;
}

.reports-summary-category {
    color: #287653;

    font-size: 20px;
    font-weight: 850;

    margin-top: 5px;

    overflow-wrap: anywhere;
}

.reports-summary-text {
    color: #9aa39f;

    font-size: 10px;

    margin-top: 2px;
}


/* ============================================================
   EXPORT
   ============================================================ */

.reports-export-card {
    display: flex;
    align-items: center;

    gap: 14px;

    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 15px;

    padding: 18px 20px;

    margin-top: 18px;

    box-shadow:
        0 3px 12px rgba(20,55,43,.035);
}

.reports-export-icon {
    width: 44px;
    height: 44px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #edf7f1;

    border-radius: 12px;

    font-size: 22px;
}

.reports-export-title {
    color: #17352b;

    font-size: 14px;
    font-weight: 800;
}

.reports-export-description {
    color: #7b8782;

    font-size: 11px;

    line-height: 1.5;

    margin-top: 3px;
}


/* ============================================================
   REPORT INFORMATION
   ============================================================ */

.reports-info-card {
    background: #ffffff;

    border: 1px solid #e1e9e5;

    border-radius: 14px;

    padding: 16px 18px;

    margin-top: 16px;
}

.reports-info-label {
    color: #8a9590;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .8px;
}

.reports-info-value {
    color: #30433b;

    font-size: 13px;
    font-weight: 700;

    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP NAVIGATION
# ============================================================

pages = [
    ("🏠", "Home"),
    ("📊", "Dashboard"),
    ("🔍", "Detection"),
    ("📈", "Analytics"),
    ("📄", "Reports"),
    ("⚙️", "Settings")
]

page_labels = [
    f"{icon} {name}"
    for icon, name in pages
]


# ============================================================
# DEFAULT PAGE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"


# ============================================================
# TOP NAVIGATION
# ============================================================

nav_columns = st.columns([2.2, 1, 1, 1, 1, 1, 1])

# ------------------------------------------------------------
# BRAND
# ------------------------------------------------------------

with nav_columns[0]:

    st.html(
        """
        <div class="wa-top-brand">

            <div class="wa-top-logo">
                ♻
            </div>

            <div>
                <div class="wa-top-brand-name">
                    WasteAI
                </div>

                <div class="wa-top-brand-subtitle">
                    Smart Waste Intelligence
                </div>
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# NAVIGATION BUTTONS
# ------------------------------------------------------------

for i, (icon, name) in enumerate(pages):

    with nav_columns[i + 1]:

        label = f"{icon} {name}"

        if st.button(
            label,
            key=f"top_nav_{name.lower()}",
            use_container_width=True
        ):

            st.session_state.page = label
            st.rerun()


# ------------------------------------------------------------
# NAVIGATION DIVIDER
# ------------------------------------------------------------

st.html(
    """
    <div class="wa-top-divider"></div>
    """
)


# Current page

page = st.session_state.page
# ============================================================
# LOAD MODEL
# ============================================================

model_path = Path(settings.DETECTION_MODEL)

try:
    model = helper.load_model(model_path)
except Exception as ex:
    model = None
    st.error(f"Unable to load model: {model_path}")
    st.error(ex)

# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    # ========================================================
    # HOME HERO
    # ========================================================

    st.html(
        """
        <div class="home-hero">

            <div class="home-hero-content">

                <div class="home-badge">
                    ♻️ WASTEAI &nbsp;•&nbsp; AI-POWERED WASTE INTELLIGENCE
                </div>

                <h1>
                    Smarter Waste.<br>
                    <span>Cleaner Future.</span>
                </h1>

                <p>
                    WasteAI uses AI-powered computer vision to detect,
                    classify and analyze waste from images, videos
                    and live camera streams.
                </p>

            </div>

            <div class="home-visual">

                <div class="home-visual-card">

                    <div class="visual-icon">♻️</div>

                    <div class="visual-title">
                        AI Waste Detection
                    </div>

                    <div class="visual-status">
                        <span></span>
                        YOLOv8 Engine Ready
                    </div>

                    <div class="visual-stats">

                        <div>
                            <strong>6+</strong>
                            <small>Waste Classes</small>
                        </div>

                        <div>
                            <strong>4</strong>
                            <small>Input Sources</small>
                        </div>

                        <div>
                            <strong>AI</strong>
                            <small>Powered</small>
                        </div>

                    </div>

                </div>

            </div>

        </div>
        """,

    )


    # ========================================================
    # HERO ACTIONS
    # ========================================================

    home_col1, home_col2 = st.columns([1, 1])

    with home_col1:

        if st.button(
            "🔍  Start Waste Detection",
            type="primary",
            use_container_width=True,
            key="home_start_detection"
        ):
            st.session_state.page = "🔍 Detection"
            st.rerun()

    with home_col2:

        if st.button(
            "📊  View Dashboard",
            use_container_width=True,
            key="home_view_dashboard"
        ):
            st.session_state.page = "📊 Dashboard"
            st.rerun()
    # ========================================================
    # WHAT WASTEAI DOES
    # ========================================================

    st.html(
        """
        <div class="home-section-heading">
            <div class="home-eyebrow">WHAT WASTEAI DOES</div>
            <h2>Intelligent waste analysis in one platform</h2>
            <p>
                Detect waste, understand its category and generate
                meaningful analysis using computer vision.
            </p>
        </div>
        """
    )


    feature_cols = st.columns(3)

    features = [
        (
            "🔍",
            "Detect Waste",
            "Identify waste objects automatically using YOLOv8 computer vision."
        ),
        (
            "🗂️",
            "Classify Materials",
            "Recognize different waste categories such as plastic, glass, metal and paper."
        ),
        (
            "📊",
            "Analyze Results",
            "View detection statistics, confidence scores and generated reports."
        )
    ]

    for col, (icon, title, description) in zip(
        feature_cols,
        features
    ):

        with col:

            st.html(
                f"""
                <div class="home-feature-card">

                    <div class="home-feature-icon">
                        {icon}
                    </div>

                    <h3>{title}</h3>

                    <p>{description}</p>

                </div>
                """
            )


    # ========================================================
    # SUPPORTED INPUTS
    # ========================================================

    st.html(
        """
        <div class="home-section-heading home-input-heading">
            <div class="home-eyebrow">ANALYSIS SOURCES</div>
            <h2>Analyze waste from any source</h2>
        </div>
        """
    )


    input_cols = st.columns(4)

    inputs = [
        ("📷", "Images", "Analyze uploaded waste images."),
        ("🎥", "Videos", "Process recorded video files."),
        ("📹", "Live Camera", "Detect waste in real time."),
        ("🌐", "Live Streams", "Analyze network video streams.")
    ]

    for col, (icon, title, description) in zip(
        input_cols,
        inputs
    ):

        with col:

            st.html(
                f"""
                <div class="home-input-card">

                    <div class="home-input-icon">
                        {icon}
                    </div>

                    <strong>{title}</strong>

                    <p>{description}</p>

                </div>
                """
            )


    # ========================================================
    # TECHNOLOGY
    # ========================================================

    st.html(
        """
        <div class="home-tech">

            <div>
                <div class="home-eyebrow">
                    POWERED BY COMPUTER VISION
                </div>

                <h2>
                    Built with AI for real-world waste detection
                </h2>

                <p>
                    WasteAI combines YOLOv8 object detection with
                    real-time processing to provide fast and
                    reliable waste classification.
                </p>
            </div>

            <div class="home-tech-badge">
                <div class="tech-model">YOLOv8</div>
                <div class="tech-label">Detection Engine</div>
                <div class="tech-status">
                    ● System Ready
                </div>
            </div>

        </div>
        """
    )
# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    # ========================================================
    # DASHBOARD HEADER
    # ========================================================

    st.html(
        """
        <div class="dashboard-header">

            <div>
                <div class="dashboard-eyebrow">
                    WASTEAI OVERVIEW
                </div>

                <h1>
                    Dashboard
                </h1>

                <p>
                    Monitor your waste detection system at a glance.
                </p>
            </div>

            <div class="dashboard-online">
                <span class="dashboard-status-dot"></span>
                System Online
            </div>

        </div>
        """
    )


    # ========================================================
    # CALCULATE OVERVIEW VALUES
    # ========================================================

    total_detections = 0
    total_items = 0
    avg_confidence = 0
    top_category = "—"

    if "detection_stats" in st.session_state:

        stats = st.session_state.detection_stats

        total_detections = stats.get(
            "total_detections",
            stats.get("detections", 0)
        )

        total_items = stats.get(
            "total_objects",
            stats.get("total_items", 0)
        )

        avg_confidence = stats.get(
            "average_confidence",
            stats.get("avg_confidence", 0)
        )

        top_category = stats.get(
            "top_category",
            stats.get("most_detected", "—")
        )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.html(
            f"""
            <div class="dashboard-kpi">

                <div class="dashboard-kpi-label">
                    TOTAL DETECTIONS
                </div>

                <div class="dashboard-kpi-value">
                    {total_detections:,}
                </div>

                <div class="dashboard-kpi-meta">
                    Recorded by WasteAI
                </div>

            </div>
            """
        )


    with col2:

        st.html(
            f"""
            <div class="dashboard-kpi">

                <div class="dashboard-kpi-label">
                    WASTE ITEMS
                </div>

                <div class="dashboard-kpi-value">
                    {total_items:,}
                </div>

                <div class="dashboard-kpi-meta">
                    Objects identified
                </div>

            </div>
            """
        )


    with col3:

        if isinstance(avg_confidence, (int, float)):
            confidence_text = f"{avg_confidence:.1f}%"
        else:
            confidence_text = "—"

        st.html(
            f"""
            <div class="dashboard-kpi">

                <div class="dashboard-kpi-label">
                    AVG CONFIDENCE
                </div>

                <div class="dashboard-kpi-value">
                    {confidence_text}
                </div>

                <div class="dashboard-kpi-meta">
                    Model prediction confidence
                </div>

            </div>
            """
        )


    with col4:

        st.html(
            f"""
            <div class="dashboard-kpi">

                <div class="dashboard-kpi-label">
                    TOP CATEGORY
                </div>

                <div class="dashboard-kpi-value dashboard-category">
                    {top_category}
                </div>

                <div class="dashboard-kpi-meta">
                    Most frequently detected
                </div>

            </div>
            """
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # DASHBOARD LOWER SECTION
    # ========================================================

    left_col, right_col = st.columns([1.6, 1])


    # ========================================================
    # RECENT ACTIVITY
    # ========================================================

    with left_col:

        st.html(
            """
            <div class="dashboard-section-card">

                <div class="dashboard-section-title">
                    Recent Detection Activity
                </div>

                <div class="dashboard-section-subtitle">
                    Latest activity recorded by the system
                </div>

            </div>
            """
        )


        if (
            "detection_history" in st.session_state
            and st.session_state.detection_history
        ):

            history = st.session_state.detection_history

            for item in history[-5:][::-1]:

                st.html(
                    f"""
                    <div class="dashboard-activity-row">

                        <div class="dashboard-activity-icon">
                            ♻
                        </div>

                        <div class="dashboard-activity-info">

                            <div class="dashboard-activity-title">
                                {item.get("category", "Waste Detection")}
                            </div>

                            <div class="dashboard-activity-source">
                                {item.get("source", "Detection")}
                            </div>

                        </div>

                        <div class="dashboard-activity-confidence">
                            {item.get("confidence", "—")}
                        </div>

                    </div>
                    """
                )

        else:

            st.html(
                """
                <div class="dashboard-empty">

                    <div class="dashboard-empty-icon">
                        ◌
                    </div>

                    <div class="dashboard-empty-title">
                        No recent detections
                    </div>

                    <div class="dashboard-empty-text">
                        Start a detection to see activity here.
                    </div>

                </div>
                """
            )


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    with right_col:

        st.html(
            """
            <div class="dashboard-section-card">

                <div class="dashboard-section-title">
                    AI System Status
                </div>

                <div class="dashboard-section-subtitle">
                    Current WasteAI services
                </div>

                <div class="dashboard-status-item">

                    <span class="dashboard-status-dot"></span>

                    <div>
                        <strong>YOLOv8</strong>
                        <small>Detection Engine</small>
                    </div>

                    <span class="dashboard-status-ready">
                        Ready
                    </span>

                </div>

                <div class="dashboard-status-item">

                    <span class="dashboard-status-dot"></span>

                    <div>
                        <strong>Detection System</strong>
                        <small>Core Services</small>
                    </div>

                    <span class="dashboard-status-ready">
                        Active
                    </span>

                </div>

                <div class="dashboard-status-item">

                    <span class="dashboard-status-dot"></span>

                    <div>
                        <strong>Storage</strong>
                        <small>Application Storage</small>
                    </div>

                    <span class="dashboard-status-ready">
                        Available
                    </span>

                </div>

            </div>
            """
        )


    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    st.html(
        """
        <div class="dashboard-quick-title">
            Quick Actions
        </div>
        """
    )

    action1, action2 = st.columns(2)

    with action1:

        if st.button(
            "🔍  Start Detection",
            type="primary",
            use_container_width=True,
            key="dashboard_start_detection"
        ):

            st.session_state.page = "🔍 Detection"
            st.rerun()


    with action2:

        if st.button(
            "📄  View Reports",
            use_container_width=True,
            key="dashboard_view_reports"
        ):

            st.session_state.page = "📄 Reports"
            st.rerun()
# ============================================================
# DETECTION
# ============================================================

elif page == "🔍 Detection":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.html("""
    <div class="detection-header">

        <div>
            <div class="detection-eyebrow">
                WASTEAI · COMPUTER VISION
            </div>

            <div class="detection-title">
                Waste Detection
            </div>

            <div class="detection-description">
                Detect and classify waste using AI-powered computer
                vision across images, videos and live streams.
            </div>
        </div>

        <div class="detection-engine-status">
            <span></span>
            YOLOv8 Ready
        </div>

    </div>
    """)


    # ========================================================
    # DETECTION SOURCE
    # ========================================================

    st.html("""
    <div class="detection-section-heading">
        <div class="detection-section-title">
            Detection Source
        </div>

        <div class="detection-section-subtitle">
            Select the source you want WasteAI to analyze.
        </div>
    </div>
    """)


    # Keep the actual source selector because the backend
    # already depends on its value.

    source_radio = st.selectbox(
        "Detection Source",
        settings.SOURCES_LIST,
        key="detection_source",
        label_visibility="collapsed"
    )


    # ========================================================
    # DETECTION CONFIGURATION
    # ========================================================

    config_col1, config_col2 = st.columns([2.5, 1])


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    with config_col1:

        st.html("""
        <div class="detection-config-card">

            <div class="detection-config-icon">
                🎯
            </div>

            <div class="detection-config-content">

                <div class="detection-config-title">
                    Confidence Threshold
                </div>

                <div class="detection-config-description">
                    Control how confident the AI must be before
                    displaying a detection.
                </div>

            </div>

        </div>
        """)


        confidence_percent = st.slider(
            "Confidence Threshold",
            min_value=5,
            max_value=100,
            value=10,
            step=5,
            label_visibility="collapsed",
            help=(
                "Higher values show only detections where "
                "the model is more confident."
            )
        )

        confidence = confidence_percent / 100

        st.caption(
            f"Current threshold: **{confidence_percent}%** · "
            "Lower values detect more objects but may increase "
            "false detections."
        )


    # --------------------------------------------------------
    # MODEL STATUS
    # --------------------------------------------------------

    with config_col2:

        st.html("""
        <div class="detection-model-card">

            <div class="detection-model-icon">
                🤖
            </div>

            <div class="detection-model-name">
                YOLOv8
            </div>

            <div class="detection-model-status">
                <span></span>
                Model Ready
            </div>

        </div>
        """)


    st.markdown("<div style='height:12px'></div>",
                unsafe_allow_html=True)


    # ========================================================
    # IMAGE DETECTION
    # ========================================================

    if source_radio == settings.IMAGE:

        st.html("""
        <div class="detection-workspace-header">

            <div>
                <div class="detection-workspace-title">
                    📷 Image Detection
                </div>

                <div class="detection-workspace-description">
                    Upload an image and let YOLOv8 identify and
                    classify waste objects.
                </div>
            </div>

            <div class="detection-workspace-badge">
                Image Analysis
            </div>

        </div>
        """)


        source_img = st.file_uploader(
            "Choose an image",
            type=("jpg", "jpeg", "png", "bmp", "webp"),
            label_visibility="collapsed",
            key="detection_image_uploader"
        )


        # ----------------------------------------------------
        # NO IMAGE
        # ----------------------------------------------------

        if source_img is None:

            st.html("""
            <div class="detection-upload-card">

                <div class="detection-upload-icon">
                    📤
                </div>

                <div class="detection-upload-title">
                    Upload a waste image
                </div>

                <div class="detection-upload-description">
                    Drop an image here or use the uploader above
                    to begin AI-powered waste detection.
                </div>

                <div class="detection-upload-formats">
                    JPG · JPEG · PNG · BMP · WEBP
                </div>

            </div>
            """)


        # ----------------------------------------------------
        # IMAGE UPLOADED
        # ----------------------------------------------------

        else:

            uploaded_image = PIL.Image.open(source_img)


            st.html("""
            <div class="detection-analysis-heading">
                Analysis Workspace
            </div>
            """)


            preview_col, analysis_col = st.columns(
                [1.55, 1],
                gap="large"
            )


            # ------------------------------------------------
            # ORIGINAL IMAGE
            # ------------------------------------------------

            with preview_col:

                st.html("""
                <div class="detection-panel-label">
                    Original Image
                </div>
                """)

                st.html("""
                <div class="detection-image-panel">
                """)

                st.image(
                    uploaded_image,
                    use_container_width=True
                )

                st.html("</div>")


            # ------------------------------------------------
            # AI ANALYSIS PANEL
            # ------------------------------------------------

            with analysis_col:

                st.html(f"""
                <div class="detection-analysis-card">

                    <div class="detection-analysis-icon">
                        🤖
                    </div>

                    <div class="detection-analysis-title">
                        Ready for Analysis
                    </div>

                    <div class="detection-analysis-text">
                        YOLOv8 will identify waste objects,
                        classify their categories and calculate
                        confidence scores.
                    </div>

                    <div class="detection-threshold-box">

                        <span>
                            Confidence Threshold
                        </span>

                        <strong>
                            {confidence_percent}%
                        </strong>

                    </div>

                </div>
                """)


                detect_button = st.button(
                    "🔍  Detect Waste",
                    type="primary",
                    use_container_width=True,
                    key="image_detect_button"
                )


            # =================================================
            # RUN IMAGE DETECTION
            # =================================================

            if detect_button:

                if model is None:

                    st.error(
                        "The YOLO model could not be loaded."
                    )

                else:

                    with st.spinner(
                        "🤖 AI is analyzing the image..."
                    ):

                        res = model.predict(
                            uploaded_image,
                            conf=confidence
                        )

                    boxes = res[0].boxes

                    res_plotted = (
                        res[0].plot()[:, :, ::-1]
                    )


                    # -----------------------------------------
                    # RESULT
                    # -----------------------------------------

                    st.markdown(
                        "<div style='height:18px'></div>",
                        unsafe_allow_html=True
                    )

                    st.html("""
                    <div class="detection-result-header">

                        <div>
                            <div class="detection-result-title">
                                Detection Result
                            </div>

                            <div class="detection-result-subtitle">
                                AI-generated waste detection output
                            </div>
                        </div>

                        <div class="detection-result-badge">
                            Analysis Complete
                        </div>

                    </div>
                    """)


                    st.html("""
                    <div class="detection-result-image">
                    """)

                    st.image(
                        res_plotted,
                        caption="AI Detection Output",
                        use_container_width=True
                    )

                    st.html("</div>")


                    # -----------------------------------------
                    # ANALYZE DETECTIONS
                    # -----------------------------------------

                    stats = {}

                    for box in boxes:

                        class_id = int(box.cls[0])

                        class_name = model.names[class_id]

                        conf_score = float(box.conf[0])


                        if class_name not in stats:

                            stats[class_name] = {
                                "count": 0,
                                "conf_sum": 0.0
                            }


                        stats[class_name]["count"] += 1

                        stats[class_name]["conf_sum"] += conf_score


                    # -----------------------------------------
                    # SUMMARY
                    # -----------------------------------------

                    if stats:

                        total_items = sum(
                            item["count"]
                            for item in stats.values()
                        )

                        unique_categories = len(stats)

                        dominant_category = max(
                            stats.items(),
                            key=lambda x: x[1]["count"]
                        )[0]


                        st.markdown(
                            "<div style='height:18px'></div>",
                            unsafe_allow_html=True
                        )


                        st.html("""
                        <div class="detection-summary-title">
                            Detection Summary
                        </div>
                        """)


                        summary_col1, summary_col2, summary_col3 = \
                            st.columns(3)


                        summary_cards = [

                            (
                                summary_col1,
                                "♻️",
                                total_items,
                                "Total Waste Items"
                            ),

                            (
                                summary_col2,
                                "🗂️",
                                unique_categories,
                                "Categories Detected"
                            ),

                            (
                                summary_col3,
                                "🏆",
                                dominant_category,
                                "Dominant Category"
                            )

                        ]


                        for column, icon, value, label in summary_cards:

                            with column:

                                value_size = (
                                    "19px"
                                    if label == "Dominant Category"
                                    else "27px"
                                )


                                st.html(f"""
                                <div class="detection-summary-card">

                                    <div class="detection-summary-icon">
                                        {icon}
                                    </div>

                                    <div style="
                                        font-size:{value_size};
                                        font-weight:800;
                                        color:#17352b;
                                        margin-top:8px;
                                        overflow-wrap:anywhere;
                                    ">
                                        {value}
                                    </div>

                                    <div class="detection-summary-label">
                                        {label}
                                    </div>

                                </div>
                                """)


                        # -------------------------------------
                        # SAVE RESULTS
                        # -------------------------------------

                        table_data = []


                        for category, data in stats.items():

                            average_confidence = (
                                data["conf_sum"] /
                                data["count"]
                            ) * 100


                            table_data.append({

                                "Waste Category": category,

                                "Quantity": data["count"],

                                "Avg Confidence":
                                    f"{average_confidence:.1f}%"

                            })


                        # Keep these because Analytics and
                        # Reports use them.

                        st.session_state[
                            "detection_stats"
                        ] = stats

                        st.session_state[
                            "detection_table"
                        ] = table_data

                        st.session_state[
                            "total_items"
                        ] = total_items

                        st.session_state[
                            "unique_categories"
                        ] = unique_categories

                        st.session_state[
                            "dominant_category"
                        ] = dominant_category


                    else:

                        st.info(
                            "No waste objects detected. "
                            "Try lowering the confidence threshold."
                        )
        # ========================================================
        # GO TO ANALYTICS
        # ========================================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        analytics_col1, analytics_col2, analytics_col3 = st.columns(
            [1, 1.2, 1]
        )

        with analytics_col2:

            if st.button(
                "📊  View Detailed Analytics",
                type="primary",
                use_container_width=True,
                key="go_to_analytics"
            ):
                st.session_state.page = "📈 Analytics"
                st.rerun()

    # ========================================================
    # VIDEO
    # ========================================================

    elif source_radio == settings.VIDEO:

        st.html("""
        <div class="detection-workspace-header">

            <div>
                <div class="detection-workspace-title">
                    🎥 Video Detection
                </div>

                <div class="detection-workspace-description">
                    Analyze recorded video frame by frame
                    using the YOLOv8 detection engine.
                </div>
            </div>

            <div class="detection-workspace-badge">
                Video Analysis
            </div>

        </div>
        """)


        helper.play_stored_video(
            confidence,
            model
        )


    # ========================================================
    # WEBCAM
    # ========================================================

    elif source_radio == settings.WEBCAM:

        st.html("""
        <div class="detection-workspace-header">

            <div>
                <div class="detection-workspace-title">
                    📹 Live Webcam Detection
                </div>

                <div class="detection-workspace-description">
                    Use your connected camera for real-time
                    waste detection.
                </div>
            </div>

            <div class="detection-workspace-badge">
                Live Camera
            </div>

        </div>
        """)


        helper.play_webcam(
            confidence,
            model
        )


    # ========================================================
    # YOUTUBE
    # ========================================================

    elif source_radio == settings.YOUTUBE:

        st.html("""
        <div class="detection-workspace-header">

            <div>
                <div class="detection-workspace-title">
                    ▶️ YouTube Detection
                </div>

                <div class="detection-workspace-description">
                    Analyze waste directly from a YouTube
                    video source.
                </div>
            </div>

            <div class="detection-workspace-badge">
                Online Video
            </div>

        </div>
        """)


        helper.play_youtube_video(
            confidence,
            model
        )


    # ========================================================
    # RTSP
    # ========================================================

    elif source_radio == settings.RTSP:

        st.html("""
        <div class="detection-workspace-header">

            <div>
                <div class="detection-workspace-title">
                    🌐 RTSP Stream Detection
                </div>

                <div class="detection-workspace-description">
                    Connect to an RTSP camera stream for
                    continuous waste detection.
                </div>
            </div>

            <div class="detection-workspace-badge">
                Live Stream
            </div>

        </div>
        """)


        helper.play_rtsp_stream(
            confidence,
            model
        )
# ============================================================
# ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    # ========================================================
    # HEADER
    # ========================================================

    st.html("""
    <div class="analytics-header">

        <div>

            <div class="analytics-eyebrow">
                WASTEAI · INTELLIGENCE CENTER
            </div>

            <div class="analytics-title">
                Waste Analytics
            </div>

            <div class="analytics-description">
                Transform detection results into meaningful
                waste distribution and classification insights.
            </div>

        </div>

        <div class="analytics-status">
            <span></span>
            Analytics Active
        </div>

    </div>
    """)


    # ========================================================
    # CHECK DATA
    # ========================================================

    if "detection_stats" not in st.session_state:

        st.html("""
        <div class="analytics-empty">

            <div class="analytics-empty-icon">
                📊
            </div>

            <div class="analytics-empty-title">
                No Analytics Data Available
            </div>

            <div class="analytics-empty-text">
                Run a waste detection first. Once WasteAI
                identifies waste, the results will automatically
                appear here for analysis.
            </div>

        </div>
        """)


        # Go directly to Detection

        empty_col1, empty_col2, empty_col3 = st.columns(
            [1, 1.2, 1]
        )

        with empty_col2:

            if st.button(
                "🔍  Go to Detection",
                type="primary",
                use_container_width=True,
                key="analytics_go_detection"
            ):

                st.session_state.page = "🔍 Detection"
                st.rerun()


    else:

        # ====================================================
        # LOAD DATA
        # ====================================================

        stats = st.session_state["detection_stats"]

        total_items = st.session_state["total_items"]

        unique_categories = (
            st.session_state["unique_categories"]
        )

        dominant_category = (
            st.session_state["dominant_category"]
        )


        # ====================================================
        # CALCULATE METRICS
        # ====================================================

        total_confidence = 0
        total_detected = 0

        for category, data in stats.items():

            total_confidence += data["conf_sum"]

            total_detected += data["count"]


        average_confidence = (
            total_confidence / total_detected
        ) * 100 if total_detected else 0


        dominant_count = (
            stats[dominant_category]["count"]
        )


        dominant_percentage = (
            dominant_count / total_items
        ) * 100 if total_items else 0


        # ====================================================
        # KPI SECTION
        # ====================================================

        st.html("""
        <div class="analytics-section-heading">

            <div class="analytics-section-title">
                Detection Overview
            </div>

            <div class="analytics-section-subtitle">
                Key metrics from the latest WasteAI analysis.
            </div>

        </div>
        """)


        k1, k2, k3, k4 = st.columns(4)


        # ----------------------------------------------------
        # TOTAL ITEMS
        # ----------------------------------------------------

        with k1:

            st.html(f"""
            <div class="analytics-kpi">

                <div class="analytics-kpi-icon">
                    ♻️
                </div>

                <div class="analytics-kpi-label">
                    TOTAL WASTE
                </div>

                <div class="analytics-kpi-value">
                    {total_items}
                </div>

                <div class="analytics-kpi-subtext">
                    objects detected
                </div>

            </div>
            """)


        # ----------------------------------------------------
        # CATEGORIES
        # ----------------------------------------------------

        with k2:

            st.html(f"""
            <div class="analytics-kpi">

                <div class="analytics-kpi-icon">
                    🗂️
                </div>

                <div class="analytics-kpi-label">
                    CATEGORIES
                </div>

                <div class="analytics-kpi-value">
                    {unique_categories}
                </div>

                <div class="analytics-kpi-subtext">
                    waste types identified
                </div>

            </div>
            """)


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        with k3:

            st.html(f"""
            <div class="analytics-kpi">

                <div class="analytics-kpi-icon">
                    🎯
                </div>

                <div class="analytics-kpi-label">
                    AVG CONFIDENCE
                </div>

                <div class="analytics-kpi-value">
                    {average_confidence:.1f}%
                </div>

                <div class="analytics-kpi-subtext">
                    model confidence
                </div>

            </div>
            """)


        # ----------------------------------------------------
        # DOMINANT CATEGORY
        # ----------------------------------------------------

        with k4:

            st.html(f"""
            <div class="analytics-kpi">

                <div class="analytics-kpi-icon">
                    🏆
                </div>

                <div class="analytics-kpi-label">
                    DOMINANT WASTE
                </div>

                <div class="analytics-kpi-category">
                    {dominant_category}
                </div>

                <div class="analytics-kpi-subtext">
                    {dominant_percentage:.1f}% of detections
                </div>

            </div>
            """)


        # ====================================================
        # CHART DATA
        # ====================================================

        chart_data = pd.DataFrame({

            "Waste Category": list(stats.keys()),

            "Quantity": [
                data["count"]
                for data in stats.values()
            ]

        })


        # ====================================================
        # DISTRIBUTION SECTION
        # ====================================================

        st.html("""
        <div class="analytics-section-heading analytics-spacing">

            <div class="analytics-section-title">
                Waste Distribution
            </div>

            <div class="analytics-section-subtitle">
                Understand which waste categories dominate the
                current detection results.
            </div>

        </div>
        """)


        chart_col, insight_col = st.columns(
            [1.7, 1]
        )


        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        with chart_col:

            st.html("""
            <div class="analytics-chart-card">

                <div class="analytics-card-title">
                    Category Distribution
                </div>

                <div class="analytics-card-description">
                    Detected waste items grouped by category.
                </div>

            </div>
            """)


            st.bar_chart(
                chart_data.set_index(
                    "Waste Category"
                ),
                use_container_width=True
            )


        # ----------------------------------------------------
        # AI INSIGHT
        # ----------------------------------------------------

        with insight_col:

            st.html(f"""
            <div class="analytics-insight">

                <div class="analytics-insight-label">
                    AI GENERATED INSIGHT
                </div>

                <div class="analytics-insight-title">
                    Dominant Waste
                </div>

                <div class="analytics-insight-category">
                    {dominant_category}
                </div>

                <div class="analytics-insight-divider"></div>

                <div class="analytics-insight-small">
                    This category represents
                </div>

                <div class="analytics-insight-percentage">
                    {dominant_percentage:.1f}%
                </div>

                <div class="analytics-insight-small">
                    of all detected waste.
                </div>

                <div class="analytics-insight-footer">
                    {dominant_count} object(s) detected
                </div>

            </div>
            """)


        # ====================================================
        # CATEGORY ANALYSIS
        # ====================================================

        st.html("""
        <div class="analytics-section-heading analytics-spacing">

            <div class="analytics-section-title">
                Category Analysis
            </div>

            <div class="analytics-section-subtitle">
                Detailed performance and distribution by waste type.
            </div>

        </div>
        """)


        analytics_data = []


        for category, data in stats.items():

            avg_confidence = (
                data["conf_sum"] /
                data["count"]
            ) * 100


            percentage = (
                data["count"] /
                total_items
            ) * 100


            analytics_data.append({

                "Waste Category": category,

                "Quantity": data["count"],

                "Share": f"{percentage:.1f}%",

                "Avg Confidence":
                    f"{avg_confidence:.1f}%"

            })


        analytics_df = pd.DataFrame(
            analytics_data
        )


        st.dataframe(
            analytics_df,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # CONFIDENCE INFORMATION
        # ====================================================

        st.html(f"""
        <div class="analytics-confidence-card">

            <div class="analytics-confidence-icon">
                🎯
            </div>

            <div class="analytics-confidence-content">

                <div class="analytics-confidence-title">
                    Detection Quality
                </div>

                <div class="analytics-confidence-text">
                    WasteAI achieved an average detection
                    confidence of
                    <strong>{average_confidence:.1f}%</strong>
                    across {total_items} detected object(s).
                </div>

            </div>

        </div>
        """)


        # ====================================================
        # FOOTER
        # ====================================================

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True
        )

        st.caption(
            "Analytics are calculated from the latest detection "
            "results stored during the current application session."
        )        
# ============================================================
# REPORTS
# ============================================================

elif page == "📄 Reports":

    # ========================================================
    # REPORT HEADER
    # ========================================================

    st.html("""
    <div class="reports-header">

        <div>

            <div class="reports-eyebrow">
                WASTEAI · REPORTING CENTER
            </div>

            <div class="reports-title">
                Waste Reports
            </div>

            <div class="reports-description">
                Generate, review and export a structured report
                from your latest waste detection analysis.
            </div>

        </div>

        <div class="reports-status">
            <span></span>
            Report Ready
        </div>

    </div>
    """)


    # ========================================================
    # CHECK DETECTION DATA
    # ========================================================

    if "detection_stats" not in st.session_state:

        st.html("""
        <div class="reports-empty">

            <div class="reports-empty-icon">
                📄
            </div>

            <div class="reports-empty-title">
                No Report Available
            </div>

            <div class="reports-empty-text">
                Complete a waste detection first. Your detection
                results will automatically become available here
                as a downloadable report.
            </div>

        </div>
        """)


        empty_col1, empty_col2, empty_col3 = st.columns(
            [1, 1.2, 1]
        )

        with empty_col2:

            if st.button(
                "🔍  Go to Detection",
                type="primary",
                use_container_width=True,
                key="reports_go_detection"
            ):

                st.session_state.page = "🔍 Detection"

                if "top_navigation" in st.session_state:
                    st.session_state.top_navigation = "🔍 Detection"

                st.rerun()


    else:

        # ====================================================
        # LOAD DETECTION DATA
        # ====================================================

        stats = st.session_state["detection_stats"]

        total_items = st.session_state["total_items"]

        unique_categories = (
            st.session_state["unique_categories"]
        )

        dominant_category = (
            st.session_state["dominant_category"]
        )


        # ====================================================
        # REPORT OVERVIEW
        # ====================================================

        st.html("""
        <div class="reports-section-heading">

            <div class="reports-section-title">
                Report Overview
            </div>

            <div class="reports-section-subtitle">
                Summary of the latest AI waste detection session.
            </div>

        </div>
        """)


        r1, r2, r3 = st.columns(3)


        with r1:

            st.html(f"""
            <div class="reports-summary-card">

                <div class="reports-summary-icon">
                    ♻️
                </div>

                <div class="reports-summary-label">
                    TOTAL WASTE ITEMS
                </div>

                <div class="reports-summary-value">
                    {total_items}
                </div>

                <div class="reports-summary-text">
                    objects detected
                </div>

            </div>
            """)


        with r2:

            st.html(f"""
            <div class="reports-summary-card">

                <div class="reports-summary-icon">
                    🗂️
                </div>

                <div class="reports-summary-label">
                    CATEGORIES
                </div>

                <div class="reports-summary-value">
                    {unique_categories}
                </div>

                <div class="reports-summary-text">
                    waste types identified
                </div>

            </div>
            """)


        with r3:

            st.html(f"""
            <div class="reports-summary-card">

                <div class="reports-summary-icon">
                    🏆
                </div>

                <div class="reports-summary-label">
                    DOMINANT CATEGORY
                </div>

                <div class="reports-summary-category">
                    {dominant_category}
                </div>

                <div class="reports-summary-text">
                    most frequently detected
                </div>

            </div>
            """)


        # ====================================================
        # BUILD REPORT
        # ====================================================

        report_data = []


        for category, data in stats.items():

            average_confidence = (
                data["conf_sum"] /
                data["count"]
            ) * 100


            percentage = (
                data["count"] /
                total_items
            ) * 100 if total_items else 0


            report_data.append({

                "Waste Category": category,

                "Quantity": data["count"],

                "Percentage": f"{percentage:.1f}%",

                "Average Confidence":
                    f"{average_confidence:.1f}%"

            })


        report_df = pd.DataFrame(report_data)


        # ====================================================
        # REPORT TABLE
        # ====================================================

        st.html("""
        <div class="reports-section-heading reports-spacing">

            <div class="reports-section-title">
                Detection Report
            </div>

            <div class="reports-section-subtitle">
                Structured breakdown of every detected waste category.
            </div>

        </div>
        """)


        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True,
            column_config={

                "Waste Category":
                    st.column_config.TextColumn(
                        "Waste Category"
                    ),

                "Quantity":
                    st.column_config.NumberColumn(
                        "Quantity",
                        format="%d"
                    ),

                "Percentage":
                    st.column_config.TextColumn(
                        "Percentage"
                    ),

                "Average Confidence":
                    st.column_config.TextColumn(
                        "Average Confidence"
                    )

            }
        )


        # ====================================================
        # EXPORT SECTION
        # ====================================================

        st.html("""
        <div class="reports-export-card">

            <div class="reports-export-icon">
                📥
            </div>

            <div class="reports-export-content">

                <div class="reports-export-title">
                    Export Waste Report
                </div>

                <div class="reports-export-description">
                    Download the current detection results as a
                    CSV file for further analysis, documentation
                    or record keeping.
                </div>

            </div>

        </div>
        """)


        report_csv = report_df.to_csv(
            index=False
        ).encode("utf-8")


        export_col1, export_col2, export_col3 = st.columns(
            [1, 1.4, 1]
        )


        with export_col2:

            st.download_button(
                "📥  Download Waste Detection Report",
                data=report_csv,
                file_name="waste_detection_report.csv",
                mime="text/csv",
                use_container_width=True,
                key="reports_page_download"
            )


        # ====================================================
        # REPORT INFORMATION
        # ====================================================

        info_col1, info_col2 = st.columns(2)


        with info_col1:

            st.html("""
            <div class="reports-info-card">

                <div class="reports-info-label">
                    DETECTION MODEL
                </div>

                <div class="reports-info-value">
                    YOLOv8 Object Detection
                </div>

            </div>
            """)


        with info_col2:

            st.html("""
            <div class="reports-info-card">

                <div class="reports-info-label">
                    REPORT TYPE
                </div>

                <div class="reports-info-value">
                    Waste Classification & Detection
                </div>

            </div>
            """)
## ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html("""
    <div style="
        background:#ffffff;
        border:1px solid #e2ebe6;
        border-radius:18px;
        padding:24px 26px;
        margin-top:8px;
        margin-bottom:20px;
        box-shadow:0 4px 14px rgba(0,0,0,.035);
    ">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:20px;
        ">

            <div>

                <div style="
                    font-size:22px;
                    font-weight:800;
                    color:#17352b;
                ">
                    ⚙️ Configuration Center
                </div>

                <div style="
                    font-size:13px;
                    color:#75817b;
                    margin-top:5px;
                    line-height:1.5;
                ">
                    Configure the AI model, detection behavior,
                    tracking, supported categories, and input sources.
                </div>

            </div>

            <div style="
                background:#edf7f1;
                color:#287653;
                border:1px solid #d7ecdf;
                border-radius:999px;
                padding:7px 12px;
                font-size:12px;
                font-weight:700;
                white-space:nowrap;
            ">
                ● System Ready
            </div>

        </div>

    </div>
    """)


    # ========================================================
    # MODEL CONFIGURATION
    # ========================================================

    st.markdown("### 🤖 AI Model Configuration")

    model_col1, model_col2 = st.columns(2)


    with model_col1:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:20px;
            min-height:125px;
            box-shadow:0 4px 14px rgba(0,0,0,.035);
        ">

            <div style="
                font-size:26px;
            ">
                🧠
            </div>

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
                margin-top:8px;
                letter-spacing:.5px;
            ">
                DETECTION MODEL
            </div>

            <div style="
                font-size:22px;
                font-weight:850;
                color:#17352b;
                margin-top:3px;
            ">
                YOLOv8
            </div>

        </div>
        """)


    with model_col2:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:20px;
            min-height:125px;
            box-shadow:0 4px 14px rgba(0,0,0,.035);
        ">

            <div style="
                font-size:26px;
            ">
                ⚡
            </div>

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
                margin-top:8px;
                letter-spacing:.5px;
            ">
                MODEL STATUS
            </div>

            <div style="
                font-size:22px;
                font-weight:850;
                color:#287653;
                margin-top:3px;
            ">
                ● Ready
            </div>

        </div>
        """)


    st.html("""
    <div style="
        background:#f6f9f7;
        border:1px solid #e2ebe6;
        border-radius:12px;
        padding:12px 15px;
        margin-top:10px;
        margin-bottom:22px;
        font-size:12px;
        color:#68736e;
    ">
        <strong style="color:#30433b;">
            Model file:
        </strong>
    """ + str(settings.DETECTION_MODEL) + """
    </div>
    """)


    # ========================================================
    # DETECTION CONFIGURATION
    # ========================================================

    st.markdown("### 🎯 Detection Configuration")

    config_col1, config_col2 = st.columns(2)


    with config_col1:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:18px 20px 10px 20px;
            margin-bottom:10px;
        ">

            <div style="
                font-size:15px;
                font-weight:800;
                color:#17352b;
            ">
                🎯 Confidence Threshold
            </div>

            <div style="
                font-size:11px;
                color:#75817b;
                margin-top:4px;
            ">
                Minimum confidence required for a detection.
            </div>

        </div>
        """)


        settings_confidence = st.slider(
            "Default Confidence Threshold",
            min_value=5,
            max_value=100,
            value=10,
            step=5,
            help=(
                "Controls how confident YOLO must be "
                "before displaying a detection."
            )
        )

        st.caption(
            f"Current default threshold: **{settings_confidence}%**"
        )


    with config_col2:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:18px 20px 10px 20px;
            margin-bottom:10px;
        ">

            <div style="
                font-size:15px;
                font-weight:800;
                color:#17352b;
            ">
                🛰️ Object Tracking
            </div>

            <div style="
                font-size:11px;
                color:#75817b;
                margin-top:4px;
            ">
                Track objects across consecutive video frames.
            </div>

        </div>
        """)


        enable_tracking = st.toggle(
            "Enable Object Tracking",
            value=False,
            help=(
                "Track detected objects across video frames."
            )
        )


        if enable_tracking:

            tracker_type = st.selectbox(
                "Tracking Algorithm",
                [
                    "bytetrack.yaml",
                    "botsort.yaml"
                ]
            )

            st.success(
                f"Tracking enabled • {tracker_type}"
            )

        else:

            tracker_type = None

            st.info(
                "Object tracking is currently disabled."
            )


    # ========================================================
    # WASTE CATEGORIES
    # ========================================================

    st.markdown("### ♻️ Supported Waste Categories")

    st.caption(
        "Waste categories currently supported by the detection model."
    )


    categories = [
        ("📦", "CARDBOARD"),
        ("🍾", "GLASS"),
        ("🥫", "METAL"),
        ("📄", "PAPER"),
        ("🥤", "PLASTIC"),
        ("🌱", "BIODEGRADABLE")
    ]


    category_cols = st.columns(3)


    for i, (icon, category) in enumerate(categories):

        with category_cols[i % 3]:

            st.html("""
            <div style="
                background:#ffffff;
                border:1px solid #e2ebe6;
                border-radius:14px;
                padding:18px;
                min-height:105px;
                margin-bottom:14px;
                box-shadow:0 3px 12px rgba(0,0,0,.025);
            ">

                <div style="
                    font-size:28px;
                ">
            """ + icon + """
                </div>

                <div style="
                    font-size:13px;
                    font-weight:800;
                    color:#17352b;
                    margin-top:8px;
                ">
            """ + category + """
                </div>

                <div style="
                    font-size:10px;
                    color:#8a948f;
                    margin-top:3px;
                ">
                    Supported category
                </div>

            </div>
            """)


    # ========================================================
    # INPUT SOURCES
    # ========================================================

    st.markdown("### 📡 Detection Input Sources")

    st.caption(
        "Available sources that can be used by the detection engine."
    )


    source_icons = {
        settings.IMAGE: "📷",
        settings.VIDEO: "🎥",
        settings.WEBCAM: "📹",
        settings.YOUTUBE: "▶️",
        settings.RTSP: "🌐"
    }


    source_cols = st.columns(
        len(settings.SOURCES_LIST)
    )


    for i, source in enumerate(
        settings.SOURCES_LIST
    ):

        with source_cols[i]:

            st.html("""
            <div style="
                background:#ffffff;
                border:1px solid #e2ebe6;
                border-radius:14px;
                padding:18px 10px;
                min-height:105px;
                text-align:center;
                box-shadow:0 3px 12px rgba(0,0,0,.025);
            ">

                <div style="
                    font-size:28px;
                ">
            """ + source_icons.get(
                source,
                "📡"
            ) + """
                </div>

                <div style="
                    margin-top:8px;
                    font-size:12px;
                    font-weight:750;
                    color:#30433b;
                ">
            """ + str(source) + """
                </div>

                <div style="
                    font-size:10px;
                    color:#8a948f;
                    margin-top:3px;
                ">
                    Available
                </div>

            </div>
            """)


    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )

    st.markdown("### ℹ️ System Information")


    info_col1, info_col2 = st.columns(2)


    with info_col1:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:20px;
            min-height:145px;
        ">

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
                letter-spacing:.5px;
            ">
                APPLICATION
            </div>

            <div style="
                font-size:16px;
                font-weight:800;
                color:#17352b;
                margin-top:7px;
            ">
                WasteAI
            </div>

            <div style="
                font-size:12px;
                color:#75817b;
                margin-top:4px;
            ">
                Smart Waste Detection System
            </div>

            <div style="
                height:1px;
                background:#e7ede9;
                margin:14px 0;
            "></div>

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
            ">
                COMPUTER VISION
            </div>

            <div style="
                font-size:13px;
                font-weight:700;
                color:#30433b;
                margin-top:4px;
            ">
                YOLOv8 Object Detection
            </div>

        </div>
        """)


    with info_col2:

        st.html("""
        <div style="
            background:#ffffff;
            border:1px solid #e2ebe6;
            border-radius:16px;
            padding:20px;
            min-height:145px;
        ">

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
                letter-spacing:.5px;
            ">
                FRAMEWORK
            </div>

            <div style="
                font-size:16px;
                font-weight:800;
                color:#17352b;
                margin-top:7px;
            ">
                Streamlit
            </div>

            <div style="
                font-size:12px;
                color:#75817b;
                margin-top:4px;
            ">
                Interactive application interface
            </div>

            <div style="
                height:1px;
                background:#e7ede9;
                margin:14px 0;
            "></div>

            <div style="
                font-size:11px;
                color:#7a8580;
                font-weight:700;
            ">
                PROCESSING
            </div>

            <div style="
                font-size:13px;
                font-weight:700;
                color:#30433b;
                margin-top:4px;
            ">
                Real-time detection & classification
            </div>

        </div>
        """)


    st.markdown(
        "<div style='height:14px'></div>",
        unsafe_allow_html=True
    )

    st.caption(
        "Configuration changes apply to the current application session."
    )