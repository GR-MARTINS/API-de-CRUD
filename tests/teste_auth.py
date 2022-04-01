from flask import url_for
from tests.flask_base_test import TestFlaskBase


class TestLogin(TestFlaskBase):
    def teste_deve_gerar_um_token(self):
        self.create_user()
        login = self.client.post(url_for('login.login'), json=self.user)

        esperado=['access_token', 'message', 'refresh_token']

        self.assertEqual(esperado,list(login.json.keys()))