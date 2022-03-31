from app.api.db import db
from passlib.hash import pbkdf2_sha512


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    livro = db.Column(db.Unicode)
    escritor = db.Column(db.Unicode)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    escritor = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)

    def gen_hash(self):
        self.password = pbkdf2_sha512(self.password)

    def verify_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)
