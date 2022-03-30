from flask import Blueprint, current_app, request, jsonify
from app.api.model import Book
from app.api.schema.bookschema import BookSchema
from app.api.doc import spec, model
from flask_pydantic_spec import Response, Request
from marshmallow import ValidationError


bp = Blueprint('books', __name__)


@bp.post('/criar')
@spec.validate(
    body=model.BookPydantic,
    resp=Response(HTTP_201=model.BookPydantic)
)
def create():
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


@bp.get('/ler/')
def read_all_books():
    """
    Busca todos os livros cadastrados no banco de dados.
    """
    bs = BookSchema(many=True)
    result = Book.query.all()
    return bs.jsonify(result), 200


@bp.get('/ler/<identificator>')
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


@bp.put('/atualizar/<identificator>')
@spec.validate(
    body=Request(model.BookPydantic),
    resp=Response(HTTP_200=model.BookPydantic)
)
def update(identificator):
    """
    Busca um livro filtrando pelo id e realiza modificações.
    """
    bs = BookSchema()
    query = Book.query.filter(Book.id == identificator)
    query.update(request.json)
    current_app.db.session.commit()
    return bs.jsonify(query.first())


@bp.delete('/deletar/<identificator>')
@spec.validate(
    body=Request(model.BookPydantic),
    resp=Response('HTTP_204')
)
def delete_book(identificator):
    """
    Remove um livro do banco de dados filtrando pelo id.
    """
    Book.query.filter(Book.id == identificator).delete()
    current_app.db.session.commit()
    return jsonify('deletado')


@bp.delete('/deletar')
@spec.validate(
    body=Request(model.ListIdBooksPydantic),
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
