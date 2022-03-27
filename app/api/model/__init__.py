from api.db import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    livro = db.Column(db.Unicode)
    escritor = db.Column(db.Unicode)
