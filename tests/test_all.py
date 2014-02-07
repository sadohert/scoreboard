'''
Created on Jan 17, 2014

@author: sadohert
'''
import unittest2
import webapp2
import json

from google.appengine.ext import testbed

from google.appengine.ext import ndb
from google.appengine.ext import db
# from the app main.py
import main

class TestGeneric(unittest2.TestCase):
    @unittest2.skip("Root handler in flux")
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
    def setUp(self):
        # GAE Local testing boilerplate code
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
                        
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
              "start_time": "17:00",
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
        body_dict = json.loads(response.body)
        self.assertEqual(body_dict['start_time'], "17:00")
        
        # Verify response.body
        
            