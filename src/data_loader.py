import pandas as pd

# Load datasets
youtube_df = pd.read_csv("data/raw/youtube_history.csv")
shopping_df = pd.read_csv("data/raw/shopping_data.csv")
learning_df = pd.read_csv("data/raw/learning_data.csv")

# Print preview
print("YouTube Data:")
print(youtube_df.head())

print("\nShopping Data:")
print(shopping_df.head())

print("\nLearning Data:")
print(learning_df.head())

import os

# Create processed folder if not exists
os.makedirs("data/processed", exist_ok=True)

# Save combined preview (temporary)
youtube_df.to_csv("data/processed/youtube_preview.csv", index=False)