from ingine import Video, SessionLocal
from scraping import YouTubeScraper
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

# Function to get transcript and save it as a JSON file
def save_transcript(video_id, filename):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)

    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)
    print(f"Transcript saved to {filename}")


# Create a new session
session = SessionLocal()

# Query the database
videos = session.query(Video).all()

for video in videos:
    video_id = video.link.split('v=')[1].split('&')[0]
    save_transcript(video_id, video.title + ".json" )

    print(video.link)

# Close the session
session.close()
