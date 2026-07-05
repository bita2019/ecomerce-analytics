"""
generate_data.py
----------------
Spotify Analytics Pipeline — Synthetic Data Generation

Generates realistic, interconnected CSV data across 6 tables:
  - users.csv           → platform users across multiple countries
  - artists.csv         → music artists with genres
  - tracks.csv          → songs linked to artists
  - subscriptions.csv   → user subscription plans with correct pricing
  - payments.csv        → payment transactions with realistic amounts
  - listening_events.csv → user listening activity linked to tracks

All foreign keys are consistent across tables.
Output: data/raw/
"""

import random
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
random.seed(42)  # reproducible data

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Volume
N_USERS          = 1000
N_ARTISTS        = 100
N_TRACKS         = 500
N_LISTENING      = 10000
START_DATE       = datetime(2024, 1, 1)
END_DATE         = datetime(2026, 6, 30)

# Subscription plans — realistic Spotify-style pricing
SUBSCRIPTION_PLANS = {
    "free":       0.00,
    "individual": 11.99,
    "duo":        16.99,
    "family":     19.99,
    "student":     5.99,
}
PLAN_WEIGHTS = [0.35, 0.40, 0.10, 0.10, 0.05]  # free most common

PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay"]
PAYMENT_STATUSES = ["success", "success", "success", "failed", "refunded"]  # weighted

COUNTRIES = ["UK", "US", "DE", "FR", "CA", "AU", "NL", "SE", "NO", "DK"]
COUNTRY_WEIGHTS = [0.30, 0.25, 0.10, 0.10, 0.08, 0.05, 0.04, 0.03, 0.03, 0.02]

GENRES = ["Pop", "Hip-Hop", "Electronic", "Rock", "R&B", "Jazz", "Classical",
          "Country", "Latin", "Indie"]

# Real-sounding artist name components
FIRST_NAMES = ["Alex", "Maya", "Jordan", "Sam", "Taylor", "Morgan", "Casey",
               "Riley", "Avery", "Quinn", "Blake", "Drew", "Skylar", "Reese",
               "Kendall", "Aria", "Luna", "Nova", "Zara", "Leo"]
LAST_NAMES  = ["Rivers", "Stone", "Fox", "Banks", "Cross", "Lake", "Hart",
               "West", "Chase", "Knight", "Storm", "Ray", "Cole", "Gray",
               "Flynn", "Reid", "Blake", "Monroe", "Wells", "Hayes"]
BAND_SUFFIXES = ["& The Band", "Project", "Collective", "Ensemble", "Trio",
                 "Orchestra", "Sound", "Experience"]

# Real-sounding track title components
TRACK_ADJECTIVES = ["Midnight", "Golden", "Neon", "Electric", "Broken",
                    "Silent", "Wild", "Falling", "Rising", "Lost", "Dark",
                    "Bright", "Cold", "Burning", "Empty", "Endless"]
TRACK_NOUNS      = ["Dreams", "Lights", "Fire", "Rain", "Heart", "Roads",
                    "Skies", "Waves", "Storm", "Shadow", "Signal", "Echo",
                    "Pulse", "Drift", "Spark", "Shore"]


# ── Helper functions ──────────────────────────────────────────────────────────
def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def random_artist_name() -> str:
    if random.random() < 0.3:
        # Band name
        name = f"{random.choice(LAST_NAMES)} {random.choice(BAND_SUFFIXES)}"
    else:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    return name


def random_track_title(used: set) -> str:
    for _ in range(20):
        title = f"{random.choice(TRACK_ADJECTIVES)} {random.choice(TRACK_NOUNS)}"
        if title not in used:
            used.add(title)
            return title
    # Fallback with number if all combinations exhausted
    return f"{random.choice(TRACK_ADJECTIVES)} {random.choice(TRACK_NOUNS)} {random.randint(2, 99)}"


def random_email(name: str, user_id: int) -> str:
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"]
    clean = name.lower().replace(" ", ".")
    return f"{clean}{user_id}@{random.choice(domains)}"


def write_csv(filepath: Path, rows: list[dict], fieldnames: list[str]):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info(f"✓ Written {len(rows):,} rows → {filepath}")


