import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

from database import get_connection


def show_admin():
    st.title("⚙️ Admin Panel")
    st.write("Admin dashboard for managing users and workouts.")

    conn = get_connection()

    users_df = pd.read_sql_query(
        """
        SELECT id, username, full_name, role, created_at
        FROM users
        ORDER BY created_at DESC
        """,
        conn
    )

    workouts_df = pd.read_sql_query(
        """
        SELECT id, username, date, exercise, reps, calories
        FROM workouts
        ORDER BY date DESC
        """,
        conn
    )

    conn.close()

    st.subheader("📊 System Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Users", len(users_df))
    col2.metric("🏋️ Workouts", len(workouts_df))

    if not workouts_df.empty:
        col3.metric("🔢 Total Reps", int(workouts_df["reps"].sum()))
        col4.metric("🔥 Calories", round(workouts_df["calories"].sum(), 2))
    else:
        col3.metric("🔢 Total Reps", 0)
        col4.metric("🔥 Calories", 0)

    st.divider()

    st.subheader("👥 Users")
    st.dataframe(users_df, use_container_width=True)

    st.subheader("🏋️ All Workout Records")

    if workouts_df.empty:
        st.warning("No workout records found.")
        return

    st.dataframe(workouts_df, use_container_width=True)

    st.subheader("🏆 User Leaderboard")

    leaderboard = workouts_df.groupby("username", as_index=False).agg({
        "reps": "sum",
        "calories": "sum"
    })

    leaderboard = leaderboard.sort_values("reps", ascending=False)

    st.dataframe(leaderboard, use_container_width=True)

    fig_leaderboard = px.bar(
        leaderboard,
        x="username",
        y="reps",
        title="User Leaderboard by Reps",
        text="reps"
    )

    st.plotly_chart(fig_leaderboard, use_container_width=True)

    st.subheader("📌 Most Popular Exercise")

    exercise_chart = workouts_df.groupby("exercise", as_index=False)["reps"].sum()

    fig_exercise = px.pie(
        exercise_chart,
        names="exercise",
        values="reps",
        title="Exercise Popularity"
    )

    st.plotly_chart(fig_exercise, use_container_width=True)

    csv_data = workouts_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download All Workouts",
        csv_data,
        "all_workouts.csv",
        "text/csv"
    )
    
    st.subheader("📊 Export Excel Report")

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        users_df.to_excel(writer, index=False, sheet_name="Users")
        workouts_df.to_excel(writer, index=False, sheet_name="Workouts")
        leaderboard.to_excel(writer, index=False, sheet_name="Leaderboard")

    st.download_button(
        label="📥 Download Excel Report",
        data=excel_buffer.getvalue(),
        file_name="shifai_admin_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.subheader("📄 Export PDF Report")

    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, "ShifAI Admin Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 90, f"Total Users: {len(users_df)}")
    pdf.drawString(50, height - 115, f"Total Workouts: {len(workouts_df)}")

    if not workouts_df.empty:
        pdf.drawString(50, height - 140, f"Total Reps: {int(workouts_df['reps'].sum())}")
        pdf.drawString(50, height - 165, f"Total Calories: {round(workouts_df['calories'].sum(), 2)}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 210, "Leaderboard")

    y = height - 240
    pdf.setFont("Helvetica", 11)

    for index, row in leaderboard.head(10).iterrows():
        pdf.drawString(
            50,
            y,
            f"{row['username']} - Reps: {int(row['reps'])}, Calories: {round(row['calories'], 2)}"
        )
        y -= 22

    pdf.save()
    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_buffer,
        file_name="shifai_admin_report.pdf",
        mime="application/pdf"
    )