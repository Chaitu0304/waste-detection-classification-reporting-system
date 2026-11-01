from pathlib import Path

import PIL

import pandas as pd

import streamlit as st

import smtplib

from email.message import EmailMessage

import settings

import helper





# ============================================================

# PAGE CONFIGURATION

# ============================================================



st.set_page_config(

    page_title="WasteAI | Smart Waste Detection",

    page_icon=None,

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


/* ============================================================
   ULTRA-RESPONSIVE MOBILE & TABLET ADAPTATION
   Fixes mobile layout, horizontal overflow, column squishing,
   touch targets, and navigation bar.
   ============================================================ */

/* Desktop Screens (screen width >= 769px): Hide mobile navigation toggler and drawer */
@media screen and (min-width: 769px) {
    div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]),
    div[data-testid="stElementContainer"]:has(.nav-mobile-marker),
    div[data-testid="stElementContainer"]:has(.mobile-menu-drawer-marker),
    div[data-testid="stElementContainer"]:has(button[key^="m_nav_"]) {
        display: none !important;
    }
}

/* Mobile & Small Tablets (screen width <= 768px) */
@media screen and (max-width: 768px) {
    /* 1. Global Viewport & Container Reset */
    html, body, .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }

    .main .block-container,
    body:has(.home-hero) .main .block-container,
    div[data-testid="stAppViewBlockContainer"] {
        padding-left: 12px !important;
        padding-right: 12px !important;
        padding-top: 8px !important;
        padding-bottom: 28px !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* 2. Hide Desktop Navigation on Mobile */
    div[data-testid="stHorizontalBlock"]:has(button[key^="d_nav_"]),
    div[data-testid="stElementContainer"]:has(.nav-desktop-marker) {
        display: none !important;
    }

    /* 3. Mobile Top Bar (Brand + Menu Toggler) */
    div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 4px 0px 8px 0px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        border-bottom: 1px solid #e2ebe6 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) > div[data-testid="column"]:first-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        width: auto !important;
        display: flex !important;
        align-items: center !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key="mobile_menu_toggler_btn"]) > div[data-testid="column"]:last-child {
        flex: 0 0 100px !important;
        width: 100px !important;
        min-width: 100px !important;
        max-width: 100px !important;
        display: flex !important;
        justify-content: flex-end !important;
    }

    button[key="mobile_menu_toggler_btn"] {
        white-space: nowrap !important;
        border-radius: 10px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        min-height: 38px !important;
        height: 38px !important;
        width: 100% !important;
        border: 1.5px solid #2e7d32 !important;
        box-shadow: 0 2px 6px rgba(46, 125, 50, 0.12) !important;
    }

    /* 4. Mobile Menu Drawer */
    div[data-testid="stElementContainer"]:has(.mobile-menu-drawer-marker) {
        display: block !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stElementContainer"]:has(button[key^="m_nav_"]) {
        display: block !important;
        width: 100% !important;
        margin-bottom: 6px !important;
    }

    button[key^="m_nav_"] {
        white-space: nowrap !important;
        width: 100% !important;
        min-height: 44px !important;
        height: 44px !important;
        font-size: 14px !important;
        font-weight: 650 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }

    .wa-top-divider {
        margin-top: 4px !important;
        margin-bottom: 16px !important;
    }

    /* 5. Universal Column Stacking for all multi-column layouts EXCEPT the mobile nav bar */
    div[data-testid="stHorizontalBlock"]:not(:has(button[key="mobile_menu_toggler_btn"])):not(:has(button[key^="d_nav_"])) {
        display: flex !important;
        flex-direction: column !important;
        flex-wrap: wrap !important;
        gap: 14px !important;
        width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"]:not(:has(button[key="mobile_menu_toggler_btn"])):not(:has(button[key^="d_nav_"])) > div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 0px !important;
    }

    /* 4. Hero Section Mobile Optimization */
    .home-hero {
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 24px 18px !important;
        min-height: auto !important;
        margin-bottom: 20px !important;
        border-radius: 20px !important;
    }

    .home-hero-content {
        max-width: 100% !important;
        width: 100% !important;
    }

    .home-hero h1,
    .hero-title,
    .main-title {
        font-size: 25px !important;
        line-height: 1.22 !important;
        letter-spacing: -0.4px !important;
    }

    .home-hero p,
    .hero-description,
    .dashboard-hero p {
        font-size: 14px !important;
        line-height: 1.45 !important;
        margin-top: 12px !important;
        max-width: 100% !important;
    }

    .home-visual {
        width: 100% !important;
        max-width: 100% !important;
        margin-top: 22px !important;
        justify-content: center !important;
    }

    .home-visual-card {
        width: 100% !important;
        max-width: 320px !important;
        padding: 20px 18px !important;
        border-radius: 18px !important;
    }

    .dashboard-hero {
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 20px 18px !important;
        min-height: auto !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
    }

    /* 5. Mobile Cards, Metrics & Padding */
    .dashboard-card,
    .detection-summary-card,
    .analytics-chart-card,
    .reports-info-card,
    .analytics-confidence-card,
    .detection-analysis-card,
    .detection-model-card,
    .home-tech-badge {
        padding: 16px 16px !important;
        border-radius: 14px !important;
        min-height: auto !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    .card-value,
    .dashboard-card-value {
        font-size: 24px !important;
        line-height: 1.2 !important;
    }

    .card-title,
    .dashboard-card-title {
        font-size: 13px !important;
    }

    /* 6. Detection Page Mobile Tuning */
    .detection-header,
    .analytics-header,
    .reports-header {
        padding: 18px 16px !important;
        border-radius: 16px !important;
        margin-bottom: 14px !important;
    }

    .detection-upload-card {
        padding: 28px 16px !important;
        border-radius: 16px !important;
        margin-top: 6px !important;
    }

    .detection-upload-icon {
        width: 50px !important;
        height: 50px !important;
        font-size: 24px !important;
        margin-bottom: 12px !important;
    }

    .detection-upload-card h3 {
        font-size: 16px !important;
    }

    .detection-upload-card p {
        font-size: 13px !important;
    }

    /* Images and Panels */
    div[data-testid="stImage"] {
        width: 100% !important;
    }

    div[data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
        max-height: 420px !important;
        object-fit: contain !important;
        border-radius: 12px !important;
    }

    .detection-result-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
        padding: 14px 16px !important;
    }

    .detection-result-badge {
        align-self: flex-start !important;
    }

    /* 7. Tables, DataFrames & Charts Horizontal Scroll Container */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 12px !important;
    }

    /* 8. Touch-First Buttons & Form Controls */
    .stButton > button {
        min-height: 44px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        width: 100% !important;
    }

    div[data-testid="stDownloadButton"] > button {
        min-height: 46px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    div[data-testid="stFileUploader"] {
        width: 100% !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        padding: 20px 14px !important;
        border-radius: 14px !important;
    }

    /* Activity Rows & Badges on Mobile */
    .dashboard-activity-row {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
        padding: 12px 14px !important;
    }

    .dashboard-activity-confidence {
        align-self: flex-start !important;
    }

    /* Empty States on Mobile */
    .dashboard-empty,
    .analytics-empty,
    .reports-empty {
        padding: 30px 16px !important;
    }

    .dashboard-empty-icon,
    .analytics-empty-icon,
    .reports-empty-icon {
        width: 52px !important;
        height: 52px !important;
        font-size: 26px !important;
    }

    .dashboard-empty-title,
    .analytics-empty-title,
    .reports-empty-title {
        font-size: 16px !important;
    }

    .dashboard-empty-text,
    .analytics-empty-text,
    .reports-empty-text {
        font-size: 13px !important;
        max-width: 100% !important;
    }
}

