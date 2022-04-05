from flask import Blueprint, request, current_app
from app.api.schema.schemas import UserSchema
from app.api.doc import spec, model
from flask_pydantic_spec import Response, Request


bp = Blueprint('users', __name__)


@bp.post('/api/v1/usuarios')
@spec.validate(
    body=model.User,
    resp=Response(HTTP_201=model.User)
)
def register():
    us = UserSchema()

    user = us.load(request.json)
    #import ipdb; ipdb.set_trace()
    user.gen_hash()

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return us.jsonify(user), 201


@bp.get('/api/v1/usuarios')
def read_users():
    ...


@bp.put('/api/v1/usuarios')
def update():
    ...


@bp.delete('/api/v1/usuarios')
def delete():
    ...