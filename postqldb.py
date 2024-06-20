import psycopg2
import json

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

# Execute the table creation query
cursor.execute(create_table_sql)

# Read JSON data from a file
with open('youtube_videos.json', 'r') as f:
    json_data = json.load(f)

# Insert JSON data into the table
for item in json_data:
    cursor.execute(
        "INSERT INTO yt_videos (data) VALUES (%s)",
        (json.dumps(item),)
)




# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Read data from the table
cursor.execute("SELECT * FROM yt_video")
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)  

# Close the cursor and connection
cursor.close()
conn.close()
