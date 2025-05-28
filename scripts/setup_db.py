import sqlite3
import os
import sys

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/ -> project root
    SCHEMA_PATH = os.path.join(BASE_DIR, 'lib', 'db', 'schema.sql')
    DB_PATH = os.path.join(BASE_DIR, 'lib', 'db', 'articles.db')

    if not os.path.exists(SCHEMA_PATH):
        print(f"Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()

        cursor.executescript(schema_sql)
        conn.commit()
        print("Database setup complete.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
