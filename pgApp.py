# Import necessary modules
from dotenv import load_dotenv
load_dotenv()

# importing postgress
import psycopg2

import streamlit as st
import os
import openai

# Configure the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Retrieve database configuration from environment variables
db_name = 'staging_sept_23'
db_user = 'postgres'
db_host = 'localhost'
db_port = 5432
db_password = ''  # No password

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Function to load GPT model and provide SQL query as the response
def get_gpt_response(question, prompt):
    # Define the messages for the model
    messages = [
        {"role": "system", "content": prompt[0]},
        {"role": "user", "content": question}
    ]

    # Call the OpenAI API with the gpt-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    # Return the response text
    return response.choices[0].message["content"].strip()

# Function to retrieve query from the SQL database (using PostgreSQL)
def execute_sql_query(sql):  # Renamed function to avoid conflict
    # Connect to PostgreSQL
    conn = psycopg2.connect(db_url)

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    # Close the connection
    conn.close()
    return rows

# TESTING!
def test_db_connection():
    print("Database port:", db_port)  # Add this line to check the retrieved port value
    
    try:
        # Attempt to connect to the PostgreSQL database
        conn = psycopg2.connect(db_url)
        
        # If connection is successful, print a success message
        print("Connection to PostgreSQL database was successful!")
        conn.close()  # Close the connection after testing

    except Exception as e:
        # If there’s an error, print the error message
        print("Failed to connect to PostgreSQL database.")
        print("Error:", e)

print("Connection Test----------------")
test_db_connection()

# Defining the prompt
prompt = [
    """
    You are an expert in converting English questions to Postgress SQL query!
    The postgress database contains many tables. 
    Do not add ``` or the word 'sql' in the response.
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL Query")
st.header("GPT App to Retrieve SQL Data")

# User input
question = st.text_input("Input your question in English: ", key="input")

# Submit button
submit = st.button("Ask the question")

# If the submit button is clicked
if submit and question:
    # SQL query from GPT
    response = get_gpt_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.write(response)

    # Execute SQL query on the database
    try:
        data = execute_sql_query(response)  # Call the renamed function
        st.subheader("SQL Query Results")
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No results found.")
    except Exception as e:
        print(f"An error occurred during SQL execution: {e}")  # Detailed logging
        st.error(f"An error occurred: {e}")  # User-friendly error message