from flask_pydantic_spec import FlaskPydanticSpec

spec = FlaskPydanticSpec('flask', title='API Books')


def init_app(app):
    spec.register(app)
