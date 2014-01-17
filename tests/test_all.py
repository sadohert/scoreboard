'''
Created on Jan 17, 2014

@author: sadohert
'''
import unittest2
import webapp2

# from the app main.py
import main

class TestHandlers(unittest2.TestCase):
    def test_root(self):
        # Build a request object passing the URI path to be tested.
        # You can also pass headers, query arguments etc.
        request = webapp2.Request.blank('/')
        # Get a response for that request.
        response = request.get_response(main.app)
        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'Hello, webapp2! STU!!')