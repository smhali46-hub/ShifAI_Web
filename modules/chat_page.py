import streamlit as st

from user_manager import get_current_user
from database import (
    save_chat_message,
    get_chat_history,
    get_user_health,
    get_user_stats
)

from modules.groq_chat import ask_groq


def show_chat():

    username = get_current_user()

    st.title("🤖 ShifAI AI Coach")

    history = get_chat_history(username)

    for sender, message in history:

        if sender == "You":
            st.info(message)

        else:
            st.success(message)

    user_input = st.chat_input(
        "Ask your AI Fitness Coach..."
    )

    if user_input:

        age, height, weight = get_user_health(username)

        workouts, reps, calories = get_user_stats(username)

        bmi = weight / ((height / 100) ** 2)

        prompt = f"""
You are ShifAI AI Fitness Coach.

User Information:

Age: {age}
Height: {height} cm
Weight: {weight} kg
BMI: {round(bmi,1)}

Workout Summary:

Total Workouts: {workouts}
Total Reps: {reps}
Total Calories Burned: {calories}

Provide professional fitness, workout and nutrition advice.

User Question:
{user_input}
"""

        reply = ask_groq(prompt)

        save_chat_message(
            username,
            "You",
            user_input
        )

        save_chat_message(
            username,
            "ShifAI",
            reply
        )

        st.rerun()