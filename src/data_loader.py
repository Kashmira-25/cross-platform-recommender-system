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