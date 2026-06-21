import streamlit as st
import base64
from pathlib import Path


def set_background(image_path="assets/bg.png"):
    image_file = Path(image_path)

    if not image_file.exists():
        st.warning("Background image not found: assets/bg.png")
        return

    encoded = base64.b64encode(image_file.read_bytes()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0.82)),
            url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
        display: none;
    }}

    .block-container {{
        max-width: 92%;
        padding-top: 2rem;
    }}

    h1 {{
        font-size: 48px !important;
        font-weight: 900 !important;
        color: white !important;
    }}

    h2, h3, p, label {{
        color: white !important;
    }}

    div[data-testid="stImage"] {{
        margin-bottom: 35px;
    }}

    div[data-testid="stRadio"] > div {{
        background: rgba(0, 0, 0, 0.72);
        border: 1px solid rgba(0, 229, 255, 0.45);
        border-radius: 24px;
        padding: 22px 35px;
        display: flex;
        justify-content: center;
        gap: 40px;
        backdrop-filter: blur(16px);
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.12);
        margin-bottom: 55px;
    }}

    div[data-testid="stRadio"] input[type="radio"] {{
        display: none;
    }}

    div[data-testid="stRadio"] label {{
        font-size: 18px;
        font-weight: 800;
        color: white !important;
        cursor: pointer;
        white-space: nowrap;
    }}

    div[data-testid="stRadio"] label:hover {{
        color: #00e5ff !important;
    }}

    div[data-testid="metric-container"] {{
        background: rgba(0, 0, 0, 0.72);
        border: 1px solid rgba(0, 229, 255, 0.35);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.10);
    }}

    .stButton button {{
        background: linear-gradient(90deg, #00e5ff, #8a2be2);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 14px 28px;
        font-size: 17px;
        font-weight: 900;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.25);
    }}

    .stButton button:hover {{
        transform: scale(1.03);
        border: 1px solid #00e5ff;
    }}

    .stSelectbox div, .stNumberInput input, .stTextInput input {{
        background-color: rgba(20,20,30,0.95) !important;
        color: white !important;
        border-radius: 12px !important;
    }}

    [data-testid="stDataFrame"] {{
        background: rgba(0,0,0,0.65);
        border-radius: 20px;
    }}

    .stAlert {{
        border-radius: 18px;
    }}
    </style>
    """, unsafe_allow_html=True)