import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # lib/db
DB_PATH = os.path.join(BASE_DIR, 'articles.db')

CONN = sqlite3.connect(DB_PATH)
CONN.row_factory = sqlite3.Row
CURSOR = CONN.cursor()
