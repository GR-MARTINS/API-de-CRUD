from marshmallow import fields, validates, ValidationError
from app.api.schema import ma
from app.api.model import Book, User


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
    livro = fields.String(required=True)
    escritor = fields.String(required=True)

    @validates('id')
    def validate_id(self, value):
        raise ValidationError('id must not be sent')

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    username = fields.String(required=True)
    password = fields.String(required=True)