# ── Generators ────────────────────────────────────────────────────────────────
def generate_users() -> list[dict]:
    log.info("Generating users...")
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sofia",
                   "Mason", "Isabella", "William", "Mia", "James", "Charlotte",
                   "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn",
                   "Alexander"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Wilson", "Taylor", "Anderson", "Thomas",
                  "Jackson", "White", "Harris", "Martin", "Thompson", "Moore",
                  "Young", "Lee"]
    users = []
    for i in range(1, N_USERS + 1):
        first = random.choice(first_names)
        last  = random.choice(last_names)
        name  = f"{first} {last}"
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS)[0]
        reg_date = random_date(START_DATE, END_DATE)
        users.append({
            "user_id":           i,
            "name":              name,
            "email":             random_email(name, i),
            "country":           country,
            "registration_date": reg_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return users


def generate_artists() -> list[dict]:
    log.info("Generating artists...")
    used_names = set()
    artists = []
    for i in range(1, N_ARTISTS + 1):
        name = random_artist_name()
        while name in used_names:
            name = random_artist_name()
        used_names.add(name)
        genre   = random.choice(GENRES)
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS)[0]
        artists.append({
            "artist_id": i,
            "name":      name,
            "genre":     genre,
            "country":   country,
        })
    return artists


def generate_tracks(artists: list[dict]) -> list[dict]:
    log.info("Generating tracks...")
    used_titles = set()
    tracks = []
    for i in range(1, N_TRACKS + 1):
        artist  = random.choice(artists)
        title   = random_track_title(used_titles)
        # Duration between 2 mins (120k ms) and 5 mins (300k ms)
        duration = random.randint(120_000, 300_000)
        tracks.append({
            "track_id":   i,
            "title":      title,
            "artist_id":  artist["artist_id"],
            "duration_ms": duration,
            "genre":      artist["genre"],  # inherit artist genre
        })
    return tracks


def generate_subscriptions(users: list[dict]) -> list[dict]:
    log.info("Generating subscriptions...")
    subscriptions = []
    for user in users:
        reg_date = datetime.strptime(user["registration_date"], "%Y-%m-%d %H:%M:%S")
        plan     = random.choices(list(SUBSCRIPTION_PLANS.keys()), weights=PLAN_WEIGHTS)[0]
        price    = SUBSCRIPTION_PLANS[plan]
        # Subscription starts on or after registration
        start    = random_date(reg_date, END_DATE)
        # Some subscriptions have ended (churned users)
        is_active = random.random() > 0.2
        end_date  = None if is_active else random_date(start, END_DATE)
        subscriptions.append({
            "user_id":           user["user_id"],
            "subscription_type": plan,
            "monthly_price":     round(price, 2),
            "start_date":        start.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date":          end_date.strftime("%Y-%m-%d %H:%M:%S") if end_date else None,
            "is_active":         is_active,
        })
    return subscriptions


def generate_payments(subscriptions: list[dict]) -> list[dict]:
    log.info("Generating payments...")
    payments = []
    payment_id = 1
    for sub in subscriptions:
        # Free users have no payments
        if sub["monthly_price"] == 0.0:
            continue
        start = datetime.strptime(sub["start_date"], "%Y-%m-%d %H:%M:%S")
        end   = (
            datetime.strptime(sub["end_date"], "%Y-%m-%d %H:%M:%S")
            if sub["end_date"] else END_DATE
        )
        # Generate one payment per month for the subscription period
        current = start
        while current < end:
            method  = random.choice(PAYMENT_METHODS)
            status  = random.choices(PAYMENT_STATUSES)[0]
            # Failed payments have 0 amount, refunds return the amount
            amount  = sub["monthly_price"] if status == "success" else 0.0
            if status == "refunded":
                amount = sub["monthly_price"]
            payments.append({
                "payment_id":     payment_id,
                "user_id":        sub["user_id"],
                "payment_date":   current.strftime("%Y-%m-%d %H:%M:%S"),
                "amount":         round(amount, 2),
                "payment_method": method,
                "status":         status,
            })
            payment_id += 1
            # Advance by ~1 month
            current = current + timedelta(days=30)
    return payments


def generate_listening_events(users: list[dict], tracks: list[dict]) -> list[dict]:
    log.info("Generating listening events...")
    events = []
    for i in range(1, N_LISTENING + 1):
        user  = random.choice(users)
        track = random.choice(tracks)
        ts    = random_date(START_DATE, END_DATE)
        # Play duration: between 30 seconds and full track duration
        play_duration = random.randint(30_000, track["duration_ms"])
        events.append({
            "event_id":        i,
            "user_id":         user["user_id"],
            "track_id":        track["track_id"],
            "timestamp":       ts.strftime("%Y-%m-%d %H:%M:%S"),
            "play_duration_ms": play_duration,
        })
    # Sort by timestamp for realism
    events.sort(key=lambda x: x["timestamp"])
    return events


# ── Main ──────────────────────────────────────────────────────────────────────
def run():
    log.info("=" * 55)
    log.info("Spotify Analytics Pipeline — Data Generation")
    log.info("=" * 55)

    users         = generate_users()
    artists       = generate_artists()
    tracks        = generate_tracks(artists)
    subscriptions = generate_subscriptions(users)
    payments      = generate_payments(subscriptions)
    listening     = generate_listening_events(users, tracks)

    write_csv(OUTPUT_DIR / "users.csv",            users,
              ["user_id", "name", "email", "country", "registration_date"])

    write_csv(OUTPUT_DIR / "artists.csv",          artists,
              ["artist_id", "name", "genre", "country"])

    write_csv(OUTPUT_DIR / "tracks.csv",           tracks,
              ["track_id", "title", "artist_id", "duration_ms", "genre"])

    write_csv(OUTPUT_DIR / "subscriptions.csv",    subscriptions,
              ["user_id", "subscription_type", "monthly_price",
               "start_date", "end_date", "is_active"])

    write_csv(OUTPUT_DIR / "payments.csv",         payments,
              ["payment_id", "user_id", "payment_date",
               "amount", "payment_method", "status"])

    write_csv(OUTPUT_DIR / "listening_events.csv", listening,
              ["event_id", "user_id", "track_id",
               "timestamp", "play_duration_ms"])

    log.info("=" * 55)
    log.info("✓ All files written to data/raw/")
    log.info(f"  Users:            {len(users):,}")
    log.info(f"  Artists:          {len(artists):,}")
    log.info(f"  Tracks:           {len(tracks):,}")
    log.info(f"  Subscriptions:    {len(subscriptions):,}")
    log.info(f"  Payments:         {len(payments):,}")
    log.info(f"  Listening events: {len(listening):,}")
    log.info("=" * 55)
    log.info("Next step: run src/bronze_to_silver.py")


if __name__ == "__main__":
    run()

