from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Step 1: Base directory
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# Step 2: File paths
# ---------------------------------------------------
integrated_path = BASE_DIR / "data" / "processed" / "integrated_user_data.csv"
profile_path = BASE_DIR / "data" / "processed" / "user_interest_profile.csv"
recommendation_path = BASE_DIR / "data" / "processed" / "user_recommendations.csv"
output_path = BASE_DIR / "data" / "processed" / "explained_recommendations.csv"

# ---------------------------------------------------
# Step 3: Load datasets
# ---------------------------------------------------
integrated_df = pd.read_csv(integrated_path)
profile_df = pd.read_csv(profile_path)
recommendation_df = pd.read_csv(recommendation_path)

print("Files loaded successfully.\n")

# ---------------------------------------------------
# Step 4: Build platform summary
# ---------------------------------------------------
platform_summary = (
    integrated_df.groupby("user_id")["platform"]
    .unique()
    .reset_index()
)

platform_summary["platforms_used"] = platform_summary["platform"].apply(
    lambda x: ", ".join(sorted(x))
)

platform_summary = platform_summary.drop(columns=["platform"])

# ---------------------------------------------------
# Step 5: Remove duplicate columns from recommendation_df
# ---------------------------------------------------
duplicate_cols = ["top_interest_category", "top_interest_score"]
recommendation_df = recommendation_df.drop(
    columns=[col for col in duplicate_cols if col in recommendation_df.columns],
    errors="ignore"
)

# ---------------------------------------------------
# Step 6: Merge recommendation data with profile data
# ---------------------------------------------------
final_df = recommendation_df.merge(
    profile_df[["user_id", "top_interest_category", "top_interest_score"]],
    on="user_id",
    how="left"
)

# ---------------------------------------------------
# Step 7: Merge platform summary
# ---------------------------------------------------
final_df = final_df.merge(
    platform_summary,
    on="user_id",
    how="left"
)

# ---------------------------------------------------
# Step 8: Fill missing values safely
# ---------------------------------------------------
final_df["top_interest_category"] = final_df["top_interest_category"].fillna("Unknown")
final_df["top_interest_score"] = final_df["top_interest_score"].fillna(0)
final_df["platforms_used"] = final_df["platforms_used"].fillna("Unknown")

# ---------------------------------------------------
# Step 9: Generate explanation text
# ---------------------------------------------------
def generate_explanation(row):
    return (
        f"User {row['user_id']} shows strong interest in "
        f"{row['top_interest_category']} "
        f"(score: {row['top_interest_score']}) "
        f"based on activity across {row['platforms_used']}."
    )

final_df["recommendation_reason"] = final_df.apply(generate_explanation, axis=1)

# ---------------------------------------------------
# Step 10: Save output
# ---------------------------------------------------
final_df.to_csv(output_path, index=False)

print("Explained recommendations created successfully.\n")
print(final_df)

print(f"\nSaved at: {output_path}")