from pathlib import Path
import pandas as pd


# ---------------------------------------------------
# Base directory
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------
# Load raw datasets
# ---------------------------------------------------
def load_raw_data():
    youtube_path = BASE_DIR / "data" / "raw" / "youtube_real_data.csv"
    shopping_path = BASE_DIR / "data" / "raw" / "shopping_data.csv"
    learning_path = BASE_DIR / "data" / "raw" / "learning_data.csv"

    youtube_df = pd.read_csv(youtube_path)
    shopping_df = pd.read_csv(shopping_path)
    learning_df = pd.read_csv(learning_path)

    return youtube_df, shopping_df, learning_df


# ---------------------------------------------------
# Integrate datasets into common schema
# ---------------------------------------------------
def integrate_data(youtube_df, shopping_df, learning_df):
    youtube_transformed = pd.DataFrame()
    youtube_transformed["user_id"] = youtube_df.get("user_id", 999)
    youtube_transformed["platform"] = "YouTube"
    youtube_transformed["item_name"] = youtube_df.get("video_title", "Unknown")
    youtube_transformed["item_category"] = youtube_df.get("category", "Other")
    youtube_transformed["interaction_type"] = "watched"
    youtube_transformed["engagement_score"] = youtube_df.get("watch_time", 10)
    youtube_transformed["timestamp"] = youtube_df.get("timestamp", "Unknown")

    shopping_transformed = pd.DataFrame()
    shopping_transformed["user_id"] = shopping_df["user_id"]
    shopping_transformed["platform"] = "Shopping"
    shopping_transformed["item_name"] = shopping_df["product_name"]
    shopping_transformed["item_category"] = shopping_df["category"]
    shopping_transformed["interaction_type"] = shopping_df["interaction_type"]
    shopping_transformed["engagement_score"] = shopping_df["interaction_type"].apply(
        lambda x: 10 if str(x).lower() == "purchased" else 5
    )
    shopping_transformed["timestamp"] = shopping_df["timestamp"]

    learning_transformed = pd.DataFrame()
    learning_transformed["user_id"] = learning_df["user_id"]
    learning_transformed["platform"] = "Learning"
    learning_transformed["item_name"] = learning_df["course_name"]
    learning_transformed["item_category"] = learning_df["domain"]
    learning_transformed["interaction_type"] = learning_df["completion_status"].apply(
        lambda x: "completed" if str(x).lower() == "completed" else "in_progress"
    )
    learning_transformed["engagement_score"] = learning_df.apply(
        lambda row: row["time_spent"] + 20
        if str(row["completion_status"]).lower() == "completed"
        else row["time_spent"],
        axis=1
    )
    learning_transformed["timestamp"] = learning_df["timestamp"]

    integrated_df = pd.concat(
        [youtube_transformed, shopping_transformed, learning_transformed],
        ignore_index=True
    )

    integrated_df = integrated_df.dropna(subset=["item_name"])
    integrated_df["item_category"] = integrated_df["item_category"].fillna("Other")

    return integrated_df


# ---------------------------------------------------
# Build user interest profile
# ---------------------------------------------------
def build_user_profile(integrated_df):
    category_profile = (
        integrated_df.groupby(["user_id", "item_category"])["engagement_score"]
        .sum()
        .reset_index()
        .sort_values(["user_id", "engagement_score"], ascending=[True, False])
    )

    top_interest = (
        category_profile.groupby("user_id")
        .first()
        .reset_index()
        .rename(columns={
            "item_category": "top_interest_category",
            "engagement_score": "top_interest_score"
        })
    )

    platform_count = (
        integrated_df.groupby("user_id")["platform"]
        .nunique()
        .reset_index()
        .rename(columns={"platform": "platform_count"})
    )

    interaction_count = (
        integrated_df.groupby("user_id")
        .size()
        .reset_index(name="total_interactions")
    )

    total_engagement = (
        integrated_df.groupby("user_id")["engagement_score"]
        .sum()
        .reset_index()
        .rename(columns={"engagement_score": "total_engagement_score"})
    )

    user_profile = top_interest.merge(platform_count, on="user_id")
    user_profile = user_profile.merge(interaction_count, on="user_id")
    user_profile = user_profile.merge(total_engagement, on="user_id")

    return user_profile


