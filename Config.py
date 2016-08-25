import ctypes
from ctypes import *
import re
import os
import sys

if sys.platform.startswith('win') or sys.platform.startswith('cli'):

    # Default location on Windows XP and Windows 7
    # Name (and eventually path) of the library
    # Default on Windows is MCScontrol
    MCSlib = ctypes.cdll.LoadLibrary("MCSControl")
    
    
    
    
    #constant_file = os.path.join("H:","DevelopmentTools","eclipse","workspace","MCS3D","Constantlist.dat")
    constant_list = []
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/Constant_list.dat'):
        #Open empty file
        constant_file = open("Constant_list.dat",'w')
        # Full path of the NIDAQmx.h file
        dot_h_file = os.path.join("C:\\", "SmarAct", "MCS", "SDK", "include", "MCSControl.h")
        if dot_h_file is None or not os.path.exists(dot_h_file):
            raise (NotImplementedError, "Location of MCS library and include file unknown on %s" % (sys.platform))
        dot_h_file = open(dot_h_file,'r') #Open MCSControl.h file
        #regex for constants, #define...
        define = re.compile(r'\#define\s+(\S+)\s+(".*"|\S+)')
        for line in dot_h_file:
            m = define.match(line)
            if m:
                #groups stored in (). 1- name of constant, 2-value of constant
                name = m.group(1)
                value = m.group(2)
                constant_file.write(name+'\t'+value+'\n')
                try:
                    exec(name+'='+value)
                except NameError:
                    pass
                except SyntaxError:
                    pass
                else:
                    constant_list.append(name)
        dot_h_file.close()

    #if constant_list exists
    else:
        #open and read
        constant_file = open("Constant_list.dat",'r')
        define = re.compile(r'(\S+)\s+(".*"|\S+)')
        for line in constant_file:
            m = define.match(line)
            name = m.group(1)
            value = m.group(2)
            try:
                exec(name+'='+value)
            except NameError:
                pass
            except SyntaxError:
                pass
            else:
                constant_list.append(name)
    constant_file.close()
    #if not os.path.isfile
    
def handle_error(code):
    print ("MCS Error "+ str(code) +": " + constant_list[code+3])


#typedef aliases in header file
SA_STATUS = c_uint
SA_INDEX = c_uint
SA_PACKET_TYPE = c_uint


#SA_Packet structure defined in MCS Control.h
class SA_packet(ctypes.Structure):
    _fields_ = [("packetType", SA_PACKET_TYPE),
                ("channelIndex", SA_INDEX),
                ("data1", c_uint),
                ("data2", c_int),
                ("data3", c_int),
                ("data4", c_uint)]

SA_PACKET = SA_packet()