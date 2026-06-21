from modules.groq_chat import ask_groq


def generate_fitness_plan(
        age,
        height,
        weight,
        bmi):

    prompt = f"""
Create a complete 7 day fitness plan.

Age: {age}
Height: {height}
Weight: {weight}
BMI: {bmi}

Include:

1. Workout schedule
2. Calories target
3. Water intake
4. Diet plan
5. Sleep recommendation

Professional format.
"""

    return ask_groq(prompt)