import os
import google.generativeai as genai
import time
import pprint

# Function to measure execution time
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
  "max_output_tokens": 81920,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "follow json format { 'questions' 'blah blha;\nanswer : blah blah ,\ntone: funny/witty,ormal, casual, friendly, professional, humorous, etc.\nBehavior: Polite, assertive, empathetic, sarcastic\n}\nonly the json nothing else",
        "generate 5 pairs like this in 1 json",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"questions\": [\n    {\n      \"question\": \"What is the meaning of life?\",\n      \"answer\": \"42.  But seriously, it's probably about finding your own purpose and making the most of the time you have.\",\n      \"tone\": \"humorous\",\n      \"behavior\": \"friendly\"\n    },\n    {\n      \"question\": \"How do I fix a broken heart?\",\n      \"answer\": \"Time, friends, and a good playlist.  You'll get through this, I promise.\",\n      \"tone\": \"casual\",\n      \"behavior\": \"empathetic\"\n    },\n    {\n      \"question\": \"What's the best way to learn a new language?\",\n      \"answer\": \"Immersion, dedication, and maybe a little bit of bribery (with cookies, perhaps).\",\n      \"tone\": \"funny\",\n      \"behavior\": \"polite\"\n    },\n    {\n      \"question\": \"What is the capital of France?\",\n      \"answer\": \"Paris, of course!  Did you think I'd say something else?\",\n      \"tone\": \"witty\",\n      \"behavior\": \"assertive\"\n    },\n    {\n      \"question\": \"How can I be more productive?\",\n      \"answer\": \"Set realistic goals, break down big tasks, and don't be afraid to take breaks.  And maybe a little bit of caffeine, but don't overdo it.\",\n      \"tone\": \"professional\",\n      \"behavior\": \"polite\"\n    }\n  ]\n}\n``` \n",
      ],
    },
  ]
)

@timeit
def gen():
      response = chat_session.send_message("INSERT_INPUT_HERE")
      print(response._chunks, response._result, response.__doc__)


gen()