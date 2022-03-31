from unittest import TestCase
from flask import url_for
from app.app import create_app


class TestFlaskBase(TestCase):
    def setUp(self):
        """
        é executado antes de todos os testes
        """
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

    def tearDown(self):
        """
        é executado após todos os testes
        """
        self.app.db.drop_all()


class TesteCriar(TestFlaskBase):
    def test_criar_deve_retornar_o_payload_enviado_sem_id(self):
        dado = {
            'livro': 'python3',
            'escritor': 'Glayton'
        }

        response = self.client.post(url_for('books.create'), json=dado)

        # import ipdb; ipdb.set_trace()

        response = response.json
        response.pop('id')
        self.assertEqual(dado, response)


    def test_criar_deve_retornar_erro_quando_o_payload_for_incompleto(self):

        dado = {
            'livro': 'python3',
            # 'escritor': 'Glayton'
        }

        esperado = [{'loc': ['escritor'], 'msg': 'field required', 'type': 'value_error.missing'}]
        response = self.client.post(url_for('books.create'), json=dado)

        # import ipdb; ipdb.set_trace()

        self.assertEqual(esperado, response.json)

    def test_criar_deve_retornar_erro_quando_o_payload_contiver_a_chave_id(self):

        dado = {
            'livro': 'python3',
            'escritor': 'Glayton',
            'id': '1'

        }

        esperado = {'message': 'id must not be sent'}
        response = self.client.post(url_for('books.create'), json=dado)

        # import ipdb; ipdb.set_trace()

        self.assertEqual(esperado, response.json)


class TesteLer(TestFlaskBase):
    def teste_ler_deve_retornar_uma_query_vazia(self):
        esperado = []
        response = self.client.get(url_for('books.read_all_books'))
        self.assertEqual(esperado, response.json)

    def teste_ler_deve_retornar_uma_query_com_elemento_inserido(self):
        livro = {'escritor': 'glayton', 'livro': 'python3'}
        self.client.post(url_for('books.create'), json=livro)
        response = self.client.get(url_for('books.read_all_books'))
        self.assertEqual(1, len(response.json))

    def teste_ler_deve_retornar_uma_query_com_elemento_solicitado_pelo_id(self):
        livro = {'escritor': 'glayton', 'livro': 'python3'}
        self.client.post(url_for('books.create'), json=livro)
        response = self.client.get(url_for('books.read_book', identificator=1))
        self.assertEqual(3, len(response.json))

    def teste_ler_deve_retornar_um_erro_se_o_id_solicitado_nao_existir(self):
        esperado = {'message': 'Book not found'}
        response = self.client.get(url_for('books.read_book', identificator=1))
        self.assertEqual(esperado, response.json)
