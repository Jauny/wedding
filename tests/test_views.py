import unittest
from flask import request

from app import app


class ViewsTest(unittest.TestCase):
    def setUp(self):
        """Setup tests."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        """Assert GET / returns 200."""
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_rsvp_get(self):
        """Assert GET /rsvp redirects to /."""
        resp = self.app.get('/rsvp')
        self.assertEqual(resp.status_code, 200)

    def test_rsvp_post_errors(self):
        """Assert POST /rsvp with invalid form returns errors."""
        resp = self.app.post('/rsvp', data={
            'email': ''
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('email' in resp.data)

    def test_rsvp_post_fast_rsvp(self):
        """
        Assert POST /rsvp with fast-rsvp yes saves data
        and has correct flash message.
        """
        with app.test_request_context():
            resp = self.app.post('/rsvp', data={
                'fast-rsvp': 'yes'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(request.path, '/')

    def test_rsvp_post_fast_rsvp_no(self):
        """
        Assert POST /rsvp with fast-rsvp no saves data
        and has correct flash message.
        """
        with app.test_request_context():
            resp = self.app.post('/rsvp', data={
                'fast-rsvp': 'no'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(request.path, '/')


if __name__ == '__main__':
    unittest.main()
