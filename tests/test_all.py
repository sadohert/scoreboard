'''
Created on Jan 17, 2014

@author: sadohert
'''
import unittest2
import webapp2
import json

# from the app main.py
import main

class TestGeneric(unittest2.TestCase):
    def test_root(self):
        # Build a request object passing the URI path to be tested.
        # You can also pass headers, query arguments etc.
        request = webapp2.Request.blank('/')
        # Get a response for that request.
        response = request.get_response(main.app)
        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'Hello, webapp2! STU!!')

class TestGameCreation(unittest2.TestCase):
        
    def test_basic(self):
        '''Basic first test of handler that doesn't implement 'GET'
        '''
        request = webapp2.Request.blank('/newgame')
        # Get a response for that request.
        response = request.get_response(main.app)
        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 405)
        
    def test_newGame(self):
        ng_json = '''
            {
              "version": "0", 
              "start_time": "19:00",
              "description": "League play between U13 boys team", 
              "age_category": 3,
              "gender_category": 0, 
              "type": 0, 
              "location": {
                "lat": 50, 
                "lon": 120
              }, 
              "teams": [
                [
                  "Waterloo", 
                  "yellow"
                ], 
                [
                  "Kitchener", 
                  "green"
                ]
              ]
            }
        '''
        ng_dict = {}
        ng_dict['newgame'] = json.dumps(json.loads(ng_json))
        
        post_request = webapp2.Request.blank('/newgame', POST=ng_dict)

        # Get a response for that request.
        response = post_request.get_response(main.app)
        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        
        # Verify response.body
        
            