/* Extra Small Phones (screen width <= 420px) */
@media screen and (max-width: 420px) {
    .main .block-container,
    body:has(.home-hero) .main .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    .home-hero h1,
    .hero-title,
    .main-title {
        font-size: 22px !important;
    }

    .home-hero,
    .dashboard-hero,
    .detection-header,
    .analytics-header,
    .reports-header {
        padding: 18px 14px !important;
        border-radius: 14px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key^="top_nav_"]) button {
        font-size: 12px !important;
        padding: 6px 12px !important;
        min-height: 38px !important;
    }
}

</style>

""", unsafe_allow_html=True)



# ============================================================

# TOP NAVIGATION

# ============================================================



PAGES = ["Home", "Dashboard", "Detection", "Analytics", "Reports", "Settings"]

if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Home"

if "mobile_menu_open" not in st.session_state:
    st.session_state.mobile_menu_open = False

# ============================================================
# TOP NAVIGATION (RESPONSIVE: DESKTOP BAR + MOBILE TOGGLER)
# ============================================================

# --- DESKTOP NAVIGATION ---
st.html('<div class="nav-desktop-marker"></div>')
d_nav_cols = st.columns([2.4, 1, 1, 1, 1, 1, 1])

with d_nav_cols[0]:
    st.html("""
    <div class="wa-top-brand">
        <div class="wa-top-logo">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#176044" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
                <path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/>
                <path d="m14 14 3-3 3 3"/>
                <path d="m11 5 3-3 3 3"/>
                <path d="M14 2v6"/>
                <path d="m6 16-3 3 3 3"/>
            </svg>
        </div>
        <div>
            <div class="wa-top-brand-name">WasteAI</div>
            <div class="wa-top-brand-subtitle">Waste Intelligence Platform</div>
        </div>
    </div>
    """)

for i, p_name in enumerate(PAGES):
    with d_nav_cols[i + 1]:
        is_cur = (st.session_state.page == p_name)
        b_type = "primary" if is_cur else "secondary"
        if st.button(p_name, key=f"d_nav_{p_name.lower()}", type=b_type, width="stretch"):
            st.session_state.page = p_name
            st.rerun()

# --- MOBILE NAVIGATION WITH MENU TOGGLER ---
st.html('<div class="nav-mobile-marker"></div>')
m_nav_col1, m_nav_col2 = st.columns([2.4, 1.6])

with m_nav_col1:
    st.html("""
    <div class="wa-top-brand">
        <div class="wa-top-logo">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#176044" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
                <path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/>
                <path d="m14 14 3-3 3 3"/>
                <path d="m11 5 3-3 3 3"/>
                <path d="M14 2v6"/>
                <path d="m6 16-3 3 3 3"/>
            </svg>
        </div>
        <div class="wa-top-brand-name">WasteAI</div>
    </div>
    """)

with m_nav_col2:
    is_open = st.session_state.get("mobile_menu_open", False)
    tog_label = "Close" if is_open else "Menu"
    tog_type = "primary" if is_open else "secondary"
    if st.button(tog_label, key="mobile_menu_toggler_btn", type=tog_type, width="stretch"):
        st.session_state.mobile_menu_open = not is_open
        st.rerun()

# Mobile Menu Drawer
if st.session_state.get("mobile_menu_open", False):
    st.html('<div class="mobile-menu-drawer-marker"></div>')
    m_drawer = st.container()
    with m_drawer:
        for p_name in PAGES:
            is_cur = (st.session_state.page == p_name)
            b_type = "primary" if is_cur else "secondary"
            active_marker = "  [Active]" if is_cur else ""
            if st.button(f"{p_name}{active_marker}", key=f"m_nav_{p_name.lower()}", type=b_type, width="stretch"):
                st.session_state.page = p_name
                st.session_state.mobile_menu_open = False
                st.rerun()

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



if "selected_model_name" not in st.session_state:
    st.session_state.selected_model_name = list(settings.AVAILABLE_MODELS.keys())[0] if settings.AVAILABLE_MODELS else "Default"

selected_info = settings.AVAILABLE_MODELS.get(st.session_state.selected_model_name, {})
model_path = selected_info.get("path", Path(settings.DETECTION_MODEL))

try:
    model = helper.load_model(model_path)
except Exception as ex:

    model = None

    st.error(f"Unable to load model: {model_path}")

    st.error(ex)



# ============================================================

# HOME

# ============================================================



if page == "Home":



    # ========================================================

    # HOME HERO

    # ========================================================



    st.html(

        """

        <div class="home-hero">



            <div class="home-hero-content">



                <div class="home-badge">

                    WASTEAI &nbsp;•&nbsp; AI-POWERED WASTE INTELLIGENCE

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



                    <div class="visual-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#176044" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/><path d="m14 14 3-3 3 3"/><path d="m11 5 3-3 3 3"/><path d="M14 2v6"/><path d="m6 16-3 3 3 3"/></svg></div>



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

            "Start Waste Detection",

            type="primary",

            use_container_width=True,

            key="home_start_detection"

        ):

            st.session_state.page = "Detection"

            st.rerun()



    with home_col2:



        if st.button(

            "View Dashboard",

            use_container_width=True,

            key="home_view_dashboard"

        ):

            st.session_state.page = "Dashboard"

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

            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>',

            "Detect Waste",

            "Identify waste objects automatically using YOLOv8 computer vision."

        ),

        (

            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',

            "Classify Materials",

            "Recognize different waste categories such as plastic, glass, metal and paper."

        ),

        (

            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',

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

        ("Image", "Images", "Analyze uploaded waste images."),

        ("Video", "Videos", "Process recorded video files."),

        ("Camera", "Live Camera", "Detect waste in real time."),

        ("Stream", "Live Streams", "Analyze network video streams.")

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



elif page == "Dashboard":



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



                        <div class="dashboard-activity-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path></svg></div>



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



                    <div class="dashboard-empty-icon"><svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></div>



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

            "Start Detection",

            type="primary",

            use_container_width=True,

            key="dashboard_start_detection"

        ):



            st.session_state.page = "Detection"

            st.rerun()





    with action2:



        if st.button(

            "View Reports",

            use_container_width=True,

            key="dashboard_view_reports"

        ):



            st.session_state.page = "Reports"

            st.rerun()

