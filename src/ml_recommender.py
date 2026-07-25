import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def generate_ml_recommendations(profile_df, integrated_df):

    recommendation_records = []

    # ----------------------------------------------------
    # Create one content library from all demo data
    # ----------------------------------------------------
    content_library = integrated_df[
        ["item_name", "item_category", "platform"]
    ].drop_duplicates().reset_index(drop=True)

    # Combine text features
    content_library["content"] = (
        content_library["item_name"].astype(str)
        + " "
        + content_library["item_category"].astype(str)
        + " "
        + content_library["platform"].astype(str)
    )

    # Convert text into vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    content_vectors = vectorizer.fit_transform(
        content_library["content"]
    )

    # ----------------------------------------------------
    # Process each user
    # ----------------------------------------------------
    for _, profile in profile_df.iterrows():

        user_id = profile["user_id"]

        user_history = integrated_df[
            integrated_df["user_id"] == user_id
        ]

        if user_history.empty:
            continue

        # Build user profile text
        user_profile_text = " ".join(
            (
                user_history["item_name"].astype(str)
                + " "
                + user_history["item_category"].astype(str)
            ).tolist()
        )

        # Convert user profile into vector
        user_vector = vectorizer.transform(
            [user_profile_text]
        )

        # Similarity with every item
        similarity = cosine_similarity(
            user_vector,
            content_vectors
        ).flatten()

        content_library["similarity"] = similarity

        # Remove already interacted items
        interacted = user_history["item_name"].tolist()

        recommendations = content_library[
            ~content_library["item_name"].isin(interacted)
        ]

        recommendations = recommendations.sort_values(
            "similarity",
            ascending=False
        )

        top = recommendations.head(3)

        recommendation_list = top["item_name"].tolist()

        while len(recommendation_list) < 3:
            recommendation_list.append("No Recommendation")

        confidence = round(
            top["similarity"].mean() * 100,
            2
        )

        recommendation_records.append({

            "user_id": user_id,

            "recommendation_1": recommendation_list[0],

            "recommendation_2": recommendation_list[1],

            "recommendation_3": recommendation_list[2],

            "confidence": confidence

        })

    return pd.DataFrame(recommendation_records)
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def generate_ml_recommendations(profile_df, integrated_df):

    recommendation_records = []

    # ----------------------------------------------------
    # Create one content library from all demo data
    # ----------------------------------------------------
    content_library = integrated_df[
        ["item_name", "item_category", "platform"]
    ].drop_duplicates().reset_index(drop=True)

    # Combine text features
    content_library["content"] = (
        content_library["item_name"].astype(str)
        + " "
        + content_library["item_category"].astype(str)
        + " "
        + content_library["platform"].astype(str)
    )

    # Convert text into vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    content_vectors = vectorizer.fit_transform(
        content_library["content"]
    )

    # ----------------------------------------------------
    # Process each user
    # ----------------------------------------------------
    for _, profile in profile_df.iterrows():

        user_id = profile["user_id"]

        user_history = integrated_df[
            integrated_df["user_id"] == user_id
        ]

        if user_history.empty:
            continue

        # Build user profile text
        user_profile_text = " ".join(
            (
                user_history["item_name"].astype(str)
                + " "
                + user_history["item_category"].astype(str)
            ).tolist()
        )

        # Convert user profile into vector
        user_vector = vectorizer.transform(
            [user_profile_text]
        )

        # Similarity with every item
        similarity = cosine_similarity(
            user_vector,
            content_vectors
        ).flatten()

        content_library["similarity"] = similarity

        # Remove already interacted items
        interacted = user_history["item_name"].tolist()

        recommendations = content_library[
            ~content_library["item_name"].isin(interacted)
        ]

        recommendations = recommendations.sort_values(
            "similarity",
            ascending=False
        )

        top = recommendations.head(3)

        recommendation_list = top["item_name"].tolist()

        while len(recommendation_list) < 3:
            recommendation_list.append("No Recommendation")

        confidence = round(
            top["similarity"].mean() * 100,
            2
        )

        recommendation_records.append({

            "user_id": user_id,

            "recommendation_1": recommendation_list[0],

            "recommendation_2": recommendation_list[1],

            "recommendation_3": recommendation_list[2],

            "confidence": confidence

        })

    return pd.DataFrame(recommendation_records)