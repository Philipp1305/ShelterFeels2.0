import psycopg2
from shelterfeels.database import config

conn = None
cur = None


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

        cur.execute("SELECT * FROM shelter_feels")
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

def get_joyful_data():
    try:
        conn = psycopg2.connect(
            host=config.hostname,
            database=config.database,
            user=config.username,
            password=config.password,
            port=config.port,
        )
        cur = conn.cursor()

        # Query to fetch "Joyful" subcategories
        cur.execute(
            "SELECT word FROM shelter_feels WHERE emotion IN ('excited', 'delightful', 'stimulated')"
        )
        data = cur.fetchall()

        cur.close()
        conn.close()

        return [row[0] for row in data]  # Return a list of words
    except Exception as e:
        print("Unable to connect to the database.")
        print(f"Error: {e}")
        return []