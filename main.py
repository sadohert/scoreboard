import webapp2
from google.appengine.ext import ndb

class Game(ndb.Model):
    # Date
    date = ndb.DateTimeProperty(auto_now_add=True)
    # Location
    location = ndb.GeoPtProperty()
    # Team #1 colour, score
    # Team #2 colour, score
    
    
    # MAYBE
    # Unique Observers
    # Unique Contributors
    pass

class CreateGame(webapp2.RequestHandler):
    def put(self):
        # tEST COMMENT
        pass

class ScoreboardApp(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2! STU!!')

routes = [
    (r'/', 'main.ScoreboardApp'),
    (r'/newgame', 'main.CreateGame'), # TODO Request create game "PUT"
    
    # TODO Request game list "GET"
    # TODO Request game update "GET"

     
]

app = webapp2.WSGIApplication(routes=routes, debug=True)