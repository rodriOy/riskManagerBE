import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_predict(self):
        response = self.client.post('/predict', json={'text': 'Hola mundo'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.json)

    def test_submit(self):
        response = self.client.post('/submit', data={'mercaderiaId': '123', 'valor': '456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
