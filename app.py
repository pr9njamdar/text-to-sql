from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide SQL queries as a response
def get_gemini_response(question, schema_info):
    # Build a more detailed prompt with schema information
    prompt = f"""
    You are an expert in converting English questions to SQL query.
    The SQL database has the following tables and columns:
    
    {schema_info}
    
    The SQL query should match the schema and should not include any invalid table or column names.
    Ensure that the query does not start or end with backticks (```).
    
    Example:
    Question: How many entries are in the students table?
    SQL command: SELECT COUNT(*) FROM students;

    Now, for the given question: "{question}", please generate a valid SQL query.
    """
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])

    # Clean the response by removing any leading/trailing triple backticks
    cleaned_response = response.text.strip("```").strip()

    return cleaned_response


# Function to retrieve query results from the SQLite database
def read_sql_query(sql, db_file):
    try:
        # Create a connection to the uploaded SQLite database file
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return str(e)

# Function to use SQLAlchemy for inspecting the database schema
def get_schema_info_with_sqlalchemy(db_file):
    schema_info = {}
    try:
        # Create a SQLAlchemy engine
        engine = create_engine(f'sqlite:///{db_file}')
        inspector = inspect(engine)

        # Get all table names
        table_names = inspector.get_table_names()

        # Get column names for each table
        for table in table_names:
            columns = inspector.get_columns(table)
            column_names = [column['name'] for column in columns]
            schema_info[table] = column_names

        return schema_info
    except SQLAlchemyError as e:
        return str(e)

# Function to validate and correct SQL query by matching with schema
def validate_sql_query(query, schema_info):
    corrected_query = query

    # Match table and column names exactly with schema_info
    for table, columns in schema_info.items():
        # If the table name is in the query, correct it
        if table.lower() in query.lower():
            corrected_query = corrected_query.replace(table.lower(), table)

        # If any column names are in the query, correct them
        for column in columns:
            if column.lower() in query.lower():
                corrected_query = corrected_query.replace(column.lower(), column)

    return corrected_query

# Streamlit App
st.set_page_config(page_title="SQL Query Generator")
st.header("Gemini-powered SQL Query Generator with Schema Matching")

# Allow the user to upload a SQLite database file
uploaded_file = st.file_uploader("Upload SQLite Database", type=["db"])

# Input for the question
question = st.text_input("Input your question:")

# Button to submit the question
submit = st.button("Ask the question")

# If a file is uploaded and submit button is clicked
if uploaded_file and submit:
    if question.strip() == "":
        st.error("Please enter a valid question.")
    else:
        try:
            # Save the uploaded database file temporarily
            with open("temp_database.db", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Get schema (tables and columns) from the database using SQLAlchemy
            schema_info = get_schema_info_with_sqlalchemy("temp_database.db")
            
            # Prepare schema info in a readable format for Gemini prompt
            formatted_schema_info = "\n".join([f"Table {table}: {', '.join(columns)}" for table, columns in schema_info.items()])
            
            # Get the SQL query from the Gemini model
            response = get_gemini_response(question, formatted_schema_info)
            st.subheader("Generated SQL Query:")
            st.code(response, language='sql')

            # Validate and correct the SQL query with the actual schema
            corrected_query = validate_sql_query(response, schema_info)
            st.subheader("Corrected SQL Query:")
            st.code(corrected_query, language='sql')

            # Execute the corrected SQL query on the uploaded database
            result = read_sql_query(corrected_query, "temp_database.db")

            # Display the results or error
            st.subheader("Query Results:")
            if isinstance(result, str):
                st.error(f"Error: {result}")
            else:
                for row in result:
                    st.write(row)
        
        except Exception as e:
            st.error(f"Error processing the query: {e}")
