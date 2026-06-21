import streamlit as st
import pandas as pd
import plotly.express as px

from user_manager import get_current_user
from database import get_connection, get_user_goal
from modules.ai_progress_analysis import analyze_progress


def get_user_workouts_from_db(username):
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


def calculate_fitness_score(df):
    if df.empty:
        return 0

    total_reps = df["reps"].sum()
    total_calories = df["calories"].sum()
    exercise_variety = df["exercise"].nunique()
    workout_count = len(df)

    consistency_score = min(workout_count * 5, 100)
    reps_score = min(total_reps / 5, 100)
    calorie_score = min(total_calories * 2, 100)
    variety_score = min(exercise_variety * 30, 100)

    score = (
        consistency_score * 0.30 +
        reps_score * 0.30 +
        calorie_score * 0.20 +
        variety_score * 0.20
    )

    return round(score, 1)


def get_fitness_level(score):
    if score >= 90:
        return "💎 Elite Athlete"
    elif score >= 75:
        return "👑 Advanced Athlete"
    elif score >= 50:
        return "🔥 Intermediate Athlete"
    else:
        return "🚀 Beginner Athlete"


def calculate_streak(df):
    if df.empty:
        return 0

    temp_df = df.copy()
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce")

    workout_days = sorted(
        temp_df["date"].dt.date.dropna().unique(),
        reverse=True
    )

    streak = 0
    today = pd.Timestamp.today().date()

    for i, day in enumerate(workout_days):
        expected_day = today - pd.Timedelta(days=i)

        if day == expected_day:
            streak += 1
        else:
            break

    return streak


def get_badges(total_workouts, total_reps, total_calories, exercise_count, streak):
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

    return badges


def show_dashboard():
    username = get_current_user()
    df = get_user_workouts_from_db(username)

    st.title("📊 Fitness Dashboard")
    st.write("Workout summary, progress analytics, achievements and AI insights.")

    if df.empty:
        st.warning("No workout data found. Please save a workout first.")
        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["day"] = df["date"].dt.date

    total_workouts = len(df)
    total_reps = int(df["reps"].sum())
    total_calories = round(df["calories"].sum(), 2)
    best_exercise = df["exercise"].mode()[0]
    exercise_count = df["exercise"].nunique()
    streak = calculate_streak(df)
    fitness_score = calculate_fitness_score(df)
    fitness_level = get_fitness_level(fitness_score)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("🏋️ Workouts", total_workouts)
    col2.metric("🔢 Reps", total_reps)
    col3.metric("🔥 Calories", total_calories)
    col4.metric("⭐ Best", best_exercise)
    col5.metric("🔥 Streak", f"{streak} days")

    st.divider()

    st.subheader("🏅 Fitness Score")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.metric("Overall Fitness Score", f"{fitness_score}/100")
        st.metric("Fitness Level", fitness_level)

    with c2:
        st.progress(fitness_score / 100)

        if fitness_score >= 90:
            st.success("Excellent performance. You are in elite range.")
        elif fitness_score >= 75:
            st.success("Great progress. You are an advanced athlete.")
        elif fitness_score >= 50:
            st.info("Good work. Keep improving your consistency.")
        else:
            st.warning("Beginner level. Stay consistent and build momentum.")

    st.divider()

    st.subheader("🎯 Daily Goal Progress")

    reps_goal, calories_goal = get_user_goal(username)

    today = pd.Timestamp.today().date()
    today_df = df[df["day"] == today]

    today_reps = int(today_df["reps"].sum())
    today_calories = round(today_df["calories"].sum(), 2)

    reps_progress = min(today_reps / reps_goal, 1.0)
    calories_progress = min(today_calories / calories_goal, 1.0)

    st.write(f"Reps: {today_reps} / {reps_goal}")
    st.progress(reps_progress)

    st.write(f"Calories: {today_calories} / {calories_goal}")
    st.progress(calories_progress)

    st.divider()

    st.subheader("🏆 Achievements")

    badges = get_badges(
        total_workouts,
        total_reps,
        total_calories,
        exercise_count,
        streak
    )

    if badges:
        badge_cols = st.columns(4)

        for i, badge in enumerate(badges):
            with badge_cols[i % 4]:
                st.success(badge)
    else:
        st.info("No achievements unlocked yet.")

    st.divider()

    st.subheader("🤖 AI Progress Analysis")

    if st.button("Generate AI Analysis"):
        with st.spinner("ShifAI is analyzing your progress..."):
            analysis = analyze_progress(df)

        st.info(analysis)

    st.divider()

    st.subheader("📋 Workout History")
    st.dataframe(df, use_container_width=True)

    st.subheader("🏋️ Reps by Exercise")

    reps_chart = df.groupby("exercise", as_index=False)["reps"].sum()

    fig_reps = px.bar(
        reps_chart,
        x="exercise",
        y="reps",
        title="Reps by Exercise",
        text="reps"
    )

    st.plotly_chart(fig_reps, use_container_width=True)

    st.subheader("🔥 Calories by Exercise")

    calories_chart = df.groupby("exercise", as_index=False)["calories"].sum()

    fig_calories = px.bar(
        calories_chart,
        x="exercise",
        y="calories",
        title="Calories by Exercise",
        text="calories"
    )

    st.plotly_chart(fig_calories, use_container_width=True)

    st.subheader("📅 Daily Progress")

    daily_progress = df.groupby("day", as_index=False)[["reps", "calories"]].sum()

    fig_daily = px.line(
        daily_progress,
        x="day",
        y=["reps", "calories"],
        title="Daily Reps and Calories Progress",
        markers=True
    )

    st.plotly_chart(fig_daily, use_container_width=True)

    st.subheader("📅 Workout Calendar")

    calendar_data = (
        df.groupby("day", as_index=False)["reps"]
        .sum()
        .rename(columns={"day": "Date", "reps": "Total Reps"})
    )

    st.dataframe(calendar_data, use_container_width=True)