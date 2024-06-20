import json
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'accha',
    'user': 'dumball',
    'password': 'tammu123'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS youtube_videos2 (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT,
    channel_name TEXT,
    channel_link TEXT,
    views INTEGER,
    upload_date DATE
);
"""
cursor.execute(create_table_query)

# Read the JSON file
with open('/home/dumball/code/blog-generator/youtube_videos.json', 'r') as file:
    data = json.load(file)

# Insert data into the table
insert_query = sql.SQL("""
INSERT INTO youtube_videos2 (title, link, channel_name, channel_link, views, upload_date)
VALUES (%s, %s, %s, %s, %s, %s)
""")

for video in data:
    # Convert views to integer
    views = video['views'].split()[0]
    if 'K' in views:
        views = int(float(views.replace('K', '')) * 1000)
    elif 'M' in views:
        views = int(float(views.replace('M', '')) * 1000000)
    else:
        views = int(views)

    # Convert upload_date to date
    upload_date_str = video['upload_date']
    if 'day' in upload_date_str:
        days_ago = int(upload_date_str.split()[0])
        upload_date = datetime.now().date() - timedelta(days=days_ago)
    elif 'month' in upload_date_str:
        months_ago = int(upload_date_str.split()[0])
        upload_date = datetime.now().date() - timedelta(days=months_ago * 30)  # Approximate months
    elif 'year' in upload_date_str:
        years_ago = int(upload_date_str.split()[0])
        upload_date = datetime.now().date() - timedelta(days=years_ago * 365)  # Approximate years
    else:
        raise ValueError(f"Unsupported date format: {upload_date_str}")

    cursor.execute(insert_query, (
        video['title'],
        video['link'],
        video['channel_name'],
        video['channel_link'],
        views,
        upload_date
    ))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Successfully imported {len(data)} videos into the database.")