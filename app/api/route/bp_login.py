from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token
from app.api.schema.schemas import UserSchema
from app.api.model import User
from app.api.doc import spec, model
from flask_pydantic_spec import Response, Request


bp = Blueprint('login', __name__)


@bp.post('/api/v1/login')
@spec.validate(
    body=model.User,
    resp=Response(HTTP_201=model.User)
)
def login():
    us = UserSchema()
    user = us.load(request.json)
    user = User.query.filter_by(username=user.username).first()
    if user and user.verify_password(request.json['password']):
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(seconds=600)
        )
        refresh_token = create_refresh_token(identity=user.id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'sucess'
        }, 200
    return {
        'message': 'Deu ruim! credenciais inválidas'
    }, 401
