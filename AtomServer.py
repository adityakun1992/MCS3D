import pickle,sys
#from objecttohttp import pickling
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

"""class StringGeneratorWebService(object):
     exposed = True

     @cherrypy.tools.accept(media='application/json')
     def GET(self):
         return cherrypy.session['myjson']

     def POST(self, length=8):
         data = pickle.load( open( "progress.p", "rb" ) )
         cherrypy.session['myjson'] = data
         return data

     def PUT(self, another_string):
         cherrypy.session['myjson'] = another_string

     def DELETE(self):
         cherrypy.session.pop('myjson', None)

     def index(self, artist, title):
         return cherrypy.session['myjson']
cherrypy.server.socket_host = '192.168.1.10'
cherrypy.server.socket_port = 8080
conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    }
}
cherrypy.quickstart(StringGeneratorWebService(), '/', conf)"""