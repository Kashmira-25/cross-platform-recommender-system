import streamlit as st
import pandas as pd
from src.pipeline import integrate_data, build_user_profile, generate_recommendations, generate_explanations

st.set_page_config(page_title="Cross-Platform Recommender System", layout="wide")

st.title("Cross-Platform Recommender System")
st.write("Analyze user behavior and generate personalized recommendations.")

# ---------------------------------------------------
# Mode Selection
# ---------------------------------------------------
mode = st.sidebar.radio("Select Mode", ["Demo Mode", "Upload Your Data"])

# ---------------------------------------------------
# DEMO MODE
# ---------------------------------------------------
if mode == "Demo Mode":
    from src.pipeline import run_pipeline

    st.sidebar.success("Using demo dataset")

    integrated_df, profile_df, recommendation_df, explained_df = run_pipeline()

# ---------------------------------------------------
# UPLOAD MODE
# ---------------------------------------------------
else:
    st.sidebar.info("Upload your CSV files")

    youtube_file = st.sidebar.file_uploader("Upload YouTube Data", type=["csv"])
    shopping_file = st.sidebar.file_uploader("Upload Shopping Data", type=["csv"])
    learning_file = st.sidebar.file_uploader("Upload Learning Data", type=["csv"])

    if youtube_file and shopping_file and learning_file:
        youtube_df = pd.read_csv(youtube_file)
        shopping_df = pd.read_csv(shopping_file)
        learning_df = pd.read_csv(learning_file)

        integrated_df = integrate_data(youtube_df, shopping_df, learning_df)
        profile_df = build_user_profile(integrated_df)
        recommendation_df = generate_recommendations(profile_df)
        explained_df = generate_explanations(integrated_df, recommendation_df)

        st.success("Data processed successfully!")
    else:
        st.warning("Please upload all three datasets.")
        st.stop()

# ---------------------------------------------------
# USER SELECTION
# ---------------------------------------------------
user_list = sorted(profile_df["user_id"].unique())
selected_user = st.sidebar.selectbox("Select User", user_list)

user_profile = profile_df[profile_df["user_id"] == selected_user]
user_recommendation = recommendation_df[recommendation_df["user_id"] == selected_user]
user_explained = explained_df[explained_df["user_id"] == selected_user]
user_data = integrated_df[integrated_df["user_id"] == selected_user]

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
st.header(f"User Dashboard - User {selected_user}")

if not user_profile.empty:
    row = user_profile.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Top Interest", row["top_interest_category"])
    col2.metric("Interest Score", row["top_interest_score"])
    col3.metric("Total Interactions", row["total_interactions"])
    col4.metric("Total Engagement", row["total_engagement_score"])

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------
st.subheader("Recommendations")

if not user_recommendation.empty:
    rec = user_recommendation.iloc[0]

    st.write(f"**1.** {rec['recommendation_1']}")
    st.write(f"**2.** {rec['recommendation_2']}")
    st.write(f"**3.** {rec['recommendation_3']}")

# ---------------------------------------------------
# EXPLANATION
# ---------------------------------------------------
st.subheader("Why these recommendations?")

if not user_explained.empty:
    exp = user_explained.iloc[0]
    st.info(exp["recommendation_reason"])

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------
st.subheader("User Activity Data")
st.dataframe(user_data)