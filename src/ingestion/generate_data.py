import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import random

# Create data directory if it doesn't exist
import os
os.makedirs("data/raw", exist_ok=True)

# Generate users data
num_users = 1000
users = pd.DataFrame({
    "user_id": range(1, num_users + 1),
    "name": [f"User {i}" for i in range(1, num_users + 1)],
    "email": [f"user{i}@example.com" for i in range(1, num_users + 1)],
    "country": np.random.choice(["US", "UK", "CA", "DE", "FR"], num_users),
    "registration_date": [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(num_users)]
})

# Generate artists data
num_artists = 200
artists = pd.DataFrame({
    "artist_id": range(1, num_artists + 1),
    "name": [f"Artist {i}" for i in range(1, num_artists + 1)],
    "genre": np.random.choice(["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic"], num_artists),
    "country": np.random.choice(["US", "UK", "CA", "DE", "FR"], num_artists)
})

# Generate tracks data
num_tracks = 5000
tracks = pd.DataFrame({
    "track_id": range(1, num_tracks + 1),
    "title": [f"Track {i}" for i in range(1, num_tracks + 1)],
    "artist_id": np.random.choice(artists["artist_id"], num_tracks),
    "duration_ms": np.random.randint(180000, 300000, num_tracks),  # 3-5 minutes
    "genre": np.random.choice(["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic"], num_tracks)
})

# Generate subscriptions data
subscriptions = pd.DataFrame({
    "user_id": users["user_id"],
    "subscription_type": np.random.choice(["free", "premium", "family"], num_users, p=[0.5, 0.4, 0.1]),
    "monthly_price": [0 if t == "free" else (9.99 if t == "premium" else 14.99) for t in np.random.choice(["free", "premium", "family"], num_users, p=[0.5, 0.4, 0.1])],
    "start_date": [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(num_users)]
})

# Generate listening events data
num_events = 10000
listening_events = pd.DataFrame({
    "event_id": range(1, num_events + 1),
    "user_id": np.random.choice(users["user_id"], num_events),
    "track_id": np.random.choice(tracks["track_id"], num_events),
    "timestamp": [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(num_events)],
    "play_duration_ms": np.random.randint(10000, 300000, num_events)
})

# Generate payments data
payments = []
payment_id = 1

for _, row in subscriptions.iterrows():
    if row["subscription_type"] != "free":
        for i in range(random.randint(1, 6)):  # simulate multiple payments
            payments.append({
                "payment_id": payment_id,
                "user_id": row["user_id"],
                "payment_date": row["start_date"] + timedelta(days=30*i),
                "amount": row["monthly_price"],
                "payment_method": random.choice(["card", "paypal"]),
                "status": np.random.choice(["success", "failed", "refunded"], p=[0.85, 0.1, 0.05])
            })
            payment_id += 1

payments = pd.DataFrame(payments)

# Save all dataframes to CSV
users.to_csv("data/raw/users.csv", index=False)
artists.to_csv("data/raw/artists.csv", index=False)
tracks.to_csv("data/raw/tracks.csv", index=False)
listening_events.to_csv("data/raw/listening_events.csv", index=False)
subscriptions.to_csv("data/raw/subscriptions.csv", index=False)
payments.to_csv("data/raw/payments.csv", index=False)

print("All Spotify + payments data generated!")