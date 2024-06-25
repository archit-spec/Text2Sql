import json
from pytube import YouTube
from moviepy.editor import AudioFileClip
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from huggingface_hub import HfApi
import re

# Path to the JSON file
json_file_path = '/content/youtube_videos2.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    videos = json.load(file)

def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

def download_and_upload_video(video):
    url = video['link']
    title = sanitize_filename(video['title'])
    final_filename = f"{title}.mp3"

    if os.path.exists(final_filename):
        print(f"{final_filename} already exists, skipping download.")
        upload_to_huggingface(final_filename, title)
        return

    print(f"Downloading {title} from {url}")
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    temp_filename = f"{title}_temp_audio.mp4"
    stream.download(filename=temp_filename)

    audio = AudioFileClip(temp_filename)
    audio.write_audiofile(final_filename, codec='mp3')
    audio.close()

    os.remove(temp_filename)

    # Upload to Hugging Face
    upload_to_huggingface(final_filename, title)

def upload_to_huggingface(filename, title):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id=f"archit11/chiptune_music",
        repo_type="dataset",
        commit_message=f"Upload {title}"
    )
    print(f"Uploaded {filename} to Hugging Face with label {title}")

# Use ThreadPoolExecutor to download and upload videos in parallel
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = [executor.submit(download_and_upload_video, video) for video in videos]
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")

print("All downloads and uploads completed.")
