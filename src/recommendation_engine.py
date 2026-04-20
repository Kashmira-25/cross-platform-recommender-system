from pathlib import Path
import pandas as pd

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
profile_path = BASE_DIR / "data" / "processed" / "user_interest_profile.csv"
output_path = BASE_DIR / "data" / "processed" / "user_recommendations.csv"

# Load user profile
df = pd.read_csv(profile_path)

# Recommendation mapping
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
    ]
}

# Function to get recommendations
def generate_recommendations(category):
    return recommendation_map.get(
        category,
        ["General Productivity Content", "Popular Learning Resources", "Trending Products"]
    )

# Apply recommendations
df["recommendation_1"] = df["top_interest_category"].apply(lambda x: generate_recommendations(x)[0])
df["recommendation_2"] = df["top_interest_category"].apply(lambda x: generate_recommendations(x)[1])
df["recommendation_3"] = df["top_interest_category"].apply(lambda x: generate_recommendations(x)[2])

# Save recommendations
df.to_csv(output_path, index=False)

print("User recommendations generated successfully.\n")
print(df)
print(f"\nSaved at: {output_path}")