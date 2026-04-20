from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "processed" / "integrated_user_data.csv"
output_path = BASE_DIR / "data" / "processed" / "user_interest_profile.csv"

df = pd.read_csv(input_path)

category_profile = (
    df.groupby(["user_id", "item_category"])["engagement_score"]
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
    df.groupby("user_id")["platform"]
    .nunique()
    .reset_index()
    .rename(columns={"platform": "platform_count"})
)

interaction_count = (
    df.groupby("user_id")
    .size()
    .reset_index(name="total_interactions")
)

total_engagement = (
    df.groupby("user_id")["engagement_score"]
    .sum()
    .reset_index()
    .rename(columns={"engagement_score": "total_engagement_score"})
)

user_profile = top_interest.merge(platform_count, on="user_id")
user_profile = user_profile.merge(interaction_count, on="user_id")
user_profile = user_profile.merge(total_engagement, on="user_id")

user_profile.to_csv(output_path, index=False)

print("User interest profile created successfully.\n")
print(user_profile)
print(f"\nSaved at: {output_path}")