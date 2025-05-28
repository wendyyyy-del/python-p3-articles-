from lib.db.connection import CONN, CURSOR
from lib.models.article import Article

class Author:

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value.strip()):
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    def save(self):
        sql = "INSERT INTO authors (name) VALUES (?)"
        CURSOR.execute(sql, (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def all(cls):
        sql = "SELECT * FROM authors"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(row[1], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM authors WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[0]) if row else None

    def articles(self):
        return Article.find_by_author(self.id)

    def magazines(self):
        from lib.models.magazine import Magazine
        articles = self.articles()
        magazine_ids = set(article.magazine_id for article in articles)
        return [Magazine.find_by_id(mid) for mid in magazine_ids]
