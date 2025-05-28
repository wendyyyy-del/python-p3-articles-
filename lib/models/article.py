from lib.db.connection import CONN, CURSOR

class Article:
    all = {}

    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article id={self.id} title='{self.title}'>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and len(value.strip()):
            self._title = value.strip()
        else:
            raise ValueError("Title must be a non-empty string")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str) and len(value.strip()) > 1:
            self._content = value.strip()
        else:
            raise ValueError("Content must be a non-empty string with more than one character")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if isinstance(value, int):
            self._author_id = value
        else:
            raise ValueError("author_id must be an integer")

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if isinstance(value, int):
            self._magazine_id = value
        else:
            raise ValueError("magazine_id must be an integer")

    def save(self):
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM articles WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(row[1], row[2], row[3], row[4], row[0]) if row else None

    @classmethod
    def find_by_author(cls, author_id):
        sql = "SELECT * FROM articles WHERE author_id = ?"
        rows = CURSOR.execute(sql, (author_id,)).fetchall()
        return [cls(r[1], r[2], r[3], r[4], r[0]) for r in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        sql = "SELECT * FROM articles WHERE magazine_id = ?"
        rows = CURSOR.execute(sql, (magazine_id,)).fetchall()
        return [cls(r[1], r[2], r[3], r[4], r[0]) for r in rows]

    @classmethod
    def all(cls):
        sql = "SELECT * FROM articles"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(r[1], r[2], r[3], r[4], r[0]) for r in rows]

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)
