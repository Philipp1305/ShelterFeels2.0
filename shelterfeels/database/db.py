import psycopg2
from shelterfeels.database import config
import json
import os


conn = None
cur = None

CACHE_FILE = "shelter_feels_cache.json"


# Connect to the PostgreSQL database
def setup_to_db():
    try:
        conn = psycopg2.connect(
            host=config.hostname,
            database=config.database,
            user=config.username,
            password=config.password,
            port=config.port,
        )

        # Create a cursor object
        cur = conn.cursor()

        create_table_query = """ CREATE TABLE IF NOT EXISTS shelter_feels (
            id SERIAL PRIMARY KEY,
            emotion VARCHAR(50) NOT NULL,
            word VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) """

        cur.execute(create_table_query)
        conn.commit()

    except Exception as e:
        print("Unable to connect to the database.")
        print(f"Error: {e}")
    finally:
        if cur is not None:
            # Close the cursor
            cur.close()
        if conn is not None:
            # Close the connection
            conn.close()


# Insert a new emotion and word into the database
def insert_emotion(emotion, word):
    print("DB entry", emotion, word)
    try:
        conn = psycopg2.connect(
            host=config.hostname,
            database=config.database,
            user=config.username,
            password=config.password,
            port=config.port,
        )
        cur = conn.cursor()

        insert_query = """ INSERT INTO shelter_feels (emotion, word) VALUES (%s, %s) """
        cur.execute(insert_query, (emotion, word))
        conn.commit()
    except Exception as e:
        print("Unable to connect to the database.")
        print(f"Error: {e}")
    finally:
        if cur is not None:
            # Close the cursor
            cur.close()
        if conn is not None:
            # Close the connection
            conn.close()


# Fetch all emotions and words from the database
def get_data_server():
    try:
        conn = psycopg2.connect(
            host="172.26.236.77",
            database=config.database,
            user=config.username,
            password=config.password,
            port=config.port,
        )
        cur = conn.cursor()

        cur.execute("SELECT EMOTION,WORD FROM shelter_feels")
        data = cur.fetchall()

        cur.close()
        conn.close()

        return data  # Return raw data
    except Exception as e:
        print("Unable to connect to the database.")
        print(f"Error: {e}")
        return None
    finally:
        if cur is not None:
            # Close the cursor
            cur.close()
        if conn is not None:
            # Close the connection
            conn.close()


# Cache all data from the database into a JSON file
def cache_all_data():
    data = get_data_server()
    if data is not None:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print("DB cached.")
    else:
        print("No data to cache.")


# Load cached data from the JSON file
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return []


# if __name__ == "__main__":
#    cache_all_data()
#    load_cache()
