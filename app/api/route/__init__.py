from app.api.route.bp_users import bp as bp_users
from app.api.route.bp_books import bp as bp_books
from app.api.route.bp_login import bp as bp_login


def init_app(app):
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_books)
    app.register_blueprint(bp_login)
