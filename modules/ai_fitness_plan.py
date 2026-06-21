from modules.groq_chat import ask_groq


def generate_7_day_plan(age, height, weight, bmi, total_workouts, total_reps, total_calories):
    prompt = f"""
You are ShifAI AI Personal Trainer.

Create a 7-day fitness plan for this user.

User:
Age: {age}
Height: {height} cm
Weight: {weight} kg
BMI: {round(bmi, 1)}

Fitness History:
Total Workouts: {total_workouts}
Total Reps: {total_reps}
Total Calories Burned: {total_calories}

Include:
1. Daily workout plan
2. Exercise recommendations
3. Rest day
4. Nutrition tips
5. Water intake
6. Motivation

Keep it practical and beginner-friendly.
"""

    return ask_groq(prompt)