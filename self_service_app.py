import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import pyodbc


# Function for API CALL----------------------------------------------------------
def api_call(system, user):
    # Fetch API Key
    with open('api_key.txt', 'r') as file:
        api_key = file.read()

    # Create the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Make the API call
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    
    # Return the content of the response
    return completion.choices[0].message.content
# ----------------------------------------------------------



# ESTABLISHING THE MYSQL DATABASE CONNECTION----------------------------------------------------------
server = 'data-sonic-trail-server.database.windows.net'
database = 'data-sonic-trail'
username = 'sqlroot'
password ='root@123'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = conn.cursor()
# ----------------------------------------------------------


## SCHEMA FETCHING ----------------------------------------------------------
# Dictionary to hold schema information
schema_dict = {}

# Fetch list of all tables in the database
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = cursor.fetchall()

# Loop through each table and fetch its schema details
for table in tables:
    table_name = table[0]
    
    # Query to fetch schema details for the current table
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, COALESCE(CHARACTER_MAXIMUM_LENGTH, '') 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
    """)
    columns = cursor.fetchall()
    
    # Store schema details in the dictionary
    schema_dict[table_name] = [(col[0], col[1], col[2]) for col in columns]

# Convert the schema dictionary to a compact formatted string
schema_str = "\n".join(
    f"{table}: {', '.join(f'{col[0]} {col[1]}({col[2]})' if col[2] else f'{col[0]} {col[1]}' for col in cols)}"
    for table, cols in schema_dict.items()
)
## --------------------------------------------------------------------------------------------------------------------


# Streamlit UI Setup  ----------------------------------------------------------
st.title("Adro-Visualizer-Chatbot")

tab1, tab2 = st.tabs(["Data Visualizer", "Chat-Bot"])

## Tab1 ----------------------------------------------------------
with tab1:
# GPT Data Visualization Area
  st.header("Data Visualizer")
  user_input = st.text_area("Enter your query:", "", key= "header_tab1")
  generate_button = st.button("Generate", key="button_tab1")

# Process the prompt using GPT
  if generate_button :
    # SQL Query System Prompt
    system_prompt = "You are a SQL Query generation assistant. Based on the table schema provided, generate SQL queries to fulfill the user's request.Please provide only the SQL query without any explanations, comments, or additional text. Do not include any Markdown formatting. The output should be ready to be executed without modification."
# SQL Query Generation User Prompt
    user_prompt = user_input + "The Schema for all the tables present in the database is as follows: " + schema_str

# Storing the Recieved Sql Query in a variable
    sql_query = api_call(system = system_prompt, user = user_prompt)


# Execute the SQL Query
    cursor.execute(sql_query)
    result = cursor.fetchall()

#Storing the ouput of the Query execution
    result_str = str(result)

# Visualization System Prompt
    system_prompt = "You are a code generation assistant. Please provide only the Python code without any explanations, comments, or additional text. Do not include any Markdown formatting, such as ```python or ``` at the beginning or end. The output should be ready to be executed without modification."

# Visualization User Prompt
    user_prompt = user_input + "The data that you have to work as is attached as follows: " + result_str

  # API Request for Visualization Code Generation 
    visualization_code = api_call(system=system_prompt, user=user_prompt)
    plot_area = st.empty()
    plot_area.pyplot(exec(visualization_code))


with tab2:
# GPT Data Visualization Area
  st.header("Chat-Bot")
  user_input = st.text_area("Enter your query", "", key="header_tab2")
  generate_button = st.button("Generate", key="button_tab2")

# Process the prompt using GPT
  if generate_button :
    # SQL Query System Prompt
    system_prompt = "You are a SQL Query generation assistant. Based on the table schema provided, generate SQL queries to provide an answer to the user.Please provide only the SQL query without any explanations, comments, or additional text. Do not include any Markdown formatting. The output should be ready to be executed without modification."
# SQL Query Generation User Prompt
    user_prompt = user_input + "The Schema for all the tables present in the database is as follows: " + schema_str

# Storing the Recieved Sql Query in a variable
    sql_query = api_call(system = system_prompt, user = user_prompt)


# #SQL Query Syntax Checker
#   # SQL Query System Prompt
#     system_prompt = "You are a SQL Query Syntax checker and validator. Check the provided query and make the required changes if any.Please provide only the correct SQL query without any explanations, comments, or additional text. Do not include any Markdown formatting. The output should be ready to be executed without modification."
# # SQL Query Generation User Prompt
#     user_prompt = "The Schema for all the tables present in the database is as follows: " + schema_str + "And the SQL query to validate is as follows: " + sql_query

#     verified_sql_query = api_call(system=system_prompt, user=user_prompt)

# Execute the SQL Query
    cursor.execute(sql_query)
    result = cursor.fetchall()

#Storing the ouput of the Query execution
    result_str = str(result)

# Chatbot System Prompt
    system_prompt = "You are a data wizard that can answer questions based on the user input and you are recieving the corresponding queried data from the database to answer the query.Precisely give only the answer and no extra information."

# Chatbot User Prompt
    user_prompt = user_input + "The data that you have to work as is attached as follows: " + result_str

  # API Request for Chatbot Response
    chatbot_response = api_call(system=system_prompt, user=user_prompt)
    
    st.subheader("Chat-Bot Response:")
    st.write(chatbot_response)  


# Close the connection when the app is closed
if 'connection' in locals() and conn.is_connected():
    conn.close()
    cursor.close()
