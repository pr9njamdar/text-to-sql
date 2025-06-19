# Text to SQL

The **Text to SQL** project enables users to convert natural language questions into SQL queries, leveraging advanced NLP models powered by Google Gemini. This application is particularly useful for interacting with SQLite databases by generating accurate SQL queries based on schema information. The system ensures that queries align with the database schema and are automatically validated and corrected before execution.

## Live Demo
Check out the live version of the app here: [Live Demo](https://text-to-sql-hfuc55xvvcsyxo2idbzk5b.streamlit.app/)

## Project Overview

This application takes user-inputted natural language questions, analyzes the database schema, and returns an appropriate SQL query. It utilizes Google Gemini for NLP capabilities, FAISS for schema similarity matching, and SQLAlchemy for database schema inspection. The final queries are validated and corrected to ensure accuracy, avoiding errors due to mismatched table or column names.

## Features

- **Natural Language to SQL**: Convert plain English questions into SQL queries with ease.
- **Schema Awareness**: Automatically inspects the database schema and ensures that generated queries match table and column names correctly.
- **SQL Query Correction**: Automatically corrects SQL queries to match database structure, avoiding execution errors.
- **Streamlit-Based Web Interface**: Provides an easy-to-use interface for uploading databases, asking questions, and viewing results.
- **Supports SQLite**: Works with SQLite databases, making it ideal for lightweight use cases and rapid prototyping.

## Installation Guide

To set up the **Text to SQL** project locally, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Gumdu777/text-to-sql.git
   cd text-to-sql
   ```

2. **Set Up a Virtual Environment**  
   It's recommended to use a virtual environment for dependency management.
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google API Key**  
   Add your Google Generative AI API key to a `.env` file:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```

5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## Detailed Usage Instructions

1. **Upload a Database**  
   Use the Streamlit interface to upload an SQLite database file (`.db` format).

2. **Input a Question**  
   Enter your natural language question in the text input field (e.g., *"How many records are in the students table?"*).

3. **Submit the Question**  
   Upon submission, the system generates and displays an SQL query based on the database schema. It also corrects the query if there are any mismatches in table or column names.

4. **View Results**  
   The query is executed, and the results are displayed directly in the app. Errors, if any, are also shown in the interface.

## Supported Databases

- **SQLite**: This application currently supports SQLite databases. Future updates may extend support to other relational databases.

## Technology Stack

- **Programming Language**: Python
- **Web Framework**: Streamlit
- **NLP Model**: Google Gemini (Google Generative AI) for generating SQL queries
- **Database Schema Inspection**: SQLAlchemy for introspecting the database structure
- **Vector Search**: FAISS (Facebook AI Similarity Search) for schema matching
- **Database**: SQLite for executing generated queries

## Future Enhancements

- **Multi-Database Support**: Extend compatibility to other SQL databases such as MySQL, PostgreSQL, etc.
- **Query Optimization**: Implement advanced query optimization based on schema complexity and indexing.
- **Improved Error Handling**: Enhance the robustness of error messages and query validation steps.
- **User Authentication**: Add user authentication to restrict access and enable personalized sessions.
