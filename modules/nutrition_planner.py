import streamlit as st

from user_manager import get_current_user
from database import get_user_health
from modules.groq_chat import ask_groq


def show_nutrition_planner():
    username = get_current_user()
    age, height, weight = get_user_health(username)

    bmi = weight / ((height / 100) ** 2)

    st.title("🥗 AI Nutrition Planner")

    goal = st.selectbox(
        "Select Goal",
        ["Weight Loss", "Muscle Gain", "Maintain Weight"]
    )

    preference = st.selectbox(
        "Food Preference",
        ["Normal", "Vegetarian", "High Protein", "Low Carb"]
    )

    meals = st.number_input(
        "Meals per day",
        min_value=2,
        max_value=6,
        value=3
    )

    if st.button("Generate Nutrition Plan"):
        prompt = f"""
You are ShifAI Nutrition Coach.

User:
Age: {age}
Height: {height} cm
Weight: {weight} kg
BMI: {round(bmi, 1)}

Goal: {goal}
Food Preference: {preference}
Meals per day: {meals}

Create a practical daily nutrition plan.
Include:
1. Breakfast
2. Lunch
3. Dinner
4. Snacks
5. Water intake
6. Foods to avoid
7. Simple advice

Keep it clear and easy to follow.
"""

        with st.spinner("Generating nutrition plan..."):
            plan = ask_groq(prompt)

        st.subheader("AI Nutrition Plan")
        st.write(plan)