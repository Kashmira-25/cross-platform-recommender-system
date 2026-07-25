import streamlit as st


def login_page():

    # -----------------------------
    # Session State Initialization
    # -----------------------------
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "registered" not in st.session_state:
        st.session_state.registered = False

    # -----------------------------
    # Title
    # -----------------------------
    st.markdown(
        "<h1 style='text-align:center;'>Cross-Platform Recommendation System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:gray;'>Personalized AI Recommendation Prototype</h4>",
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # -----------------------------
    # Login / Create Account Tabs
    # -----------------------------
    left,center,right=st.columns([1,2,1])
    with center:
        login_tab, register_tab=st.tabs(
            ["Login", "Create Account"]
        )
 
    # =================================================
    # LOGIN TAB
    # =================================================
    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if email == "" or password == "":
                st.error("Please enter Email and Password.")

            else:

                st.session_state.logged_in = True

                st.success("Login Successful!")

                st.rerun()

    # =================================================
    # CREATE ACCOUNT TAB
    # =================================================
    with register_tab:

        st.subheader("Create Account")

        new_name = st.text_input(
            "Full Name"
        )

        new_email = st.text_input(
            "Email Address"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if (
                new_name == ""
                or new_email == ""
                or new_password == ""
                or confirm_password == ""
            ):

                st.error("Please fill all fields.")

            elif new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                st.session_state.registered = True

                st.success(
                    "Account created successfully!\n\nYou can now login."
                )