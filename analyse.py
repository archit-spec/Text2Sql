import psycopg2
from pgvector.psycopg2 import register_vector
import google.generativeai as genai
import os
import requests


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

# Register the vector type with psycopg2
register_vector(cursor)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 81920
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Create a chat session
chat_session = model.start_chat() 

def translate_to_sql(question):
    response = chat_session.send_message(f"Do not output any other text. Translate the following natural language question into an SQL query:\n\nQuestion: {question}\n\nSQL Query:")

    sql_query = response.text.strip()
    return sql_query

def execute_query(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def translate_to_natural_language(results, question):
    context = "\n".join([f"Title: {row[1]}, Channel: {row[3]}, Views: {row[5]}" for row in results])
    response = chat_session.send_message(f"Translate the following natural language question into an SQL query:\n\nQuestion: {question}\n\nSQL Query:")

    answer = response.text.strip()
    return answer

def main():
    while True:
        question = input("Ask a question: ")
        if question.lower() in ["exit", "quit"]:
            break
        sql = translate_to_sql(question)
        print("SQL Query:", sql)
        results = execute_query(sql)
        answer = translate_to_natural_language(results, question)
        print("Answer:", answer)

if __name__ == "__main__":
    main()

# Insert a row with a vector
cursor.execute("""
    INSERT INTO items (name, embedding)
    VALUES (%s, %s)
""", ('item1', [1.0, 2.0, 3.0]))

# Commit the transaction
conn.commit()

# Query the table
cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
