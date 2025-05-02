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


if __name__ == "__main__":
    setup_to_db()
    insert_emotion("happy", "joy")
    insert_emotion("sad", "sorrow")
    insert_emotion("angry", "rage")
    insert_emotion("surprised", "shock")
    insert_emotion("disgusted", "revulsion")
