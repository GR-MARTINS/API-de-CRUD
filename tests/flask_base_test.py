from unittest import TestCase
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
