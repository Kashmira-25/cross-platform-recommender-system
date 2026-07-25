# ---------------------------------------------------
# FIX IMPORT PATH
# ---------------------------------------------------
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from login import login_page

from src.pipeline import run_pipeline


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Cross-Platform Recommender System",
    page_icon="🚀",
    layout="wide"
)


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False


# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
if not st.session_state.logged_in:

    login_page()

    st.stop()


# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>

.metric-card{
    background-color:#F8F9FA;
    padding:15px;
    border-radius:12px;
    border:1px solid #E6E6E6;
}

.recommend-card{
    background-color:#F4F6FF;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}

.footer{
    text-align:center;
    color:gray;
}

</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🚀 Cross-Platform Recommender System")

st.write(
"""
Analyze user behaviour across multiple platforms and generate
personalized recommendations.
"""
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📊 Dashboard")


mode = st.sidebar.radio(
    "Select Mode",
    [
        "Demo Mode",
        "Upload Your Data (Coming Soon)"
    ]
)



# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
if mode == "Demo Mode":

    if st.sidebar.button("Load Demo Data"):

        with st.spinner("Running recommendation pipeline..."):

            (
                integrated_df,
                profile_df,
                recommendation_df,
                explained_df
            ) = run_pipeline()


            st.session_state.integrated_df = integrated_df
            st.session_state.profile_df = profile_df
            st.session_state.recommendation_df = recommendation_df
            st.session_state.explained_df = explained_df

            st.session_state.data_loaded = True


        st.sidebar.success("Data Loaded Successfully")



if not st.session_state.data_loaded:

    st.info(
"""
Click **Load Demo Data** from sidebar to start.
"""
)

    st.stop()



# ---------------------------------------------------
# GET DATA
# ---------------------------------------------------

integrated_df = st.session_state.integrated_df
profile_df = st.session_state.profile_df
recommendation_df = st.session_state.recommendation_df
explained_df = st.session_state.explained_df



# DEBUG
with st.expander("Debug Columns"):

    st.write("Profile columns:")
    st.write(profile_df.columns)

    st.write("Recommendation columns:")
    st.write(recommendation_df.columns)



# ---------------------------------------------------
# USER SELECTION
# ---------------------------------------------------

st.sidebar.subheader("👤 Select User")


user_list = sorted(
    profile_df["user_id"].unique()
)


selected_user = st.sidebar.selectbox(
    "User ID",
    user_list
)



# ---------------------------------------------------
# FILTER USER
# ---------------------------------------------------

user_profile = profile_df[
    profile_df["user_id"] == selected_user
]


user_recommendation = recommendation_df[
    recommendation_df["user_id"] == selected_user
]


user_explained = explained_df[
    explained_df["user_id"] == selected_user
]


user_data = integrated_df[
    integrated_df["user_id"] == selected_user
]



# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

st.header(
    f"📊 User Dashboard - User {selected_user}"
)



if not user_profile.empty:


    row = user_profile.iloc[0]


    col1,col2,col3,col4 = st.columns(4)


    with col1:

        st.markdown(
        """
        <div class="metric-card">
        🎯 Top Interest
        </div>
        """,
        unsafe_allow_html=True
        )


        top_interest = row.get(
            "top_interest_category",
            "Not Available"
        )


        st.metric(
            "",
            top_interest
        )


    with col2:

        st.markdown(
        """
        <div class="metric-card">
        ⭐ Interest Score
        </div>
        """,
        unsafe_allow_html=True
        )


        st.metric(
            "",
            row.get(
                "top_interest_score",
                0
            )
        )



    with col3:

        st.metric(
            "📈 Total Interactions",
            row.get(
                "total_interactions",
                0
            )
        )



    with col4:

        st.metric(
            "🔥 Engagement",
            row.get(
                "total_engagement_score",
                0
            )
        )



st.divider()



# ---------------------------------------------------
# PLATFORM INTEREST
# ---------------------------------------------------

st.subheader("Platform-wise Interests")


platform_interest = (
    user_data
    .groupby(
        ["platform","item_category"]
    )["engagement_score"]
    .sum()
    .reset_index()
)



platform_interest = (
    platform_interest
    .sort_values(
        "engagement_score",
        ascending=False
    )
    .drop_duplicates(
        subset="platform"
    )
)



for _,r in platform_interest.iterrows():

    st.info(
f"""
### {r['platform']}

Top Interest: {r['item_category']}

Engagement: {r['engagement_score']}
"""
)



# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------

st.subheader(
"🎯 Personalized Recommendations"
)



if not user_recommendation.empty:


    rec = user_recommendation.iloc[0]


    for i in range(1,4):

        col = f"recommendation_{i}"

        if col in rec:

            st.markdown(
f"""
<div class="recommend-card">

### Recommendation {i}

{rec[col]}

</div>
""",
unsafe_allow_html=True
)



# ---------------------------------------------------
# EXPLANATION
# ---------------------------------------------------

st.subheader(
"💡 Why these recommendations?"
)


if not user_explained.empty:

    exp = user_explained.iloc[0]

    if "recommendation_reason" in exp:

        st.info(
            exp["recommendation_reason"]
        )



# ---------------------------------------------------
# ACTIVITY
# ---------------------------------------------------

st.subheader(
"📋 Complete User Activity"
)


st.dataframe(
    user_data,
    use_container_width=True,
    hide_index=True
)



# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

chart1,chart2 = st.columns(2)


with chart1:

    st.subheader(
    "🥧 Interest Distribution"
    )

    counts = user_data["item_category"].value_counts()


    fig,ax = plt.subplots()

    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)



with chart2:

    st.subheader(
    "📊 Platform Usage"
    )


    counts = user_data["platform"].value_counts()


    fig,ax = plt.subplots()

    counts.plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)



# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
"""
<hr>

<center>

🚀 Cross Platform Recommender System

<br>

Python • Pandas • Streamlit • Matplotlib

</center>

""",
unsafe_allow_html=True
)