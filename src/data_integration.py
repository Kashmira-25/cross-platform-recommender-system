from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Base project directory
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# File paths (UPDATED)
# ---------------------------------------------------
youtube_path = BASE_DIR / "data" / "raw" / "youtube_real_data.csv"
shopping_path = BASE_DIR / "data" / "raw" / "shopping_data.csv"
learning_path = BASE_DIR / "data" / "raw" / "learning_data.csv"

# ---------------------------------------------------
# Load datasets
# ---------------------------------------------------
youtube_df = pd.read_csv(youtube_path)
shopping_df = pd.read_csv(shopping_path)
learning_df = pd.read_csv(learning_path)

print("Datasets loaded successfully.\n")

# ---------------------------------------------------
# Transform YouTube data (REAL DATA READY)
# ---------------------------------------------------
youtube_transformed = pd.DataFrame()

youtube_transformed["user_id"] = youtube_df.get("user_id", 999)
youtube_transformed["platform"] = "YouTube"
youtube_transformed["item_name"] = youtube_df.get("video_title", "Unknown")
youtube_transformed["item_category"] = youtube_df.get("category", "Other")
youtube_transformed["interaction_type"] = "watched"
youtube_transformed["engagement_score"] = youtube_df.get("watch_time", 10)
youtube_transformed["timestamp"] = youtube_df.get("timestamp", "Unknown")

# ---------------------------------------------------
# Transform Shopping data
# ---------------------------------------------------
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

# ---------------------------------------------------
# Transform Learning data
# ---------------------------------------------------
learning_transformed = pd.DataFrame()

learning_transformed["user_id"] = learning_df["user_id"]
learning_transformed["platform"] = "Learning"
learning_transformed["item_name"] = learning_df["course_name"]
learning_transformed["item_category"] = learning_df["domain"]

learning_transformed["interaction_type"] = learning_df["completion_status"].apply(
    lambda x: "completed" if str(x).lower() == "completed" else "in_progress"
)

learning_transformed["engagement_score"] = learning_df.apply(
    lambda row: row["time_spent"] + 20 if str(row["completion_status"]).lower() == "completed"
    else row["time_spent"],
    axis=1
)

learning_transformed["timestamp"] = learning_df["timestamp"]

# ---------------------------------------------------
# Merge all transformed datasets
# ---------------------------------------------------
integrated_df = pd.concat(
    [youtube_transformed, shopping_transformed, learning_transformed],
    ignore_index=True
)

# ---------------------------------------------------
# Clean data (IMPORTANT)
# ---------------------------------------------------
integrated_df = integrated_df.dropna(subset=["item_name"])
integrated_df["item_category"] = integrated_df["item_category"].fillna("Other")

# ---------------------------------------------------
# Save integrated dataset
# ---------------------------------------------------
processed_dir = BASE_DIR / "data" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

output_path = processed_dir / "integrated_user_data.csv"
integrated_df.to_csv(output_path, index=False)

# ---------------------------------------------------
# Output preview
# ---------------------------------------------------
print("Integrated Dataset Preview:\n")
print(integrated_df.head(10))

print(f"\nTotal records: {len(integrated_df)}")
print(f"Saved at: {output_path}")