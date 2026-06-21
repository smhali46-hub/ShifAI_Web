import streamlit as st
import speech_recognition as sr


def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""


def show_voice_assistant():
    st.title("🎤 Voice Assistant")
    st.write("Say: Home, Workout, Dashboard, Nutrition, Progress, Goals, Chat, or Profile.")

    if st.button("🎙 Start Listening"):
        command = listen_command()

        if not command:
            st.error("Sorry, I could not understand.")
            return

        st.success(f"You said: {command}")

        if "home" in command:
            st.session_state["voice_page"] = "Home"

        elif "workout" in command:
            st.session_state["voice_page"] = "Workout"

        elif "dashboard" in command:
            st.session_state["voice_page"] = "Dashboard"

        elif "nutrition" in command or "diet" in command:
            st.session_state["voice_page"] = "Nutrition"

        elif "progress" in command:
            st.session_state["voice_page"] = "Progress"

        elif "goal" in command:
            st.session_state["voice_page"] = "Goals"

        elif "chat" in command:
            st.session_state["voice_page"] = "Chat"

        elif "profile" in command:
            st.session_state["voice_page"] = "Profile"

        else:
            st.warning("Command not recognized.")
            return

        st.rerun()