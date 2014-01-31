import logging
import datetime
import json

import webapp2
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import db

def coerce(value):
    SIMPLE_TYPES = (int, long, float, bool, basestring)
    if value is None or isinstance(value, SIMPLE_TYPES):
        return value
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    elif hasattr(value, 'to_dict'):    # hooray for duck typing!
        return value.to_dict()
    elif isinstance(value, dict):
        return dict((coerce(k), coerce(v)) for (k, v) in value.items())
    elif hasattr(value, '__iter__'):    # iterable, not string
        return map(coerce, value)
    else:
        raise ValueError('cannot encode %r' % value)

class TeamEntity(ndb.Model):
    name = ndb.StringProperty()
    colour = ndb.StringProperty()
    score = ndb.IntegerProperty(default=0)
    
    @classmethod
    def fromTuple(cls, teamTuple):
        return TeamEntity(name=teamTuple[0], colour=teamTuple[1])
        
        

class GameEntity(ndb.Model):
#     def to_dict(self):
#         output = {}
#         for key, prop in self._properties.iteritems():
#             value = coerce(getattr(self, key))
#             if value is not None:
#                 output[key] = value
#         return output
    # Date
    date = ndb.DateTimeProperty(auto_now_add=True)
    # Location
    location = ndb.GeoPtProperty()
    # Team #1 colour, score
    # Team #2 colour, score
    teams = ndb.StructuredProperty(TeamEntity, repeated=True)
    # Game start time
    start_time = ndb.TimeProperty()
    description = ndb.StringProperty()
    type = ndb.IntegerProperty()
    age_category = ndb.IntegerProperty(default=0)
    gender_category = ndb.IntegerProperty(default=0)
    # MAYBE
    # Unique Observers
    # Unique Contributors
    def to_dict(self):
        ret = ndb.Model.to_dict(self, exclude=['date', 'start_time', 'location'])
        return ret

    def toJson(self):
        return json.dumps(self.to_dict())

# class Game(object):
#     ''' Wrapper class for GameEntity that will incorporate the Search API
#     functionality
#     '''
#     def __init__(self, newgame_json):
#         # Data checking
#         # Do I want to do any verification of "start_time"?
#         
#         ng = GameEntity(location=ndb.GeoPt("%s, %s" % (newgame_json['location']['lat'], newgame_json['location']['lon'])), 
#                         teams=[TeamEntity.fromTuple(newgame_json['teams'][0]),
#                                TeamEntity.fromTuple(newgame_json['teams'][1])],
#                         start_time=datetime.time(newgame_json['start_time']),
#                         description=newgame_json['description'])
#         ng.put()
#         self.game_entity = ng


class GameDocument(object):
    '''Encapsulates the document fields of a Game'''
    _INDEX_NAME = 'GAMES'
    #getGeoPt
    #setGeoPt
    #getOpponents
    #setOpponents
    def __init__(self):
        pass
    
    @classmethod
    def getIndex(cls):
        return search.Index(name=cls._INDEX_NAME)

    @classmethod
    def getDoc(cls, doc_id):
        """Return the document with the given doc id. One way to do this is via
        the get_range method, as shown here.  If the doc id is not in the
        index, the first doc in the index will be returned instead, so we need
        to check for that case."""
        if not doc_id:
            return None
        try:
            index = cls.getIndex()
            response = index.get_range(
                  start_id=doc_id, limit=1, include_start_object=True)
            if response.results and response.results[0].doc_id == doc_id:
                return response.results[0]
            return None
        except search.InvalidRequest: # catches ill-formed doc ids
            return None

    @classmethod
    def removeDocById(cls, doc_id):
        """Remove the doc with the given doc id."""
        try:
            cls.getIndex().delete(doc_id)
        except search.Error:
            logging.exception("Error removing doc id %s.", doc_id)

    @classmethod
    def add(cls, documents):
        """wrapper for search index add method; specifies the index name."""
        try:
            return cls.getIndex().put(documents)
        except search.Error:
            logging.exception("Error adding documents.")
    

class GetGames(webapp2.RequestHandler):
    def get(self):
        self.response.write('<implement games list>')
        # Output to json
        pass

class CreateGame(webapp2.RequestHandler):
    def post(self):
        '''Handles the post request accepting a json string formatted by the client

        '''
        #logging.info('')
        ng_string = self.request.POST['newgame']
        if ng_string:
            newgame_json = json.loads(ng_string)
            # Check 'ng' app version, See #19
            
            # Create Game Model
            ng = GameEntity(location=ndb.GeoPt("%s, %s" % (newgame_json['location']['lat'], newgame_json['location']['lon'])), 
                            teams=[TeamEntity.fromTuple(newgame_json['teams'][0]),
                                   TeamEntity.fromTuple(newgame_json['teams'][1])],
                            start_time=datetime.datetime.strptime(newgame_json['start_time'], "%H:%M").time(),
                            description=newgame_json['description'],
                            type=newgame_json['type'])
            ng.put()
            # return response with new_game datastore ID.  Possibly json version
            # of game as well
            self.response.headers['Content-Type'] = 'application/json'

            self.response.write(json.dumps(ng.to_dict()))
        else:
            # Error.  This handler shouldn't be called without a proper
            # json object to define a new game
            logging.error("Error in CreateGame: %s", 'No defined json')

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