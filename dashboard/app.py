from pathlib import Path
import pandas as pd
import streamlit as st

# ---------------------------------------------------
# Base directory
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# File paths
# ---------------------------------------------------
integrated_data_path = BASE_DIR / "data" / "processed" / "integrated_user_data.csv"
user_profile_path = BASE_DIR / "data" / "processed" / "user_interest_profile.csv"
recommendations_path = BASE_DIR / "data" / "processed" / "user_recommendations.csv"

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(page_title="Cross-Platform Recommender System", layout="wide")

st.title("Cross-Platform Recommender System")
st.write("A system that integrates multi-platform user activity and generates personalized recommendations.")

# ---------------------------------------------------
# Load datasets
# ---------------------------------------------------
integrated_df = pd.read_csv(integrated_data_path)
profile_df = pd.read_csv(user_profile_path)
recommendation_df = pd.read_csv(recommendations_path)

# ---------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Integrated Data", "User Profile", "Recommendations"]
)

# ---------------------------------------------------
# Sidebar user selection
# ---------------------------------------------------
user_list = recommendation_df["user_id"].unique()
selected_user = st.sidebar.selectbox("Select User", user_list)

# ---------------------------------------------------
# Integrated Data Section
# ---------------------------------------------------
if section == "Integrated Data":
    st.header("Integrated User Data")
    st.write("This section shows the unified dataset created from multiple platforms.")

    filtered_integrated_data = integrated_df[integrated_df["user_id"] == selected_user]

    st.subheader(f"Integrated Data for User {selected_user}")
    st.dataframe(filtered_integrated_data)

# ---------------------------------------------------
# User Profile Section
# ---------------------------------------------------
elif section == "User Profile":
    st.header("User Interest Profile")
    st.write("This section shows the selected user's top interest, engagement, and activity summary.")

    user_profile_data = profile_df[profile_df["user_id"] == selected_user]

    st.subheader(f"Profile for User {selected_user}")
    st.dataframe(user_profile_data)

# ---------------------------------------------------
# Recommendations Section
# ---------------------------------------------------
elif section == "Recommendations":
    st.header("Personalized Recommendations")
    st.write("This section shows generated recommendations for the selected user.")

    user_data = recommendation_df[recommendation_df["user_id"] == selected_user]

    st.subheader(f"Recommendations for User {selected_user}")
    st.dataframe(user_data)