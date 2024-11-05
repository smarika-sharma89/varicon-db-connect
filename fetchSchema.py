import psycopg2
from pgApp import db_url

# Function to fetch the table names in the database
def fetch_table_names():
    try:
        # Connect to PostgreSQL using the database URL
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Query to get the names of all tables in the public schema
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public';
        """)

        # Fetch all table names
        tables = cur.fetchall()

        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")  # Print each table name

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print("Failed to fetch table names.")
        print("Error:", e)

# TESTING TABLE NAME FETCHING
print("Connection Test----------------")
fetch_table_names()
