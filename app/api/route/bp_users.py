from flask import Blueprint, request, current_app
from app.api.schema.schemas import UserSchema


bp = Blueprint('users', __name__)


@bp.post('/api/usuarios/criar_usuario')
def register():
    us = UserSchema()
    
    user = us.load(request.json)
    #import ipdb; ipdb.set_trace()
    user.gen_hash()

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return us.jsonify(user), 201
