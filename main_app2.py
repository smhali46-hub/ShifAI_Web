import streamlit as st
from pathlib import Path

from style import set_background
from login_page import show_login, logout
from user_manager import get_current_user
from database import init_db, get_user_role

from modules.home_page import show_home
from modules.workout_page import show_workout
from modules.dashboard_page import show_dashboard
from modules.nutrition_page import show_nutrition
from modules.progress_page import show_progress
from modules.admin_page import show_admin
from modules.profile_page import show_profile
from modules.chat_page import show_chat
from modules.goal_page import show_goals
from modules.voice_assistant import show_voice_assistant
from modules.nutrition_planner import show_nutrition_planner


st.set_page_config(
    page_title="ShifAI Assistant",
    page_icon="💪",
    layout="wide"
)

Path("users").mkdir(exist_ok=True)

init_db()
set_background()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if not st.session_state["logged_in"]:
    show_login()
    st.stop()

username = get_current_user()
role = get_user_role(username)

if role == "admin":
    menu_items = ["Home", "Workout", "Dashboard", "Nutrition", "Progress", "Goals", "Chat", "Voice", "Profile", "Admin"]
else:
    menu_items = ["Home", "Workout", "Dashboard", "Nutrition", "Progress", "Goals", "Chat", "Voice", "Profile"]

col1, col2 = st.columns([5, 1])

with col1:
    if Path("assets/logo.png").exists():
        st.image("assets/logo.png", width=280)
    else:
        st.title("ShifAI Assistant")

with col2:
    st.write(f"👤 {username}")
    if st.button("🚪 Logout"):
        logout()



selected_menu = st.radio(
    "Menu",
    menu_items,
    horizontal=True,
    label_visibility="collapsed"
)

if "voice_page" in st.session_state:
    page = st.session_state["voice_page"]
    del st.session_state["voice_page"]
else:
    page = selected_menu

if page == "Home":
    show_home()

elif page == "Workout":
    show_workout()

elif page == "Dashboard":
    show_dashboard()

elif page == "Nutrition":
    show_nutrition()

elif page == "Progress":
    show_progress()

elif page == "Goals":
    show_goals()

elif page == "Chat":
    show_chat()

elif page == "Voice":
    show_voice_assistant()

elif page == "Profile":
    show_profile()

elif page == "Admin" and role == "admin":
    show_admin()