import streamlit as st
from pathlib import Path
from modules.ai_fitness_plan import generate_7_day_plan

from user_manager import get_current_user
from database import (
    get_user_profile,
    get_user_stats,
    get_user_health,
    update_user_health
)

PROFILE_DIR = Path("users/profile_photos")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def show_profile():

    username = get_current_user()

    profile = get_user_profile(username)

    if not profile:
        st.error("User profile not found.")
        return

    username, full_name, role, created_at = profile

    total_workouts, total_reps, total_calories = get_user_stats(username)

    st.title("👤 User Profile")

    # ==================================
    # Profile Photo
    # ==================================

    photo_path = PROFILE_DIR / f"{username}.png"

    col_photo, col_info = st.columns([1, 2])

    with col_photo:

        if photo_path.exists():
            st.image(str(photo_path), width=200)
        else:
            st.info("No profile photo uploaded")

        uploaded_photo = st.file_uploader(
            "Upload Photo",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded_photo:

            photo_path.write_bytes(
                uploaded_photo.getbuffer()
            )

            st.success("Photo uploaded successfully.")
            st.rerun()

    # ==================================
    # Account Information
    # ==================================

    with col_info:

        st.subheader("Account Information")

        st.write(f"**Full Name:** {full_name}")
        st.write(f"**Username:** {username}")
        st.write(f"**Role:** {role}")
        st.write(f"**Joined:** {created_at}")

    st.divider()

    # ==================================
    # Health Profile
    # ==================================

    health = get_user_health(username)

    if health:
        age, height, weight = health
    else:
        age, height, weight = 25, 170, 70

    st.subheader("🏥 Health Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=int(age or 25)
        )

    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=int(height or 170)
        )

    with col3:
        weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=300,
            value=int(weight or 70)
        )

    if st.button("💾 Save Health Profile"):

        update_user_health(
            username,
            age,
            height,
            weight
        )

        st.success("Health profile updated.")

    # ==================================
    # BMI
    # ==================================

    bmi = weight / ((height / 100) ** 2)

    st.subheader("📊 BMI Analysis")

    bmi_col1, bmi_col2 = st.columns([1, 2])

    with bmi_col1:
        st.metric(
            "BMI Score",
            round(bmi, 1)
        )

    with bmi_col2:

        if bmi < 18.5:
            category = "Underweight"
            st.warning("⚠️ Underweight")

        elif bmi < 25:
            category = "Normal Weight"
            st.success("✅ Normal Weight")

        elif bmi < 30:
            category = "Overweight"
            st.warning("⚠️ Overweight")

        else:
            category = "Obese"
            st.error("🚨 Obese")

        st.write(f"**Category:** {category}")

    if st.button("🎯 Generate AI Fitness Plan"):

        from modules.ai_plan_generator import generate_fitness_plan

        plan = generate_fitness_plan(
            age,
            height,
            weight,
            bmi
        )

        st.subheader("AI Generated Fitness Plan")
        st.write(plan)
        
    st.divider()

    #####
    #Weekly Planner
    st.subheader("🎯 AI 7-Day Fitness Plan")

    if st.button("Generate 7-Day AI Fitness Plan"):
        bmi = weight / ((height / 100) ** 2)

        with st.spinner("Generating your personalized fitness plan..."):
            plan = generate_7_day_plan(
                age,
                height,
                weight,
                bmi,
                total_workouts,
                total_reps,
                total_calories
            )

        st.write(plan)

    # ==================================
    # Fitness Summary
    # ==================================

    st.subheader("🏋️ Fitness Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Workouts",
            total_workouts
        )

    with c2:
        st.metric(
            "Total Reps",
            total_reps
        )

    with c3:
        st.metric(
            "Calories Burned",
            round(total_calories, 2)
        )