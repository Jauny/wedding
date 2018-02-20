import unittest
from app import app


class ViewsTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
