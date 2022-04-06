from flask import Blueprint, current_app, request, jsonify
from app.api.model import Book
from app.api.schema.schemas import BookSchema
from app.api.doc import spec, model
from flask_pydantic_spec import Response, Request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required


bp = Blueprint('books', __name__)


@bp.post('/api/v1/livros')
@spec.validate(
    body=model.Book,
    resp=Response(HTTP_201=model.Book)
)
@jwt_required()
def create_book():
    """
    Realiza a inserção de um livro no banco de dados.
    """
    bs = BookSchema()
    try:
        book = bs.load(request.json)
    except ValidationError:
        return {'message': 'id must not be sent'}, 400
    # import ipdb; ipdb.set_trace()
    current_app.db.session.add(book)
    current_app.db.session.commit()
    return bs.jsonify(book), 201


@bp.get('/api/v1/livros')
@spec.validate(
    headers=model.Token,
    resp=Response(HTTP_201=model.ListBooks)
)
@jwt_required()
def read_all_books():
    """
    Busca todos os livros cadastrados no banco de dados.
    """
    bs = BookSchema(many=True)
    result = Book.query.all()
    return bs.jsonify(result), 200


@bp.get('/api/v1/livros/<identificator>')
@spec.validate(
    headers=model.Token,
    resp=Response(HTTP_200=model.Book)
)
def read_book(identificator):
    """
    Busca um livro cadastrado no banco de dados filtrando pelo id.
    """
    bs = BookSchema()

    try:
        result = Book.query.filter(Book.id == identificator)[0]
    except IndexError:
        return {'message': 'Book not found'}, 404

    return bs.jsonify(result), 200


@bp.put('/api/v1/livros/<identificator>')
@spec.validate(
    body=Request(model.Book),
    resp=Response(HTTP_201=model.Book)
)
def update(identificator):
    """
    Busca um livro filtrando pelo id e realiza modificações.
    """
    bs = BookSchema()

    query = Book.query.filter(Book.id == identificator)
    try:
        lista = query[0]
    except IndexError:
        return {"message": "response validation error"}, 404

    query.update(request.json)
    current_app.db.session.commit()
    return bs.jsonify(query.first()), 201


@bp.delete('/api/v1/livros/<identificator>')
@spec.validate(
    resp=Response('HTTP_204')
)
def delete_book(identificator):
    """
    Remove um livro do banco de dados filtrando pelo id.
    """
    Book.query.filter(Book.id == identificator).delete()
    current_app.db.session.commit()
    return jsonify('deletado')


@bp.delete('/api/v1/livros')
@spec.validate(
    body=Request(model.ListIdBooks),
    resp=Response('HTTP_204')
)
def delete_books():
    """
    Remove um livro do banco de dados filtrando pelo id.
    """
    for identificator in request.context.body.dict()['list']:
        Book.query.filter(Book.id == identificator).delete()
    current_app.db.session.commit()
    return jsonify('deletado')
