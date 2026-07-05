import pandas as pd

tables = {
    "artists":          "artist_id",
    "users":            "user_id",
    "tracks":           "track_id",
    "payments":         "payment_id",
    "subscriptions":    "user_id",
    "listening_events": "event_id",
}
for table_name,column_name in tables.items():
    
    df = pd.read_csv(f"data/raw/{table_name}.csv")
    null_count = df[column_name].isnull().sum()
    if null_count !=0:
        print(f"Error: {null_count} null values found in '{column_name}' column of {table_name} table.")
    else:
        print(f"No null values found in '{column_name}' column of {table_name} table.")
    
    row_count = df.shape[0]    
    print(f'There are {row_count} rows in {table_name}')
    
users_df = pd.read_csv('data/raw/users.csv')
payments_df = pd.read_csv('data/raw/payments.csv')
tracks_df = pd.read_csv('data/raw/tracks.csv')
listening_df = pd.read_csv('data/raw/listening_events.csv')
tracks_id = set(tracks_df ['track_id'].unique())

listening_id = set(listening_df['track_id'].unique())
missing_tracks_from_tracksTable = listening_id - tracks_id
print(f"Missing track_ids in tracks table: {missing_tracks_from_tracksTable}")

# Check every user_id in listening_events exists in users
listening_user_id = set(listening_df['user_id'].unique())
users_user_id = set(users_df['user_id'].unique())
listening_missing_user_id = listening_user_id - users_user_id
print(f"Missing listening user_ids from users table: {listening_missing_user_id}")

# Check every user_id in payments exists in users
payments_user_id = set(payments_df['user_id'].unique())
payments_missing_user_id = payments_user_id - users_user_id
print(f'Missing payments user_ids from users table: {payments_missing_user_id}')


