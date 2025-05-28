# test_author.py
import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import CONN, CURSOR

@pytest.fixture(autouse=True)
def setup_and_teardown():
    CURSOR.executescript('''
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS articles;
        DROP TABLE IF EXISTS magazines;

        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );

        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            FOREIGN KEY(magazine_id) REFERENCES magazines(id)
        );
    ''')
    CONN.commit()
    yield
    CURSOR.executescript('''
        DROP TABLE authors;
        DROP TABLE magazines;
        DROP TABLE articles;
    ''')
    CONN.commit()

def test_author_creation_and_articles():
    author = Author("Alice")
    author.save()
    mag = Magazine("Tech World", "Technology")
    mag.save()
    art = Article("AI Advances", author.id, mag.id)
    art.save()

    assert author in Author.all()
    assert len(author.articles()) == 1
    assert author.articles()[0].title == "AI Advances"