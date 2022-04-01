from flask import url_for
from tests.flask_base_test import TestFlaskBase


class TestUser(TestFlaskBase):
    def test_api_deve_registrar_usuario_na_base(self):
        user = {
            'username': 'test',
            'password': '1234'
        }

        esperado = {
            'id': 1,
            'username': 'test',
            'password': '1234'
        }

        response = self.client.post(url_for('users.register'), json=user)

        self.assertEqual(201, response.status_code)

        self.assertEqual(esperado['username'], response.json['username'])
