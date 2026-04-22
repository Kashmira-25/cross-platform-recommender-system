from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re

# ---------------------------------------------------
# Step 1: Base directory
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# Step 2: File paths
# ---------------------------------------------------
html_path = BASE_DIR / "data" / "raw" / "youtube_real" / "watch-history.html"
output_path = BASE_DIR / "data" / "raw" / "youtube_real_data.csv"

# ---------------------------------------------------
# Step 3: Helper function to assign category
# ---------------------------------------------------
def assign_category(title: str) -> str:
    title = str(title).lower()

    if any(keyword in title for keyword in [
        "python", "coding", "programming", "developer", "software", "tech",
        "javascript", "java", "web development", "laptop", "computer"
    ]):
        return "Technology"

    elif any(keyword in title for keyword in [
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "neural network", "data science", "ml"
    ]):
        return "AI"

    elif any(keyword in title for keyword in [
        "workout", "gym", "fitness", "exercise", "yoga", "diet", "protein",
        "health", "running"
    ]):
        return "Fitness"

    elif any(keyword in title for keyword in [
        "fashion", "makeup", "beauty", "styling", "outfit", "skincare",
        "lipstick", "dress"
    ]):
        return "Fashion"

    elif any(keyword in title for keyword in [
        "study", "education", "tutorial", "course", "lecture", "exam",
        "learning", "student"
    ]):
        return "Education"

    elif any(keyword in title for keyword in [
        "music", "song", "album", "concert", "playlist", "singer"
    ]):
        return "Music"

    elif any(keyword in title for keyword in [
        "movie", "trailer", "series", "film", "comedy", "entertainment",
        "show", "episode", "funny"
    ]):
        return "Entertainment"

    else:
        return "Other"

# ---------------------------------------------------
# Step 4: Helper function to estimate watch time
# ---------------------------------------------------
def estimate_watch_time(title: str) -> int:
    title = str(title).lower()

    if any(word in title for word in ["podcast", "lecture", "course"]):
        return 25
    elif any(word in title for word in ["tutorial", "explained", "guide"]):
        return 20
    else:
        return 10

# ---------------------------------------------------
# Step 5: Validate file
# ---------------------------------------------------
if not html_path.exists():
    raise FileNotFoundError(f"File not found: {html_path}")

print(f"Reading file: {html_path}")

# ---------------------------------------------------
# Step 6: Read HTML file
# ---------------------------------------------------
with open(html_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

print("HTML file loaded successfully.")

# ---------------------------------------------------
# Step 7: Extract relevant watch history entries
# ---------------------------------------------------
entries = soup.find_all(
    "div",
    class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"
)

print(f"Relevant entries found: {len(entries)}")

# ---------------------------------------------------
# Step 8: Limit entries for quick testing
# Change TEST_MODE to False for full extraction
# ---------------------------------------------------
TEST_MODE = True
TEST_LIMIT = 500

if TEST_MODE:
    entries = entries[:TEST_LIMIT]
    print(f"TEST MODE ON: Processing first {len(entries)} entries only.")
else:
    print("FULL MODE ON: Processing all entries.")

# ---------------------------------------------------
# Step 9: Parse entries
# ---------------------------------------------------
data = []

for i, entry in enumerate(entries):
    if i % 50 == 0:
        print(f"Processing entry {i}...")

    try:
        links = entry.find_all("a")
        full_text = entry.get_text(" ", strip=True)

        if not links:
            continue

        # First link is usually video title
        video_title = links[0].get_text(strip=True)

        if not video_title:
            continue

        # Second link is usually channel name
        channel_name = links[1].get_text(strip=True) if len(links) > 1 else "Unknown"

        # Try extracting timestamp from text
        timestamp_match = re.search(
            r'([A-Z][a-z]{2,8}\s+\d{1,2},\s+\d{4}.*)$',
            full_text
        )
        timestamp = timestamp_match.group(1).strip() if timestamp_match else "Unknown"

        data.append({
            "user_id": 999,
            "video_title": video_title,
            "channel_name": channel_name,
            "category": assign_category(video_title),
            "watch_time": estimate_watch_time(video_title),
            "liked": "Unknown",
            "timestamp": timestamp
        })

    except Exception:
        continue

# ---------------------------------------------------
# Step 10: Convert to DataFrame
# ---------------------------------------------------
df = pd.DataFrame(data)

# Remove duplicates
df = df.drop_duplicates()

# ---------------------------------------------------
# Step 11: Validate output
# ---------------------------------------------------
if df.empty:
    print("No watch history entries were extracted.")
else:
    print(f"\nExtracted {len(df)} records successfully.\n")
    print(df.head())

# ---------------------------------------------------
# Step 12: Save CSV
# ---------------------------------------------------
df.to_csv(output_path, index=False)

print(f"\nYouTube real data saved at: {output_path}")