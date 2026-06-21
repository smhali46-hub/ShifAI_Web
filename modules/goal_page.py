import streamlit as st

from user_manager import get_current_user
from database import get_user_goal, save_user_goal


def show_goals():
    username = get_current_user()

    st.title("🎯 Fitness Goals")
    st.write("Set your daily workout targets.")

    current_reps, current_calories = get_user_goal(username)

    reps_goal = st.number_input(
        "Daily Reps Goal",
        min_value=10,
        max_value=1000,
        value=int(current_reps),
        step=10
    )

    calories_goal = st.number_input(
        "Daily Calories Goal",
        min_value=10,
        max_value=1000,
        value=int(current_calories),
        step=10
    )

    if st.button("💾 Save Goals"):
        save_user_goal(username, reps_goal, calories_goal)
        st.success("Goals saved successfully.")