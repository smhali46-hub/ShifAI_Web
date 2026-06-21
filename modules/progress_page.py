import streamlit as st
import pandas as pd

from user_manager import get_progress_file

def show_progress():


    progress_file = get_progress_file()

    st.title("📈 Progress Tracker")
    st.write("Daily reps and calorie progress.")

    if not progress_file.exists():
        st.warning("No progress data found.")
        return

    df = pd.read_csv(progress_file)

    if df.empty:
        st.warning("Progress file is empty.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Day"] = df["Date"].dt.date

    daily_progress = df.groupby("Day")[["Reps", "Calories"]].sum()

    st.subheader("Daily Reps")
    st.line_chart(daily_progress["Reps"])

    st.subheader("Daily Calories")
    st.line_chart(daily_progress["Calories"])

    st.subheader("Progress Summary")
    st.dataframe(daily_progress, use_container_width=True)
