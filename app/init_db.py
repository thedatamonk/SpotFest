import psycopg2
from psycopg2 import sql
from decouple import config

def database_exists(conn, db_name):
    """Check if a database with the given name exists."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
        return cursor.fetchone() is not None


def create_database(db_name, user, password, host="localhost", port="5432"):
    # Connect to the default 'postgres' database
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True  # Enable autocommit

    try:
        if not database_exists(conn, db_name):
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")
    except psycopg2.Error as e:
        print(f"Error creating database {db_name}: {e}")
    finally:
        conn.close()

# Usage
create_database(db_name="spotfest_dev", user=config("DEFAULT_USER"), password=config("DEFAULT_PASSWORD"))
