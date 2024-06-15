import ffmpeg
import pandas as pd
import multiprocessing as mp
import os

def split_video(input_path, output_path, start_time, end_time):
    try:
        (
            ffmpeg
            .input(input_path, ss=start_time, to=end_time)
            .output(output_path)
            .run(overwrite_output=True, quiet=True, capture_stdout=True, capture_stderr=True)
        )
        print(f"Successfully created {output_path}")
    except ffmpeg.Error as e:
        print(f"Error occurred for {output_path}: {e}")

def process_row(row, input_video_path):
    start_time = row['start_time']
    end_time = row['end_time']
    chunk_id = row['chunk_id']
    output_path = f"{chunk_id}.mp4"
    split_video(input_video_path, output_path, start_time, end_time)
    
    
df = pd.read_csv("/kaggle/input/transcript/data.csv")
input_video_path = '/kaggle/working/out.webm'
with mp.Pool(mp.cpu_count()) as pool:
    pool.starmap(process_row, [(row, input_video_path) for index, row in df.iterrows()])
