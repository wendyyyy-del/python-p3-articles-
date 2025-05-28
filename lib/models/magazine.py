from lib.db.connection import CONN, CURSOR
from lib.models.article import Article

class Magazine:

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value.strip()):
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value.strip()):
            self._category = value.strip()
        else:
            raise ValueError("Category must be a non-empty string")

    def save(self):
        sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def all(cls):
        sql = "SELECT * FROM magazines"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(row[1], row[2], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM magazines WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

    def articles(self):
        return Article.find_by_magazine(self.id)

    def authors(self):
        from lib.models.author import Author
        articles = self.articles()
        author_ids = set(article.author_id for article in articles)
        return [Author.find_by_id(aid) for aid in author_ids]
