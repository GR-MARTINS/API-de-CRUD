from flask import url_for
from tests.flask_base_test import TestFlaskBase


class TesteCriar(TestFlaskBase):
    def test_criar_deve_retornar_o_payload_enviado_sem_id(self):
        dado = {
            'livro': 'python3',
            'escritor': 'Glayton'
        }

        response = self.client.post(url_for('books.create_book'), json=dado)

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
        response = self.client.post(url_for('books.create_book'), json=dado)

        # import ipdb; ipdb.set_trace()

        self.assertEqual(esperado, response.json)

    def test_criar_deve_retornar_erro_quando_o_payload_contiver_a_chave_id(self):

        dado = {
            'livro': 'python3',
            'escritor': 'Glayton',
            'id': '1'

        }

        esperado = {'message': 'id must not be sent'}
        response = self.client.post(url_for('books.create_book'), json=dado)

        # import ipdb; ipdb.set_trace()

        self.assertEqual(esperado, response.json)


class TesteLer(TestFlaskBase):
    def teste_ler_deve_retornar_uma_query_vazia(self):
        self.create_user()
        token = self.create_token()
        from time import sleep
        #sleep(2)
        response = self.client.get(
            url_for('books.read_all_books'),
            headers=token
        )

        self.assertEqual([], response.json)

    def teste_ler_deve_retornar_uma_query_com_elemento_inserido(self):
        self.create_user()
        token = self.create_token()

        livro = {'escritor': 'glayton', 'livro': 'python3'}
        self.client.post(url_for('books.create_book'), json=livro)
        response = self.client.get(url_for('books.read_all_books'), headers=token)
        self.assertEqual(1, len(response.json))

    def teste_ler_deve_retornar_uma_query_com_elemento_solicitado_pelo_id(self):
        livro = {'escritor': 'glayton', 'livro': 'python3'}
        self.client.post(url_for('books.create_book'), json=livro)
        response = self.client.get(url_for('books.read_book', identificator=1))
        self.assertEqual(3, len(response.json))

    def teste_ler_deve_retornar_um_erro_se_o_id_solicitado_nao_existir(self):
        esperado = {'message': 'Book not found'}
        response = self.client.get(url_for('books.read_book', identificator=1))
        self.assertEqual(esperado, response.json)


class TesteAtualizar(TestFlaskBase):
    def teste_se_o_identificador_nao_for_encontrado_retorne_um_erro(self):
        esperado = {'message': 'response validation error'}
        json = {'escritor': 'glayton', 'livro': 'python3'}
        response = self.client.put(url_for('books.update', identificator=1), json=json)
        self.assertEqual(esperado, response.json)

    def teste_se_o_identificador_for_encontrado_retorne_livro_atualizado(self):
        esperado = json = {'escritor': 'glayton', 'livro': 'python3', 'id': 1}

        dado = {
            'livro': 'python2',
            'escritor': 'Glayton'
        }

        response = self.client.post(url_for('books.create_book'), json=dado)

        json = {'escritor': 'glayton', 'livro': 'python3'}

        response = self.client.put(url_for('books.update', identificator=1), json=json)
        self.assertEqual(esperado, response.json)


class TesteDeletar(TestFlaskBase):
    def teste_deletar_deve_retornar_deletado_se_nao_encontrar_registro(self):
        response = self.client.delete(url_for('books.delete_book', identificator=1))
        self.assertEqual('deletado', response.json)

    def teste_deletar_deve_retornar_deletado_se_encontrar_registro(self):
        dado = {
            'livro': 'python2',
            'escritor': 'Glayton'
        }

        response = self.client.post(url_for('books.create_book'), json=dado)
        response = self.client.delete(url_for('books.delete_book', identificator=1))
        self.assertEqual('deletado', response.json)

    def teste_deletar_deve_retornar_deletado_se_encontrar_todos_os_registros(self):
        dado = {
            'livro': 'python2',
            'escritor': 'Glayton'
        }

        lista = {'list': [1]}

        response = self.client.post(url_for('books.create_book'), json=dado)
        response = self.client.delete(url_for('books.delete_books'), json=lista)
        self.assertEqual('deletado', response.json)