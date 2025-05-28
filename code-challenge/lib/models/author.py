from lib.db.connection import CONN, CURSOR

class Author:

    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        if id:
            Author.all[id] = self

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    def save(self):
        sql = "INSERT INTO authors (name) VALUES (?)"
        CURSOR.execute(sql, (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Author.all[self.id] = self

    def update(self, **attrs):
        columns, values = [], []
        for attr, val in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, val)
                columns.append(f"{attr} = ?")
                values.append(getattr(self, attr))
        if columns:
            values.append(self.id)
            sql = f"UPDATE authors SET {', '.join(columns)} WHERE id = ?"
            CURSOR.execute(sql, values)
            CONN.commit()

    def delete(self):
        if self.id:
            sql = "DELETE FROM authors WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del Author.all[self.id]

    @classmethod
    def find_by_id(cls, author_id):
        sql = "SELECT * FROM authors WHERE id = ?"
        row = CURSOR.execute(sql, (author_id,)).fetchone()
        return cls(row[1], id=row[0]) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM authors WHERE name = ?"
        rows = CURSOR.execute(sql, (name,)).fetchall()
        return [cls(r[1], id=r[0]) for r in rows]

    @classmethod
    def all(cls):
        sql = "SELECT * FROM authors"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(r[1], id=r[0]) for r in rows]

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        from lib.models.magazine import Magazine
        sql = """
            SELECT DISTINCT m.*
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Magazine(r[1], r[2], id=r[0]) for r in rows]
