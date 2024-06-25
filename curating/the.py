import psycopg2
import google.generativeai as genai
import os
import re

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'accha',
    'user': 'dumball',
    'password': 'tammu123'
}
# Global variables for database connection
conn = None
cursor = None

def connect_to_db():
    global conn, cursor
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        print("Successfully connected to the database.")
    except psycopg2.Error as e:
        print(f"Unable to connect to the database: {e}")
        exit(1)

def reset_connection():
    global conn, cursor
    if conn:
        conn.rollback()  # Rollback any aborted transactions
        conn.close()
    if cursor:
        cursor.close()
    connect_to_db()

connect_to_db()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.0,
    "top_p": 0.95,
    "top_k": 50,
    "max_output_tokens": 1024
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

def translate_to_sql(question):
    prompt = f"""
    Translate the following natural language question into a valid SQL query for a table named 'youtube_videos2' with the following columns:
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT,
    channel_name TEXT,
    channel_link TEXT,
    views INTEGER,
    upload_date DATE
    Important notes:
    1. The 'views' column is stored as INTEGER 
    3. For sorting by views, use ORDER BY numeric_views DESC
    4. Limit results to top 5 unless specified otherwise
    5. When asked about "best" videos, interpret this as "most viewed" videos

   
    If the question cannot be translated into a meaningful SQL query, respond with 'INVALID_QUERY'.
    Do not include any explanations or comments, just the raw SQL query or 'INVALID_QUERY'.

    Question: {question}

    SQL Query:
    """
    response = chat_session.send_message(prompt)
    sql_query = response.text.strip()
    
    # Remove any remaining markdown formatting
    sql_query = re.sub(r'```sql|```', '', sql_query).strip()
    
    # Check if the query is empty or just comments
    if sql_query == 'INVALID_QUERY' or not sql_query or sql_query.startswith('--'):
        return None
    return sql_query

def translate_to_natural_language(results, question):
    if not results:
        return "No results found for the given query."
    
    # Convert results to a string representation
    result_str = "\n".join([str(row) for row in results[:5]])
    
    prompt = f"""
    Given the following data from a YouTube videos database and the original question, provide a concise and informative answer:

    Data:
    {result_str}

    Original Question: {question}

    Please format the answer as follows:
    1. Start with a brief introduction sentence explaining what the data represents.
    2. List the top videos (if applicable) with their titles, view counts, and channel names.
    3. If relevant, provide any additional insights or summary statistics.
    4. Conclude with a sentence that ties back to the original question.

    Answer:
    """
    
    response = chat_session.send_message(prompt)
    answer = response.text.strip()
    return answer

def execute_query(sql):
    global conn, cursor
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"An error occurred while executing the query: {e}")
        print("Attempting to reset the database connection...")
        reset_connection()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error persists after resetting connection: {e}")
            return None

def main():
    print("Welcome to the YouTube Videos Database Chat!")
    print("You can ask questions about the videos in the database.")
    print("Type 'exit' or 'quit' to end the session.")
    
    while True:
        question = input("\nAsk a question: ")
        if question.lower() in ["exit", "quit"]:
            break
        
        if not question.strip():
            print("Please enter a valid question.")
            continue
        
        sql = translate_to_sql(question)
        if sql is None:
            print("I'm sorry, but I couldn't translate that into a valid SQL query. Could you please rephrase your question or ask about specific data in the database?")
            continue
        
        print("\nSQL Query:", sql)
        results = execute_query(sql)
        if results is not None:
            answer = translate_to_natural_language(results, question)
            print("\nAnswer:", answer)

    print("\nThank you for using the YouTube Videos Database Chat. Goodbye!")

if __name__ == "__main__":
    main()

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()