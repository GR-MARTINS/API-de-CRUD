from flask import Blueprint, current_app, request, jsonify
from api.model import Book
from api.schema.bookschema import BookSchema


bp = Blueprint('books', __name__)


@bp.route('/criar', methods=['POST'])
def create():
    bs = BookSchema()
    book = bs.load(request.json)
    current_app.db.session.add(book)
    current_app.db.session.commit()
    return bs.jsonify(book), 201


@bp.route('/ler', methods=['GET'])
def read():
    bs = BookSchema(many=True)
    result = Book.query.all()
    return bs.jsonify(result), 200


@bp.route('/atualizar/<identificator>', methods=['POST'])
def update(identificator):
    bs = BookSchema()
    query = Book.query.filter(Book.id == identificator)
    query.update(request.json)
    current_app.db.session.commit()
    return bs.jsonify(query.first())


@bp.route('/deletar/<identificator>', methods=['POST'])
def delete(identificator):
    Book.query.filter(Book.id == identificator).delete()
    current_app.db.session.commit()
    return jsonify('deletado')
