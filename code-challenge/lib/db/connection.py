import sqlite3

def get_connection():
conn = sqlite3.connect('articles.db')
conn.row_factory = sqlite3.Row 
return conn
 import sqlite3

CONN = sqlite3.connect("test_database.db")
CURSOR = CONN.cursor()
