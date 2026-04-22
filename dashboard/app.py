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
explained_recommendations_path = BASE_DIR / "data" / "processed" / "explained_recommendations.csv"

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(page_title="Cross-Platform Recommender System", layout="wide")

st.title("Cross-Platform Recommender System")
st.write("A system that integrates multi-platform user activity and generates personalized recommendations with explanation.")

# ---------------------------------------------------
# Load datasets
# ---------------------------------------------------
integrated_df = pd.read_csv(integrated_data_path)
profile_df = pd.read_csv(user_profile_path)
recommendation_df = pd.read_csv(recommendations_path)
explained_df = pd.read_csv(explained_recommendations_path)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["User Dashboard", "Integrated Data", "User Profile", "Recommendations"]
)

user_list = sorted(profile_df["user_id"].unique())
selected_user = st.sidebar.selectbox("Select User", user_list)

# ---------------------------------------------------
# Filter selected user data
# ---------------------------------------------------
user_integrated = integrated_df[integrated_df["user_id"] == selected_user]
user_profile = profile_df[profile_df["user_id"] == selected_user]
user_recommendation = recommendation_df[recommendation_df["user_id"] == selected_user]
user_explained = explained_df[explained_df["user_id"] == selected_user]

# ---------------------------------------------------
# User Dashboard Section
# ---------------------------------------------------
if section == "User Dashboard":
    st.header(f"User Dashboard - User {selected_user}")

    if not user_profile.empty:
        profile_row = user_profile.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Top Interest", profile_row["top_interest_category"])
        col2.metric("Interest Score", profile_row["top_interest_score"])
        col3.metric("Total Interactions", profile_row["total_interactions"])
        col4.metric("Total Engagement", profile_row["total_engagement_score"])

    st.subheader("Recommendations")
    if not user_recommendation.empty:
        rec_row = user_recommendation.iloc[0]

        st.write(f"**1.** {rec_row['recommendation_1']}")
        st.write(f"**2.** {rec_row['recommendation_2']}")
        st.write(f"**3.** {rec_row['recommendation_3']}")
    else:
        st.warning("No recommendations available for this user.")

    st.subheader("Why these recommendations?")
    if not user_explained.empty:
        explained_row = user_explained.iloc[0]
        st.info(explained_row["recommendation_reason"])
    else:
        st.warning("No explanation available for this user.")

    st.subheader("Recent Integrated Activity")
    st.dataframe(user_integrated)

# ---------------------------------------------------
# Integrated Data Section
# ---------------------------------------------------
elif section == "Integrated Data":
    st.header("Integrated User Data")
    st.write("This section shows the selected user's combined activity across platforms.")
    st.dataframe(user_integrated)

# ---------------------------------------------------
# User Profile Section
# ---------------------------------------------------
elif section == "User Profile":
    st.header("User Interest Profile")
    st.write("This section shows the selected user's interest profile.")
    st.dataframe(user_profile)

# ---------------------------------------------------
# Recommendations Section
# ---------------------------------------------------
elif section == "Recommendations":
    st.header("Recommendations and Explanation")

    st.subheader("Recommendation Data")
    st.dataframe(user_recommendation)

    st.subheader("Explanation")
    st.dataframe(user_explained)