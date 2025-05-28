from lib.db.connection import CONN, CURSOR

class Magazine:

    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
        if id:
            Magazine.all[id] = self

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value.strip():
            self._category = value.strip()
        else:
            raise ValueError("Category must be a non-empty string")

    def save(self):
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Magazine.all[self.id] = self

    def update(self, **attrs):
        columns, values = [], []
        for attr, val in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, val)
                columns.append(f"{attr} = ?")
                values.append(getattr(self, attr))
        if columns:
            values.append(self.id)
            sql = f"UPDATE magazines SET {', '.join(columns)} WHERE id = ?"
            CURSOR.execute(sql, values)
            CONN.commit()

    def delete(self):
        if self.id:
            sql = "DELETE FROM magazines WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del Magazine.all[self.id]

    @classmethod
    def find_by_id(cls, magazine_id):
        sql = "SELECT * FROM magazines WHERE id = ?"
        row = CURSOR.execute(sql, (magazine_id,)).fetchone()
        return cls(row[1], row[2], id=row[0]) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM magazines WHERE name = ?"
        rows = CURSOR.execute(sql, (name,)).fetchall()
        return [cls(r[1], r[2], id=r[0]) for r in rows]

    @classmethod
    def all(cls):
        sql = "SELECT * FROM magazines"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(r[1], r[2], id=r[0]) for r in rows]

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_magazine(self.id)

    def authors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author(r[1], r[2], id=r[0]) for r in rows]
