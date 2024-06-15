from engine import Video, SessionLocal

# Create a new session
session = SessionLocal()

# Query the database
videos = session.query(Video).all()

for video in videos:
    print(video.link)

# Close the session
session.close()