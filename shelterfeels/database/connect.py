import psycopg2
import config

conn = None
cur = None

# Connect to the PostgreSQL database

try:

    conn = psycopg2.connect(
        host=config.hostname,
        database=config.database,
        user=config.username,
        password=config.password,
        port=config.port
    )

    # Create a cursor object
    cur = conn.cursor()

    create_table_query = ''' CREATE TABLE IF NOT EXISTS shelter_feels (
        id SERIAL PRIMARY KEY,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) '''
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
    