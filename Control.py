from Config import *
import time
#from PyDAQmx import *
from subprocess import Popen
import datetime
import json
import pickle
import numpy as np
#import objecttohttp

def ExitIfError(st):
    if st != SA_OK:
        handle_error(st)
    else:
        print "Connectection Successful"


class SmarAct:
    def __init__(self, config):
        self.jsonobj = None
        self.mcsHandle = SA_INDEX()
        self.x = c_int()
        self.y = c_int()
        self.statusy=c_uint()
        self.statusx=c_uint()
        self.msg = "Intitialized"


        self.reconnecting = False
        self.config = config
        self.moveinProgress = 0
        self.Stopped = 0
        self.Holding = 0
        self.stageError = 0
        self.status_command_dictionary = {0:'Stopped', 1:'Stepping', 2:'Scanning', 3:'Holding', 4:'Target', 
                                          5:'Move Delay', 6:'Calibrating', 7:'Finding Ref', 8:'Opening'}
        self.printing = 0
        self.moving = 0
        #print MCSlib.SA_GetPosition_S(self.mcsHandle,0,byref(self.y))
        ExitIfError(MCSlib.SA_InitSystems(config))

        self.tries = 0
        self.current_point = 0
        self.point = 0
        self.percentage = 0
        self.msg = 0


        #initialize the NI-DAQmx
        """try:
            self.taskHandle = TaskHandle()
            self.write = int32()
            self.writedata = (numpy.ones((1000,), dtype=numpy.uint8))
            DAQmxCreateTask("",byref(self.taskHandle))
            
            #Shutter Actuator is connected to P0.0
            DAQmxCreateDOChan(self.taskHandle,"Dev1/port0/line0","",DAQmx_Val_ChanForAllLines)
            #DAQmxCfgSampClkTiming(taskHandle,"",1000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)
            DAQmxStartTask(self.taskHandle)
            #DAQmxWriteDigitalLines(self.taskHandle1, 1000, 20, 10.0, 20, self.writedata*0, byref(self.write), None)
        except DAQError as err:
            pass
        try:
            self.taskHandle_x = TaskHandle()
            self.taskHandle_y = TaskHandle()
            self.write = int32()
            self.writedata = (numpy.ones((1000,), dtype=numpy.float64))
            DAQmxCreateTask("",byref(self.taskHandle_x))
            DAQmxCreateTask("",byref(self.taskHandle_y))
            
            #Flexure X-axis is connected to AO0
            DAQmxCreateAOVoltageChan(self.taskHandle_x,"Dev1/ao0","",0.0,5.0,DAQmx_Val_Volts,None)
            #Flexure X-axis is connected to AO1
            DAQmxCreateAOVoltageChan(self.taskHandle_y,"Dev1/ao1","",0.0,5.0,DAQmx_Val_Volts,None)
            
            DAQmxStartTask(self.taskHandle_x)
            DAQmxStartTask(self.taskHandle_y)
        except DAQError as err:
            pass
            #print "DAQmx Error: %s"%err

        #MCSlib.SA_ReleaseSystems(byref(buffsize))"""

    def initializeStage(self):
        ExitIfError(MCSlib.SA_InitSystems(self.config))

    def reconnect(self):
        self.reconnecting = True
        if self.tries==0:
            self.lost_time = str(datetime.datetime.now().time())
            self.msg = "Lost connection to stage at " + self.lost_time
        self.tries += 1
        self.generate_json()
        p = Popen("restartcom.bat")
        time.sleep(5)
        if MCSlib.SA_InitSystems(self.config) == SA_OK:
            self.msg = "Lost connection to stage at " + self.lost_time + " and regained connection"
            self.tries = 0
            self.generate_json()
        else:
            self.msg = "Lost connection to stage at " + self.lost_time + " \n Tries: " + str(self.tries)
            self.generate_json()
        time.sleep(5)

    def __str__(self):
        self.getPosition()
        self.getStatus()
        return '''
    Current Settings:
        Mode of Operation:       {} sync or async
        Current Position:        {}-->x  {}-->y
        X-Status:                {}
        Y-Status:                {}
    '''.format(self.config, self.x, self.y, 
               self.status_command_dictionary[self.statusx.value], self.status_command_dictionary[self.statusy.value])

    def getStatus(self):
        MCSlib.SA_GetStatus_S(self.mcsHandle,0,byref(self.statusy))
        MCSlib.SA_GetStatus_S(self.mcsHandle,1,byref(self.statusx))
        #print self.statusx.value, self.statusy.value
        return [self.statusx.value, self.statusy.value]

    def wait(self):
        history=[]
        while True:
            self.getStatus()
            #print self.getPosition(),self.getStatus(),"xyz"
            history.extend([self.getPosition()])
            if len(history)>10:
                #print history
                if ((not history or [history[0]]*len(history) == history)):
                    del history
                    self.reconnect()
                    break
                history=[]
            if self.statusx.value == 3 and self.statusy.value == 3:
                print "reached"
                break
        


    def getPosition(self):
        #buffsize=c_int(10)
        #ExitIfError(MCSlib.SA_InitSystems(0))
        MCSlib.SA_GetPosition_S(self.mcsHandle,0,byref(self.y))
        MCSlib.SA_GetPosition_S(self.mcsHandle,1,byref(self.x))
        return [self.x.value, self.y.value]


    def moveRelative(self, xpos, ypos):
        self.dx, self.dy = self.dx+xpos, self.dy+ypos
        #self.moving = 1
        reached =0
        while True:
            try:
                MCSlib.SA_GotoPositionRelative_S(self.mcsHandle, 1, xpos, 60000)
                MCSlib.SA_GotoPositionRelative_S(self.mcsHandle, 0, ypos, 60000)
                history=[]
                while True:
                    self.getStatus()
                    #print self.getPosition(),self.getStatus(),"xyz"
                    history.extend([self.getPosition()])
                    if len(history)>20:
                        #print history
                        if ((not history or [history[0]]*len(history) == history)):
                            del history
                            raise
                        history=[]
                    if self.statusx.value == 3 and self.statusy.value == 3:
                        reached = 1
                        break
                break
            except:
                self.reconnect()
        self.statusx.value=self.statusy.value=0
        self.dx, self.dy = xpos, ypos
        #self.wait()

    def move(self, xpos=-6500000, ypos=44000000):
        #if self.getStatus()
        print xpos,ypos
        reached =0
        while True:
            try:
                MCSlib.SA_GotoPositionAbsolute_S(self.mcsHandle,0,ypos,60000)
                MCSlib.SA_GotoPositionAbsolute_S(self.mcsHandle,1,xpos,60000)
                history=[]
                while True:
                    self.getStatus()
                    #print self.getPosition(),self.getStatus(),"xyz"
                    history.extend([self.getPosition()])
                    if len(history)>20:
                        if ((not history or [history[0]]*len(history) == history)):   #if all history points are the same
                            del history
                            raise    
                        history=[]
                    if self.statusx.value == 3 and self.statusy.value == 3:
                        reached = 1
                        break
                break
            except:
                #a disconnect has occured-need to reset USB
                self.reconnect()
        self.statusx.value=self.statusy.value=0
        self.dx, self.dy = xpos, ypos



    def flex_move(self, x, y):
        try:
            #change voltage for x-axis on flexure stage
            DAQmxWriteAnalogF64(self.taskHandle_x, 1000, 20, 10.0, 20, self.writedata*(5*(x+3750)/7500), byref(self.write), None)
            #change voltage for Y-axis on flexure stage
            DAQmxWriteAnalogF64(self.taskHandle_y, 1000, 20, 10.0, 20, self.writedata*(5*(y+3750)/7500), byref(self.write), None)
        except DAQError as err:
            print "DAQmx Error: %s"%err



    #not using flexure ---- shutter connected to analog
    def expose_auto(self, t):
        try:
            #self.wait()
            DAQmxWriteAnalogF64(self.taskHandle_x, 1000, 20, 10.0, 20, self.writedata*0, byref(self.write), None)
            time.sleep(t)
            DAQmxWriteAnalogF64(self.taskHandle_x, 1000, 20, 10.0, 20, self.writedata*5, byref(self.write), None)
            #DAQmxWriteDigitalLines (self.taskHandle, 1000, 20, 10.0, 20, self.writedata*(not self.printing), byref(self.write), None)
        except DAQError as err:
            print "DAQmx Error: %s"%err

    def expose_on(self):
        try:
            #self.wait()
            DAQmxWriteAnalogF64(self.taskHandle_x, 1000, 20, 10.0, 20, self.writedata*0, byref(self.write), None)
            
            #DAQmxWriteDigitalLines (self.taskHandle, 1000, 20, 10.0, 20, self.writedata*(not self.printing), byref(self.write), None)
        except DAQError as err:
            print "DAQmx Error: %s"%err

    def expose_off(self):
        try:
            #self.wait()
            DAQmxWriteAnalogF64(self.taskHandle_x, 1000, 20, 10.0, 20, self.writedata*5, byref(self.write), None)
            
            #DAQmxWriteDigitalLines (self.taskHandle, 1000, 20, 10.0, 20, self.writedata*(not self.printing), byref(self.write), None)
        except DAQError as err:
            print "DAQmx Error: %s"%err
            
    #flexure connected ---- shutter controlled on digital line
    """def expose(self,t):
        try:
            self.wait()
            DAQmxWriteDigitalLines (self.taskHandle, 1000, 20, 10.0, 20, self.writedata, byref(self.write), None)
            time.sleep(t)
            DAQmxWriteDigitalLines(self.taskHandle, 1000, 20, 10.0, 20, self.writedata*0, byref(self.write), None)
        except DAQError as err:
            print "DAQmx Error: %s"%err
            """

    def printSeries(self,series,dosage):
        i=0
        self.tries = 0
        self.current_point = 0
        self.point = [series[0]]
        self.percentage = 0
        self.max_points = len(series)
        for item in series:
            print "Now moving to :" + " " + str(item)
            self.msg = "Print process is in operation. There are no issues currently."
            self.point = [item[0]/1000000,item[1]/1000000]
            self.percentage = (self.current_point/len(series))*100
            done = np.array(np.array(series[:self.current_point])/1000000)
            yet = np.array(np.array(series[self.current_point:])/1000000)
            self.generate_json()
            self.generatePoint_json(done, yet)
            self.move(item[0],item[1])
            print "Reached"
            print "Exposing for " + str(dosage[i]) + " seconds"
            self.expose_auto(dosage[i])
            self.current_point += 1
            i+=1
        self.msg = "Process Completed"
        self.generate_json()
        self.generatePoint_json(done, yet)


    def generate_json(self):
        self.jsonobj = json.dumps({"current_percentage": self.percentage, "current_point": self.current_point, "noofpoints": self.max_points, "point": self.point, "msg": self.msg})
        s = pickle.dump(self.jsonobj, open( "progress.p", "wb" ) )

    def generatePoint_json(self, done, yet):
        jsonpoints = json.dumps({"done": done.tolist(), "yet":yet.tolist()})
        s = pickle.dump( jsonpoints, open( "points.p", "wb" ) )


    def release(self):
        buffsize=c_int(10)
        MCSlib.SA_ReleaseSystems(byref(buffsize))

    def __del__(self):
        buffsize=c_int(10)
        MCSlib.SA_ReleaseSystems(byref(buffsize))
        # DAQmx Stop Cod
        """DAQmxStopTask(self.taskHandle)
        DAQmxClearTask(self.taskHandle)
        DAQmxStopTask(self.taskHandle_x)
        DAQmxClearTask(self.taskHandle_x)
        DAQmxStopTask(self.taskHandle_y)
        DAQmxClearTask(self.taskHandle_y)"""
