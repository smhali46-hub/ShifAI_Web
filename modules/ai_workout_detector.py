import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

from database import save_workout_db
from user_manager import get_current_user


mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


def start_ai_detection(exercise):
    st.warning("Camera will open. Press Q to stop and save workout.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Camera not found.")
        return

    reps = 0
    stage = None
    feedback = "Get Ready"

    with mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as pose:

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                try:
                    if exercise == "Squat":
                        hip = [
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                        ]
                        knee = [
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
                        ]
                        ankle = [
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
                        ]

                        angle = calculate_angle(hip, knee, ankle)

                        if angle > 160:
                            stage = "up"
                            feedback = "Stand Tall"

                        if angle < 95 and stage == "up":
                            stage = "down"
                            feedback = "Good Depth"

                        if angle > 160 and stage == "down":
                            stage = "up"
                            reps += 1
                            feedback = "Squat Rep Counted"

                    elif exercise == "Push-Up":
                        shoulder = [
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                        ]
                        elbow = [
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
                        ]
                        wrist = [
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                        ]

                        angle = calculate_angle(shoulder, elbow, wrist)

                        if angle > 160:
                            stage = "up"
                            feedback = "Arms Straight"

                        if angle < 90 and stage == "up":
                            stage = "down"
                            feedback = "Good Push-Up Depth"

                        if angle > 160 and stage == "down":
                            stage = "up"
                            reps += 1
                            feedback = "Push-Up Rep Counted"

                    elif exercise == "Bicep Curl":
                        shoulder = [
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                        ]
                        elbow = [
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
                        ]
                        wrist = [
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                        ]

                        angle = calculate_angle(shoulder, elbow, wrist)

                        if angle > 150:
                            stage = "down"
                            feedback = "Arm Extended"

                        if angle < 45 and stage == "down":
                            stage = "up"
                            reps += 1
                            feedback = "Curl Rep Counted"

                    mp_draw.draw_landmarks(
                        image_bgr,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )

                except Exception:
                    feedback = "Body not clear"

            cv2.rectangle(image_bgr, (0, 0), (520, 170), (0, 0, 0), -1)

            cv2.putText(
                image_bgr,
                f"Exercise: {exercise}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            cv2.putText(
                image_bgr,
                f"Reps: {reps}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 255, 0),
                3
            )

            cv2.putText(
                image_bgr,
                f"Feedback: {feedback}",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )

            cv2.putText(
                image_bgr,
                "Press Q to Stop",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 180, 0),
                2
            )

            cv2.imshow("ShifAI AI Workout Detection", image_bgr)

            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

    if reps > 0:
        username = get_current_user()
        calories = round(reps * 0.3, 2)

        save_workout_db(username, exercise, reps, calories)

        st.success(
            f"{exercise} completed successfully. "
            f"Reps: {reps}, Calories: {calories}"
        )
    else:
        st.warning("No reps detected.")