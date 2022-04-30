from flask import Blueprint, request, current_app, jsonify
from app.models.schemas import UserSchema
from app.ext.pydantic_spec import spec
from app.models import model
from flask_pydantic_spec import Response, Request
from app.models.user import User


bp = Blueprint('users', __name__)


@bp.post('/api/v1/usuarios')
@spec.validate(
    body=model.User,
    resp=Response(HTTP_201=model.User)
)
def register():
    us = UserSchema()

    user = us.load(request.json)
    # import ipdb; ipdb.set_trace()
    user.gen_hash()

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return us.jsonify(user), 201


@bp.get('/api/v1/usuarios')
def read_users():
    us = UserSchema(many=True)
    result = User.query.all()
    return us.jsonify(result), 200


@bp.put('/api/v1/usuarios/<identificator>')
def update(identificator):
    us = UserSchema()

    query = User.query.filter(User.id == identificator)
    try:
        lista = query[0]
    except IndexError:
        return {"message": "response validation error"}, 404

    query.update(request.json)
    current_app.db.session.commit()
    return us.jsonify(query.first()), 201


@bp.delete('/api/v1/usuarios/<identificator>')
def delete(identificator):
    User.query.filter(User.id == identificator).delete()
    current_app.db.session.commit()
    return jsonify('deletado')
