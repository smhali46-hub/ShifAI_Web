import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from user_manager import get_progress_file
from user_manager import get_current_user
from database import save_workout_db
#from modules.ai_workout_detector import start_ai_detection


def save_workout(exercise, reps):
    username = get_current_user()
    progress_file = get_progress_file()
    progress_file.parent.mkdir(exist_ok=True)

    calories = round(reps * 0.3, 2)
    save_workout_db(username, exercise, reps, calories)

    new_row = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Exercise": exercise,
        "Reps": reps,
        "Calories": calories
    }])

    if progress_file.exists():
        old_data = pd.read_csv(progress_file)
        final_data = pd.concat([old_data, new_row], ignore_index=True)
    else:
        final_data = new_row

    final_data.to_csv(progress_file, index=False)

    return calories


def show_workout():
    st.title("🏋️ Workout Detection")
    st.write("Select workout, view guide image/video, and save your reps.")

    exercise = st.selectbox(
        "Select Exercise",
        ["Squat", "Push-Up", "Bicep Curl"]
    )

    image_map = {
        "Squat": "assets/squat.png",
        "Push-Up": "assets/pushup.png",
        "Bicep Curl": "assets/bicepcurl.png"
    }

    video_map = {
        "Squat": "assets/videos/squat.mp4",
        "Push-Up": "assets/videos/pushup.mp4",
        "Bicep Curl": "assets/videos/bicepcurl.mp4"
    }

    col_img, col_video = st.columns(2)

    with col_img:
        st.subheader("Exercise Guide Image")
        image_path = Path(image_map[exercise])

        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.warning(f"Image not found: {image_path}")

    with col_video:
        st.subheader("Exercise Guide Video")
        video_path = Path(video_map[exercise])

        if video_path.exists():
            st.video(str(video_path))
        else:
            st.warning(f"Video not found: {video_path}")

    reps = st.number_input(
        "Enter Reps",
        min_value=1,
        max_value=500,
        value=10,
        step=1
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Workout"):
            calories = save_workout(exercise, reps)
            st.success(
                f"{exercise} saved successfully. "
                f"Reps: {reps}, Calories: {calories}"
            )

    #with col2:
     #   if st.button("🎯 Start AI Detection"):
     #   st.warning("AI camera detection is available in the local desktop version only.")

    if st.session_state.get("run_detection", False):
        st.success("AI Detection Started")
        st.info("Next step: connect workout_detector.py here.")
