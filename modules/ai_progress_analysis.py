# modules/ai_progress_analysis.py

from modules.groq_chat import ask_groq


def analyze_progress(df):

    if df.empty:
        return "No workout data available."

    total_reps = int(df["reps"].sum())
    total_calories = round(df["calories"].sum(), 2)

    exercise_summary = (
        df.groupby("exercise")["reps"]
        .sum()
        .to_dict()
    )

    prompt = f"""
You are ShifAI Fitness Coach.

Analyze the user's progress.

Total Reps: {total_reps}
Total Calories: {total_calories}

Exercise Summary:
{exercise_summary}

Provide:

1. Progress summary
2. Strengths
3. Weaknesses
4. Recommendations
5. Motivation

Keep it under 200 words.
"""

    return ask_groq(prompt)
