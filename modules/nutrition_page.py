import streamlit as st

from user_manager import get_current_user
from database import get_user_health
from modules.groq_chat import ask_groq


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "⚠️"
    elif bmi < 25:
        return "Normal Weight", "✅"
    elif bmi < 30:
        return "Overweight", "⚠️"
    else:
        return "Obese", "🚨"


def show_nutrition():
    username = get_current_user()

    st.title("🥗 Nutrition Center")
    st.write("Food calories, AI meal planning, BMI advice and water intake.")

    health = get_user_health(username)

    if health:
        age, height, weight = health
    else:
        age, height, weight = 25, 170, 70

    age = age or 25
    height = height or 170
    weight = weight or 70

    bmi = weight / ((height / 100) ** 2)
    bmi_category, bmi_icon = get_bmi_category(bmi)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Food Analysis", "AI Meal Plan", "BMI Advice", "Water Intake"]
    )

    # ==========================
    # TAB 1: FOOD ANALYSIS
    # ==========================
    with tab1:
        st.subheader("🍽 Food Calorie Checker")

        calories_data = {
            "Apple": 95,
            "Banana": 105,
            "Rice": 205,
            "Chicken Breast": 165,
            "Egg": 78,
            "Milk": 120,
            "Chapati": 120,
            "Fish": 206,
            "Burger": 354,
            "Pizza Slice": 285,
            "Oats": 150,
            "Salad": 80
        }

        food = st.selectbox("Select Food", list(calories_data.keys()))

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

        total_calories = calories_data[food] * quantity

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Food", food)

        with col2:
            st.metric("Estimated Calories", f"{total_calories} kcal")

        st.info("Note: Calories are approximate values.")

    # ==========================
    # TAB 2: AI MEAL PLAN
    # ==========================
    with tab2:
        st.subheader("🤖 AI Nutrition Planner")

        goal = st.selectbox(
            "Fitness Goal",
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
            value=3,
            step=1
        )

        if st.button("Generate AI Meal Plan"):
            prompt = f"""
You are ShifAI Nutrition Coach.

Create a practical daily nutrition plan.

User Details:
Age: {age}
Height: {height} cm
Weight: {weight} kg
BMI: {round(bmi, 1)}
BMI Category: {bmi_category}

Goal: {goal}
Food Preference: {preference}
Meals per day: {meals}

Include:
1. Breakfast
2. Lunch
3. Dinner
4. Snacks
5. Water intake
6. Foods to avoid
7. Simple daily advice

Keep it clear, practical and beginner friendly.
"""

            with st.spinner("Generating AI nutrition plan..."):
                plan = ask_groq(prompt)

            st.subheader("AI Generated Nutrition Plan")
            st.write(plan)

    # ==========================
    # TAB 3: BMI ADVICE
    # ==========================
    with tab3:
        st.subheader("📊 BMI Nutrition Advice")

        col1, col2, col3 = st.columns(3)

        col1.metric("BMI", round(bmi, 1))
        col2.metric("Category", f"{bmi_icon} {bmi_category}")
        col3.metric("Weight", f"{weight} kg")

        if bmi < 18.5:
            st.warning("You are underweight. Focus on healthy calorie surplus and strength training.")
        elif bmi < 25:
            st.success("Your BMI is in the normal range. Focus on balanced nutrition and consistency.")
        elif bmi < 30:
            st.warning("You are overweight. Focus on calorie control, protein intake and regular activity.")
        else:
            st.error("Your BMI is high. Focus on sustainable weight loss and consult a health professional if needed.")

        if st.button("Get AI BMI Advice"):
            prompt = f"""
You are ShifAI Fitness and Nutrition Coach.

User:
Age: {age}
Height: {height} cm
Weight: {weight} kg
BMI: {round(bmi, 1)}
BMI Category: {bmi_category}

Give personalized nutrition advice.
Include:
1. Current BMI meaning
2. Food recommendation
3. Workout recommendation
4. What to avoid
5. 3 simple daily habits

Keep it short and practical.
"""

            with st.spinner("Generating BMI advice..."):
                advice = ask_groq(prompt)

            st.subheader("AI BMI Advice")
            st.write(advice)

    # ==========================
    # TAB 4: WATER INTAKE
    # ==========================
    with tab4:
        st.subheader("💧 Daily Water Intake")

        water_liters = round((weight * 35) / 1000, 1)

        st.metric("Recommended Water Intake", f"{water_liters} L/day")

        st.write("General formula used: 35 ml per kg body weight.")

        st.success(
            f"For your weight of {weight} kg, try to drink around {water_liters} liters of water per day."
        )

        st.info(
            "Increase water intake if you exercise heavily, sweat more, or live in a hot climate."
        )