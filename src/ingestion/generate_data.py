import pandas as pd
import numpy as np
from datetime import datetime
import random

payments =[]
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

payments.to_csv("data/raw/payments.csv", index=False)
users.to_csv("data/raw/users.csv", index=False)
artists.to_csv("data/raw/artists.csv", index=False)
tracks.to_csv("data/raw/tracks.csv", index=False)
listening_events.to_csv("data/raw/listening_events.csv", index=False)
subscriptions.to_csv("data/raw/subscriptions.csv", index=False)
payments.to_csv("data/raw/payments.csv", index=False)


print("All Spotify + payments data generated!")