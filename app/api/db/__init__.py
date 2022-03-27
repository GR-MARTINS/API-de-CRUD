from flask_sqlalchemy import SQLAlchechemy


db = SQLAlchechemy()


def init_app(app):
    db.init_app(app)
    app.db = db
