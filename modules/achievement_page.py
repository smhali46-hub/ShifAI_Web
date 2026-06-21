import streamlit as st
import pandas as pd

from user_manager import get_current_user
from database import get_connection


def get_workouts(username):
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT date, exercise, reps, calories
        FROM workouts
        WHERE username = ?
        ORDER BY date ASC
        """,
        conn,
        params=(username,)
    )

    conn.close()
    return df


def calculate_streak(df):
    if df.empty:
        return 0

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    workout_days = sorted(df["date"].dt.date.unique(), reverse=True)

    streak = 0
    today = pd.Timestamp.today().date()

    for i, day in enumerate(workout_days):
        expected_day = today - pd.Timedelta(days=i)

        if day == expected_day:
            streak += 1
        else:
            break

    return streak


def show_achievements():
    username = get_current_user()
    df = get_workouts(username)

    st.title("🏆 Achievements & Streaks")
    st.write("Track your badges, consistency and fitness milestones.")

    if df.empty:
        st.warning("No workouts yet. Complete your first workout to unlock badges.")
        return

    total_workouts = len(df)
    total_reps = int(df["reps"].sum())
    total_calories = round(df["calories"].sum(), 2)
    exercise_count = df["exercise"].nunique()
    streak = calculate_streak(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🔥 Streak", f"{streak} days")
    c2.metric("🏋️ Workouts", total_workouts)
    c3.metric("🔢 Reps", total_reps)
    c4.metric("⚡ Calories", total_calories)

    st.divider()

    st.subheader("Unlocked Badges")

    badges = []

    if total_workouts >= 1:
        badges.append("🏆 First Workout")

    if total_workouts >= 5:
        badges.append("🔥 5 Workout Champion")

    if total_reps >= 100:
        badges.append("💯 100 Reps Club")

    if total_reps >= 500:
        badges.append("👑 500 Reps Master")

    if total_calories >= 100:
        badges.append("⚡ 100 Calories Burned")

    if exercise_count >= 3:
        badges.append("🏋️ Complete Athlete")

    if streak >= 3:
        badges.append("🔥 3 Day Streak")

    if streak >= 7:
        badges.append("🚀 7 Day Streak")

    if badges:
        for badge in badges:
            st.success(badge)
    else:
        st.info("No badges unlocked yet.")