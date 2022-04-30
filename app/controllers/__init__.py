from app.controllers.bp_users import bp as bp_users
from app.controllers.bp_books import bp as bp_books
from app.controllers.bp_login import bp as bp_login


def init_app(app):
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_books)
    app.register_blueprint(bp_login)
