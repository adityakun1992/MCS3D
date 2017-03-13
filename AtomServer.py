import pickle,sys
import cherrypy, json

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        #s=sys.stdin.read().decode("string_escape")
        data = pickle.load( open( "progress.p", "rb" ) )
        #data = json.dumps({"current_percentage": 0, "current_point": 0, "noofpoints": 0, "point": [0,0], "msg": "Intialized, Not running"})
        return data

    @cherrypy.expose
    def points(self):
        #s=sys.stdin.read().decode("string_escape")
        data = pickle.load( open( "points.p", "rb" ) )
        #data = json.dumps({"current_percentage": 0, "current_point": 0, "noofpoints": 0, "point": [0,0], "msg": "Intialized, Not running"})
        return data

cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'} )
cherrypy.quickstart(HelloWorld())