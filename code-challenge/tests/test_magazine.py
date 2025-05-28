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
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS magazines;
        DROP TABLE IF EXISTS articles;
    ''')
    CONN.commit()

def test_magazine_relationships():
    author = Author("Bob")
    author.save()
    mag = Magazine("Science Today", "Science")
    mag.save()
    art = Article("Quantum Mechanics", author.id, mag.id)
    art.save()

    assert mag in Magazine.all()
    assert len(mag.articles()) == 1
    assert mag.articles()[0].title == "Quantum Mechanics"
    assert mag.authors()[0].name == "Bob"
