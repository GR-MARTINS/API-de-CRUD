from flask import url_for
from tests.flask_base_test import TestFlaskBase


class TestLogin(TestFlaskBase):
    def teste_deve_gerar_um_token(self):
        self.create_user()
        login = self.client.post(url_for('login.login'), json=self.user)

        esperado = ['access_token', 'message', 'refresh_token']

        self.assertEqual(esperado, list(login.json.keys()))

    def teste_login_deve_retornar_um_erro(self):
        user = {
            'password': '1234',
            'username': 'a'
        }
        login = self.client.post(url_for('login.login'), json=user)

        esperado = {'message': 'Deu ruim! credenciais inválidas'}

        self.assertEqual(esperado, login.json)
