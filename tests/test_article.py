# test_article.py
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

def test_article_properties_and_find():
    author = Author("Carol")
    author.save()
    mag = Magazine("Health Digest", "Health")
    mag.save()
    art = Article("Nutrition Tips", author.id, mag.id)
    art.save()

    assert art in Article.all()
    assert Article.find_by_id(art.id).title == "Nutrition Tips"
    assert art.author().name == "Carol"
    assert art.magazine().name == "Health Digest"
    assert Article.find_by_author(author.id)[0].title == "Nutrition Tips"
    assert Article.find_by_magazine(mag.id)[0].title == "Nutrition Tips"