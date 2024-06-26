# File: scripts/seed_database.py

from db import get_db, engine, Base, YoutubeVideo, VideoSegment
from operations.video_ops import create_video_segment
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModel
import torch
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np

# Load pre-trained model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # You can choose a different model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())

    try:
        # Sample YouTube video IDs (replace with actual video IDs)
        video_ids = ["dQw4w9WgXcQ", "jNQXAC9IVRw", "6-HUgzYPm9g"]

        for video_id in video_ids:
            transcript = get_video_transcript(video_id)
            if not transcript:
                continue

            # Create YoutubeVideo entry
            video = YoutubeVideo(video_id=video_id, title=f"Video {video_id}", description="Sample description")
            db.add(video)
            db.commit()

            # Split transcript into segments (for simplicity, we'll split by sentences)
            import nltk
            nltk.download('punkt')
            sentences = nltk.sent_tokenize(transcript)

            # Create segments with embeddings
            for i, sentence in enumerate(sentences):
                embedding = get_embedding(sentence)
                start_time = datetime.now() + timedelta(seconds=i*10)  # Dummy start times
                end_time = start_time + timedelta(seconds=10)
                
                create_video_segment(
                    db,
                    video_id,
                    sentence,
                    start_time,
                    end_time,
                    embedding.tolist()
                )

        print("Database seeded successfully with video transcripts and embeddings!")

    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()