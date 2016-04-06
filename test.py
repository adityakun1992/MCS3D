"""points = []
series.exposure_points = []
i=1
j=0
series.setOrigin(0, 0)
while i<=80:
	points.append([0,i*10000])
	points.append([0,-i*10000])
	points.append([i*10000,0])
	points.append([-i*10000,0])
	i += 20
series.appendCustom(points)

print series.exposure_points
series.preview()
stage.printSeries(series.exposure_points,1)"""

# import time
# import threading
#
# def func1():
#     t = threading.Thread(target=func2)
#     t.start()
#     print("Do stuff here")
# def func2():
#     time.sleep(10)
#     print("Do more stuff here")
#
# func1()
# print("func1 has returned")



#a = ['a', 'b', 'c', 'd']
#print 'x'.join(a)
#import os, subprocess
"""import Admin

if not Admin.isUserAdmin():
        Admin.runAsAdmin()
#import subprocess
#subprocess.call(['runas', '/user:Administrator', 'c:', 'cd/','cd C:/Program Files (x86)/Windows Kits/10/Tools/x64', 'devcon.exe restart *FTDIBUS*', 'pause'])
#os.system("c: & cd\ & cd C:/Program Files (x86)/Windows Kits/10/Tools/x64 & devcon.exe restart *FTDIBUS*")
#os.system("echo %cd%")

from subprocess import Popen
p = Popen("restartcom.bat")
stdout, stderr = p.communicate()"""
"""from Config import *
mcsHandle = SA_INDEX()
config = 0
x = c_int()
y = c_int()
moveinProgress = 0
Stopped = 0
Holding = 0
stageError = 0
status_command_dictionary = {0:'Stopped', 1:'Stepping', 2:'Scanning', 3:'Holding', 4:'Target',
                             5:'Move Delay', 6:'Calibrating', 6:'Target', 7:'Finding Ref', 8:'Opening'}
statusy=c_uint()
statusx=c_uint()
printing = 0
moving = 0
i=0
def ExitIfError(st):
    if st != SA_OK:
        handle_error(st)
while True:
    try:
        #ExitIfError(MCSlib.SA_InitSystems(0))
        print MCSlib.SA_GetPosition_S(mcsHandle,0,byref(y))
        #raise
        print "xyz"
        print MCSlib.SA_GetPosition_S(mcsHandle,1,byref(x))
        print x.value
        print MCSlib.SA_GotoPositionAbsolute_S(mcsHandle,0,0,60000)

        print MCSlib.SA_GotoPositionAbsolute_S(mcsHandle,1,0,60000)
    except:
        print "div by 0"
        i=1
        continue
    break"""

import Admin
import time
if not Admin.isUserAdmin():
        Admin.runAsAdmin()

while True:
    print "xyz"
    time.sleep(1)

