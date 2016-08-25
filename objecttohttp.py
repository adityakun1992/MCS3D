import json
import pickle, subprocess
import datetime
#from GUI import stage
#print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
#print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}], sort_keys=True, indent=4))
#current_time = datetime.datetime.now().time()
#print current_time

def pickling():
    if stage.jsonobj != None:
        pickleobj = pickle.dump(stage.jsonobj)
    else:
    data = json.dumps({"current_percentage": 0, "current_point": 0, "noofpoints": 0, "point": [0,0], "msg": "Intialized, Not running"})
    s = pickle.dump( data, open( "progress.p", "wb" ) )