# ---------------------------------------------------
# Generate recommendations
# ---------------------------------------------------
def generate_recommendations(user_profile_df):
    recommendation_map = {
        "Technology": [
            "AI Tools and Productivity Apps",
            "Laptop Accessories",
            "Advanced Python Course"
        ],
        "Education": [
            "Programming Tutorials",
            "Skill Development Courses",
            "Study Productivity Tools"
        ],
        "Data Science": [
            "Machine Learning Course",
            "Python Projects for Practice",
            "Data Analytics Toolkit"
        ],
        "AI": [
            "Deep Learning Course",
            "AI Research Videos",
            "Prompt Engineering Guide"
        ],
        "Fitness": [
            "Workout App Subscription",
            "Yoga and Training Videos",
            "Protein and Wellness Products"
        ],
        "Fashion": [
            "Fashion Styling Videos",
            "Beauty and Makeup Products",
            "Trend-Based Shopping Suggestions"
        ],
        "Entertainment": [
            "Trending Web Series",
            "Comedy and Fun Content",
            "Popular Movie Recommendations"
        ],
        "Music": [
            "Curated Playlists",
            "Music Learning Content",
            "Concert and Album Suggestions"
        ],
        "Other": [
            "General Productivity Content",
            "Popular Learning Resources",
            "Trending Products"
        ]
    }

    def get_recommendations(category):
        return recommendation_map.get(category, recommendation_map["Other"])

    recommendations_df = user_profile_df.copy()
    recommendations_df["recommendation_1"] = recommendations_df["top_interest_category"].apply(
        lambda x: get_recommendations(x)[0]
    )
    recommendations_df["recommendation_2"] = recommendations_df["top_interest_category"].apply(
        lambda x: get_recommendations(x)[1]
    )
    recommendations_df["recommendation_3"] = recommendations_df["top_interest_category"].apply(
        lambda x: get_recommendations(x)[2]
    )

    return recommendations_df


# ---------------------------------------------------
# Generate recommendation explanations
# ---------------------------------------------------
def generate_explanations(integrated_df, recommendations_df):
    platform_summary = (
        integrated_df.groupby("user_id")["platform"]
        .unique()
        .reset_index()
    )

    platform_summary["platforms_used"] = platform_summary["platform"].apply(
        lambda x: ", ".join(sorted(x))
    )
    platform_summary = platform_summary.drop(columns=["platform"])

    final_df = recommendations_df.merge(
        platform_summary,
        on="user_id",
        how="left"
    )

    final_df["platforms_used"] = final_df["platforms_used"].fillna("Unknown")

    def build_reason(row):
        return (
            f"User {row['user_id']} shows strong interest in "
            f"{row['top_interest_category']} "
            f"(score: {row['top_interest_score']}) "
            f"based on activity across {row['platforms_used']}."
        )

    final_df["recommendation_reason"] = final_df.apply(build_reason, axis=1)

    return final_df


# ---------------------------------------------------
# Save outputs
# ---------------------------------------------------
def save_outputs(integrated_df, user_profile_df, recommendations_df, explained_df):
    processed_dir = BASE_DIR / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    integrated_df.to_csv(processed_dir / "integrated_user_data.csv", index=False)
    user_profile_df.to_csv(processed_dir / "user_interest_profile.csv", index=False)
    recommendations_df.to_csv(processed_dir / "user_recommendations.csv", index=False)
    explained_df.to_csv(processed_dir / "explained_recommendations.csv", index=False)


# ---------------------------------------------------
# Run full pipeline
# ---------------------------------------------------
def run_pipeline():
    youtube_df, shopping_df, learning_df = load_raw_data()
    integrated_df = integrate_data(youtube_df, shopping_df, learning_df)
    user_profile_df = build_user_profile(integrated_df)
    recommendations_df = generate_recommendations(user_profile_df)
    explained_df = generate_explanations(integrated_df, recommendations_df)

    save_outputs(integrated_df, user_profile_df, recommendations_df, explained_df)

    return integrated_df, user_profile_df, recommendations_df, explained_df