# ============================================================

# DETECTION

# ============================================================



elif page == "Detection":



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



            <div class="detection-config-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></div>



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

            value=18,

            step=1,

            label_visibility="collapsed",

            help=(

                "Control model sensitivity. 12%–20% is recommended for mixed waste piles to catch occluded items."

            )

        )



        confidence = confidence_percent / 100



        st.caption(

            f"Current threshold: **{confidence_percent}%** · "

            "*Tip: Set to 12%–20% for mixed waste scenes to catch faint/occluded objects.*"

        )

        mode_c1, mode_c2 = st.columns(2)
        with mode_c1:
            high_res_mode = st.checkbox(
                "High-Res (1024px)",
                value=True,
                help="Preserves fine visual details on small or distant items in mixed scenes."
            )
        with mode_c2:
            tta_mode = st.checkbox(
                "Multi-Scale TTA",
                value=False,
                help="Test-Time Augmentation: boosts recall on occluded, crushed, or angled items."
            )





    # --------------------------------------------------------

    # MODEL STATUS

    # --------------------------------------------------------



    with config_col2:

        st.html("""
        <div class="detection-config-card">
            <div class="detection-config-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg></div>
            <div class="detection-config-content">
                <div class="detection-config-title">Active AI Model</div>
                <div class="detection-config-description">Select model checkpoint for detection</div>
            </div>
        </div>
        """)

        model_options = list(settings.AVAILABLE_MODELS.keys())
        current_idx = model_options.index(st.session_state.selected_model_name) if st.session_state.selected_model_name in model_options else 0
        new_selected = st.selectbox(
            "Active AI Model",
            options=model_options,
            index=current_idx,
            label_visibility="collapsed",
            key="model_select_dropdown"
        )
        if new_selected != st.session_state.selected_model_name:
            st.session_state.selected_model_name = new_selected
            st.rerun()

        model_fname = selected_info.get("filename", model_path.name)
        model_desc = selected_info.get("description", "")
        st.caption(f"Active Model: **{model_fname}** · {model_desc}")





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

                    Image Detection

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



                <div class="detection-upload-icon"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg></div>



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



                    <div class="detection-analysis-icon"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg></div>



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

                    "Detect Waste",

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

                        "Analyzing image with WasteAI model..."

                    ):



                        pred_kwargs = {
                            "conf": confidence,
                            "iou": 0.45,
                            "agnostic_nms": False,
                        }
                        if high_res_mode:
                            pred_kwargs["imgsz"] = 1024
                        if tta_mode:
                            pred_kwargs["augment"] = True

                        res = model.predict(
                            uploaded_image,
                            **pred_kwargs
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

                        summary_col1, summary_col2, summary_col3 = st.columns(3)

                        summary_cards = [



                            (

                                summary_col1,

                                '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/><path d="m14 14 3-3 3 3"/><path d="m11 5 3-3 3 3"/><path d="M14 2v6"/><path d="m6 16-3 3 3 3"/></svg>',

                                total_items,

                                "Total Waste Items"

                            ),



                            (

                                summary_col2,

                                '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',

                                unique_categories,

                                "Categories Detected"

                            ),



                            (

                                summary_col3,

                                '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',

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

                "View Detailed Analytics",

                type="primary",

                use_container_width=True,

                key="go_to_analytics"

            ):

                st.session_state.page = "Analytics"

                st.rerun()



    # ========================================================

    # VIDEO

    # ========================================================



    elif source_radio == settings.VIDEO:



        st.html("""

        <div class="detection-workspace-header">



            <div>

                <div class="detection-workspace-title">

                    Video Detection

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

                    Live Webcam Detection

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

                    YouTube Detection

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

                    RTSP Stream Detection

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



elif page == "Analytics":



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



            <div class="analytics-empty-icon"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></div>



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

                "Go to Detection",

                type="primary",

                use_container_width=True,

                key="analytics_go_detection"

            ):



                st.session_state.page = "Detection"

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



                <div class="analytics-kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 0-1.78L17 10"/><path d="m14 14 3-3 3 3"/><path d="m11 5 3-3 3 3"/><path d="M14 2v6"/><path d="m6 16-3 3 3 3"/></svg></div>



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



                <div class="analytics-kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></div>



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



                <div class="analytics-kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></div>



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



                <div class="analytics-kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>



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



            <div class="analytics-confidence-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></div>



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



elif page == "Reports":



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



            <div class="reports-empty-icon"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>



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

                "Go to Detection",

                type="primary",

                use_container_width=True,

                key="reports_go_detection"

            ):



                st.session_state.page = "Detection"



                if "top_navigation" in st.session_state:

                    st.session_state.top_navigation = "Detection"



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



                <div class="reports-summary-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path></svg></div>

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



                <div class="reports-summary-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></div>

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



                <div class="reports-summary-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ca8a04" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div>

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



            <div class="reports-export-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></div>



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

                "Download Waste Detection Report (CSV)",

                data=report_csv,

                file_name="waste_detection_report.csv",

                mime="text/csv",

                use_container_width=True,

                key="reports_page_download"

            )

            # Load email configuration safely
            def _get_app_email_config():
                cfg = {"sender": "", "password": "", "admin": ""}
                if "email_config" in st.session_state:
                    return st.session_state["email_config"]
                try:
                    if hasattr(st, "secrets") and "email" in st.secrets:
                        sec = st.secrets["email"]
                        return {
                            "sender": sec.get("sender", ""),
                            "password": sec.get("password", ""),
                            "admin": sec.get("admin", "")
                        }
                except Exception:
                    pass
                import tomllib
                candidate_paths = [
                    Path(".streamlit/secrets.toml"),
                    Path("streamlit-detection-tracking - app/.streamlit/secrets.toml"),
                    Path(__file__).resolve().parent / ".streamlit" / "secrets.toml",
                ]
                for cp in candidate_paths:
                    if cp.exists():
                        try:
                            with open(cp, "rb") as fp:
                                data = tomllib.load(fp)
                                if "email" in data:
                                    return {
                                        "sender": data["email"].get("sender", ""),
                                        "password": data["email"].get("password", ""),
                                        "admin": data["email"].get("admin", "")
                                    }
                        except Exception:
                            pass
                return cfg

            email_cfg = _get_app_email_config()
            cur_sender = email_cfg.get("sender", "")
            cur_pass = email_cfg.get("password", "")
            cur_admin = email_cfg.get("admin", "")

            is_dummy_or_empty = (
                not cur_sender or
                not cur_pass or
                not cur_admin or
                "your_email" in cur_sender.lower() or
                "your_16_character" in cur_pass.lower() or
                "example.com" in cur_admin.lower()
            )

            if st.button(
                "Send Report to Admin",
                width="stretch",
                key="reports_page_email"
            ):
                if is_dummy_or_empty:
                    st.warning("Email credentials are not configured yet! Please enter your Gmail address, 16-character App Password, and Admin email in the settings below.")
                else:
                    try:
                        with st.spinner("Connecting to Gmail SMTP and sending report..."):
                            msg = EmailMessage()
                            msg["Subject"] = "Waste Detection and Classification Report"
                            msg["From"] = cur_sender
                            msg["To"] = cur_admin
                            msg.set_content(
                                "Please find the latest waste detection "
                                "report attached as a CSV file.\n\n"
                                "This report was generated by the "
                                "Waste Detection and Classification System."
                            )
                            msg.add_attachment(
                                report_csv,
                                maintype="text",
                                subtype="csv",
                                filename="waste_detection_report.csv",
                            )

                            import socket
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
                                smtp.login(cur_sender, cur_pass)
                                smtp.send_message(msg)

                            st.success(f"Report emailed to {cur_admin} successfully!")
                    except smtplib.SMTPAuthenticationError:
                        st.error("Authentication failed: Please check your Gmail address and 16-character App Password.\n\nNote: If 2-Step Verification is enabled, you must use a Google App Password from https://myaccount.google.com/apppasswords rather than your regular account password.")
                    except (socket.timeout, TimeoutError):
                        st.error("Connection timed out: Unable to reach smtp.gmail.com within 15 seconds. Please check your internet connection or firewall.")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")

            # Expandable configuration section for user convenience
            with st.expander("Email and SMTP Configuration", expanded=is_dummy_or_empty):
                st.markdown(
                    "<div style='font-size: 0.85rem; color: #555; margin-bottom: 8px;'>"
                    "Configure your Gmail SMTP settings to enable emailing reports to admins.<br>"
                    "<b>Note:</b> Gmail requires a 16-character App Password: "
                    "Go to <a href='https://myaccount.google.com/apppasswords' target='_blank'>myaccount.google.com/apppasswords</a> to generate one."
                    "</div>",
                    unsafe_allow_html=True
                )
                input_sender = st.text_input("Sender Gmail Address", value=cur_sender if not ("your_email" in cur_sender) else "", placeholder="your_email@gmail.com", key="smtp_cfg_sender")
                input_pass = st.text_input("16-character App Password", value=cur_pass if not ("your_16_character" in cur_pass) else "", type="password", placeholder="xxxx xxxx xxxx xxxx", key="smtp_cfg_pass")
                input_admin = st.text_input("Admin / Recipient Email", value=cur_admin if not ("example.com" in cur_admin) else "", placeholder="admin@example.com", key="smtp_cfg_admin")

                if st.button("Save Email Configuration", width="stretch", key="save_smtp_cfg_btn"):
                    if not input_sender or not input_pass or not input_admin:
                        st.error("Please fill out all three fields (Sender, App Password, and Admin email).")
                    else:
                        st.session_state["email_config"] = {
                            "sender": input_sender.strip(),
                            "password": input_pass.strip(),
                            "admin": input_admin.strip()
                        }
                        toml_content = f'# Streamlit Email Configuration for Waste Detection Reports\n[email]\nsender = "{input_sender.strip()}"\npassword = "{input_pass.strip()}"\nadmin = "{input_admin.strip()}"\n'
                        for sp in [Path(".streamlit/secrets.toml"), Path("streamlit-detection-tracking - app/.streamlit/secrets.toml")]:
                            try:
                                sp.parent.mkdir(parents=True, exist_ok=True)
                                sp.write_text(toml_content, encoding="utf-8")
                            except Exception:
                                pass
                        st.success("Credentials saved successfully! You can now send reports directly.")
                        st.rerun()

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



elif page == "Settings":



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

                    Configuration Center

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



    st.markdown("### AI Model Configuration")



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



            <div style="font-size:26px;"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg></div>



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



            <div style="font-size:26px;"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>



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



    st.markdown("### Detection Configuration")



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

                Confidence Threshold

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

            value=35,

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

                Object Tracking

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



    st.markdown("### Supported Waste Categories")



    st.caption(

        "Waste categories currently supported by the detection model."

    )





    categories = [

        ("Cardboard", "CARDBOARD"),

        ("Glass", "GLASS"),

        ("Metal", "METAL"),

        ("Paper", "PAPER"),

        ("Plastic", "PLASTIC"),

        ("Organic", "BIODEGRADABLE")

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



    st.markdown("### Detection Input Sources")



    st.caption(

        "Available sources that can be used by the detection engine."

    )





    source_icons = {

        settings.IMAGE: "Image",

        settings.VIDEO: "Video",

        settings.WEBCAM: "Webcam",

        settings.YOUTUBE: "YouTube",

        settings.RTSP: "RTSP Stream"

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

                "Sensors"

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



    st.markdown("### System Information")





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