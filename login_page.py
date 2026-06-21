import streamlit as st

from database import create_user, validate_user, get_user_role
from user_manager import set_current_user, logout_user


def show_login():
    st.title("🔐 ShifAI Login")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):
            if not username or not password:
                st.warning("Please enter username and password.")
                return

            if validate_user(username, password):
                role = get_user_role(username)

                set_current_user(username)

                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role

                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        full_name = st.text_input("Full Name", key="new_fullname")
        new_username = st.text_input("New Username", key="new_username")
        new_password = st.text_input(
            "New Password",
            type="password",
            key="new_password"
        )

        if st.button("Create Account"):
            if not new_username or not new_password:
                st.warning("Please enter username and password.")
                return

            status, message = create_user(
                new_username,
                new_password,
                full_name
            )

            if status:
                st.success(message)
                st.info("Now go to Login tab and login.")
            else:
                st.error(message)


def logout():
    logout_user()

    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    st.rerun()