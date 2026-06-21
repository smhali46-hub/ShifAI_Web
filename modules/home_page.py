import streamlit as st


def show_home():
    st.title("💪 ShifAI Fitness Assistant")
    st.subheader("AI Gym Fitness Progress Monitoring System")

    st.write(
        "ShifAI is an AI-powered fitness assistant that helps users track workouts, "
        "monitor progress, calculate BMI, generate nutrition plans, and receive "
        "personalized AI coaching."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("🏋️ Exercises", "Squat, Push-Up, Curl")
    col2.metric("🤖 AI Coach", "Groq Powered")
    col3.metric("📊 Analytics", "Live Dashboard")

    st.divider()

    st.subheader("🚀 Main Features")

    c1, c2 = st.columns(2)

    with c1:
        st.write("✅ AI workout detection")
        st.write("✅ Rep counting")
        st.write("✅ Calories tracking")
        st.write("✅ Fitness score")
        st.write("✅ Achievements")

    with c2:
        st.write("✅ BMI calculation")
        st.write("✅ AI nutrition planner")
        st.write("✅ Groq AI chat coach")
        st.write("✅ Voice assistant")
        st.write("✅ Admin dashboard")

    st.divider()
    
  

    st.subheader("📌 How to Use")

    st.write("1. Create an account or login.")
    st.write("2. Update your profile with age, height and weight.")
    st.write("3. Set your daily goals.")
    st.write("4. Start workout detection.")
    st.write("5. Track your progress in the dashboard.")
    st.write("6. Use AI Chat and Nutrition Planner for personalized guidance.")

    st.divider()

    st.success("Start your fitness journey with ShifAI — Train smarter with AI.")

    st.divider()
    st.subheader("📖 About ShifAI")

    st.write("""
    **ShifAI Fitness Assistant** is an AI-powered fitness management platform
    designed to help users improve their health and fitness journey through
    intelligent workout tracking, nutrition planning, progress monitoring,
    and personalized AI coaching.

    The system combines Artificial Intelligence, Computer Vision, Data Analytics,
    and Generative AI to provide a smart fitness experience for users of all levels.
    """)

    st.subheader("🛠 Project Information")

    st.write("""
    **Project Name:** ShifAI Fitness Assistant

    **Version:** 1.0

    **Technology Stack:**
    - Python
    - Streamlit
    - SQLite
    - MediaPipe
    - OpenCV
    - Plotly
    - Groq AI (Llama 3)
    - Pandas

    **Core Modules:**
    - User Management
    - AI Workout Detection
    - Dashboard Analytics
    - Nutrition Planner
    - BMI Analysis
    - AI Fitness Coach
    - Voice Assistant
    - Admin Panel
    """)

    st.subheader("👨‍💻 Developer Information")

    st.info("""
    Developer: Mohamed Hasan Ali

    Project: ShifAI Fitness Assistant

    Role:
    AI Developer | System Designer | Full Stack Developer

    Skills Used:
    - Artificial Intelligence
    - Computer Vision
    - Generative AI
    - Python Development
    - Database Management
    - Data Analytics

    © 2026 ShifAI Fitness Assistant
    """)