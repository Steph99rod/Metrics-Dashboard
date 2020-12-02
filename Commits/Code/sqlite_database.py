import sqlite3
import os
import sys


def open_connection(repo_name):
    """
    This is some SQL code that creates the tables and columns in a database named after the repository its data is holding.
    """
    try:
        connection = sqlite3.connect("/metrics/" + str(repo_name) + ".db")
    except sqlite3.OperationalError as e: 
        sys.exit(f"Could not connect to {str(repo_name)}: {e}")

    cursor = connection.cursor()

    # Create table - COMMITS
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS COMMITS (author VARCHAR(3000), author_date VARCHAR(3000), committer VARCHAR(3000), committer_date VARCHAR(3000), commits_url VARCHAR(3000), message VARCHAR(30000), comment_count VARCHAR(3000), comments_url VARCHAR(3000));"
    )
    # Create table - COMMITS_CALCULATIONS
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS COMMITS_CALCULATIONS (calc_name VARCHAR(3000), value VARCHAR(3000), unit VARCHAR(3000));"
    )
    # Create table - COMMITS_CALCULATIONS
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS COMMITS_CALCULATIONS_HOURLY (commiter_calendar_date VARCHAR(3000), committer_hour VARCHAR(3000));"
    )
    connection.commit()

    return cursor, connection
