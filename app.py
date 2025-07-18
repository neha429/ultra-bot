
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API using the API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
model = genai.GenerativeModel("gemini-2.0-flash")

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
