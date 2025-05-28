import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lib.db.connection import CONN, CURSOR

def seed():
    # Clear existing data (optional, for fresh start)
    CURSOR.execute("DELETE FROM articles")
    CURSOR.execute("DELETE FROM authors")
    CURSOR.execute("DELETE FROM magazines")
    CONN.commit()

    # Insert authors
    authors = [
        ("Jane Austen",),
        ("Mark Twain",),
        ("Virginia Woolf",)
    ]
    CURSOR.executemany("INSERT INTO authors (name) VALUES (?)", authors)

    # Insert magazines
    magazines = [
        ("Classic Literature", "Literature"),
        ("Modern Fiction", "Fiction"),
        ("Historical Monthly", "History")
    ]
    CURSOR.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)

    CONN.commit()

    # Fetch inserted author and magazine IDs
    CURSOR.execute("SELECT id, name FROM authors")
    authors_dict = {name: id for id, name in CURSOR.fetchall()}

    CURSOR.execute("SELECT id, name FROM magazines")
    magazines_dict = {name: id for id, name in CURSOR.fetchall()}

    # Insert articles with valid content and references to author_id and magazine_id
    articles = [
        (
            "Pride and Prejudice Review",
            "An insightful review of Jane Austen's classic novel Pride and Prejudice.",
            authors_dict["Jane Austen"],
            magazines_dict["Classic Literature"]
        ),
        (
            "Adventures of Huckleberry Finn Summary",
            "A comprehensive summary of Mark Twain's Adventures of Huckleberry Finn.",
            authors_dict["Mark Twain"],
            magazines_dict["Classic Literature"]
        ),
        (
            "Stream of Consciousness Techniques",
            "Exploring the narrative style pioneered by Virginia Woolf.",
            authors_dict["Virginia Woolf"],
            magazines_dict["Modern Fiction"]
        ),
        (
            "History of 19th Century Literature",
            "A detailed look at the literary movements of the 19th century.",
            authors_dict["Jane Austen"],
            magazines_dict["Historical Monthly"]
        )
    ]
    CURSOR.executemany(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", articles
    )

    CONN.commit()
    print("Database seeded with valid sample data.")

if __name__ == "__main__":
    seed()
