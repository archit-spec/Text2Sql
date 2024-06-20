import os
import google.generativeai as genai
import time
import pprint
import json
import glob


def concatenate_transcript_text(transcript_file):
  with open(transcript_file, 'r') as f:
    transcript_data = json.load(f)

  concatenated_text = ""
  for item in transcript_data:
    concatenated_text += item["text"] + " "

  return concatenated_text.strip()

# Example usage:
for file in glob.glob(os.path.join(os.getcwd(), "transcripts", "*.json")):
   concatenated_text = concatenate_transcript_text(transcript_file)

#function to time it
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 81920,TODO: put cpu in bus not the other way around

}


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.generate_content()

@timeit
def gen():
      response = chat_session.send_message("INSERT_INPUT_HERE")
      print(response._chunks, response._result, response.__doc__)


gen()