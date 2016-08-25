import pickle,sys
#from objecttohttp import pickling
import cherrypy, json

"""class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        s=sys.stdin.read().decode("string_escape")
        data = pickle.loads(s)
        #data = json.dumps({"current_percentage": 0, "current_point": 0, "noofpoints": 0, "point": [0,0], "msg": "Intialized, Not running"})
        return data
cherrypy.quickstart(HelloWorld())"""

class StringGeneratorWebService(object):
     exposed = True

     @cherrypy.tools.accept(media='text/plain')
     def GET(self):
         return cherrypy.session['mystring']

     def POST(self, length=8):
         data = pickle.load( open( "progress.p", "rb" ) )
         cherrypy.session['mystring'] = data
         return data

     def PUT(self, another_string):
         cherrypy.session['mystring'] = another_string

     def DELETE(self):
         cherrypy.session.pop('mystring', None)

conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    }
}
cherrypy.quickstart(StringGeneratorWebService(), '/', conf)