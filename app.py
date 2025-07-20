
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import psycopg2

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API using the API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
model = genai.GenerativeModel("gemini-2.0-flash")
# Database connection function
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    def create_table():
    conn = connect_db()
    cur = conn.cursor()
    # Example SQL - replace with your actual table definition
    cur.execute("""
        CREATE TABLE IF NOT EXISTS example_table (
            id SERIAL PRIMARY KEY,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
def log_query(user_input, bot_response):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);",
        (user_input, bot_response)
    )
    conn.commit()
    cur.close()
    conn.close()


# Define function to get the model's response
def my_output(query: str) -> str:
    response = model.generate_content(query)
    return response.text

# Streamlit page configuration
st.set_page_config(page_title="QUERY BOT")
st.header("QUERY BOT")

# Input and button
input_text = st.text_input("Enter your query:", key="input")
submit = st.button("Ask your query")

# Display response if user submits
if submit and input_text:
    response = my_output(input_text)
    st.subheader("The Response is:")
    st.write(response)
