import cv2
import streamlit as st
from datetime import datetime
from database import save_workout_db
from user_manager import get_current_user


def start_ai_detection(exercise):
    st.warning("Camera window will open. Press Q to stop detection.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Camera not found.")
        return

    reps = 0
    calories = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.putText(
            frame,
            f"Exercise: {exercise}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Reps: {reps}",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Press SPACE to count rep | Q to quit",
            (30, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow("ShifAI AI Workout Detection", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):
            reps += 1

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if reps > 0:
        username = get_current_user()
        calories = round(reps * 0.3, 2)
        save_workout_db(username, exercise, reps, calories)

        st.success(
            f"AI Detection completed. {exercise}: {reps} reps, {calories} calories saved."
        )
    else:
        st.info("No reps counted.")