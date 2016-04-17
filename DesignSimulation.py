import os, re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import math


class design:
    def __init__(self):
        self.file_path=os.path.dirname(os.path.realpath(__file__)) + '/ExposureFiles/'
        self.mask = None
        self.exposure_points=[]
        self.dosage=[]
        self.origin = [0,0]
    
    def name(self, name):
        self.name = name
        if (os.path.exists(self.file_path + self.name + '.txt')):
            print "Importing data from existing file..."
            self.readData()
            self.exists = True
            print "Success"
        else:
            self.exposure_points = []
            self.exists = False


    def gengrid(self, pitch_x, pitch_y):
        self.grid = []
        unique=[]
        if len(self.mask)==4:
            i = (self.mask[1])*1000000
            j = (self.mask[3])*1000000
            while i <= 0:
                while j <= 0:
                    self.grid.append([i+(self.origin[0]*1000000), j+(self.origin[1]*1000000)])
                    self.grid.append([i+(self.origin[0]*1000000), -j+(self.origin[1]*1000000)])
                    self.grid.append([-i+(self.origin[0]*1000000), -j+(self.origin[1]*1000000)])
                    self.grid.append([-i+(self.origin[0]*1000000), j+(self.origin[1]*1000000)])
                    j += (pitch_x*1000000)
                i += (pitch_y*1000000)
                j = (self.mask[3])*1000000
            #unique[:]=[x for x in self.grid if x not in unique]
            #self.grid = unique
            self.exposure_points.extend(self.grid)
        elif(len(self.mask)==1):
            i = -50*1000000
            j = -60*1000000

            while i <= 0:
                while j <= 0:
                    self.grid.append([i+(self.origin[0]*1000000), j+(self.origin[1]*1000000)])
                    self.grid.append([i+(self.origin[0]*1000000), -j+(self.origin[1]*1000000)])
                    self.grid.append([-i+(self.origin[0]*1000000), -j+(self.origin[1]*1000000)])
                    self.grid.append([-i+(self.origin[0]*1000000), j+(self.origin[1]*1000000)])
                    j += (pitch_x*1000000)
                i += (pitch_y*1000000)
                j = -60*1000000

            #unique[:]=[x for x in self.grid if x not in unique]
            #self.grid = unique
            #for item in self.grid:
                #print str(item)+ "\t"+str(math.sqrt(((item[0]-self.origin[0]*1000000)**2)  +  ((item[1]-self.origin[1]*1000000)**2)  ))+"\t" +str(math.sqrt(((item[0]-self.origin[0]*1000000)**2)  +  ((item[1]-self.origin[1]*1000000)**2)  ) >= (self.mask[0]*1000000))
                #if (math.sqrt(((X[0]-self.origin[0]*1000000)**2)  +  ((X[1]-self.origin[1]*1000000)**2)  ) > (self.mask[0]*1000000)):
            self.grid[:] = [x for x in self.grid if (math.sqrt(((x[0]-self.origin[0]*1000000)**2)  +  ((x[1]-self.origin[1]*1000000)**2)  ) <= (self.mask[0]*1000000))]
            for item in self.grid:
                if self.grid.count(item)>1:
                    print "xyz"
            self.exposure_points.extend(self.grid)
            #print self.exposure_points





    def readData(self):
        exposurefile=open(os.path.join(self.file_path+self.name + '.txt'), 'r')
        entries=[]      #reading from file
        exposure_points = []    #list
        for line in exposurefile:
            entries.append(re.findall((r'([-+]?\d+)\s*([-+]?\d+)'), line))
        #convert to a proper 2 dimensional array/list
        for item in entries:
            for subitem in item:
                exposure_points.append([float(subitem[0]),float(subitem[1])])
        self.exposure_points = exposure_points
        exposurefile.close()


    def circle(self,r,n):
        circle = mpatches.Circle(grid[0], 0.1, ec="none")
        patches.append(circle)
        label(grid[0], "Circle")
        # r=r*1000000
        # perimeter=[(math.cos(2*math.pi/n*x)*r+self.origin[0],math.sin(2*math.pi/n*x)*r+self.origin[1]) for x in xrange(0,(n*2))]
        # self.exposure_points.extend(perimeter)
        # for item in perimeter:
        #     print str(item)


    def disc(self,r,n):
        r=r*1000000
        perimeter=[(math.cos(2*math.pi/n*x)*r+self.origin[0],math.sin(2*math.pi/n*x)*r+self.origin[1]) for x in xrange(0,(n*2))]
        self.exposure_points.extend(perimeter)
        for item in perimeter:
            print str(item)



    def preview(self):
        fig = plt.figure(2)
        fig.canvas.set_window_title('Preview Window')
        plt.figure(2)
        """if self.mask:
            plt.plot([self.mask[0]+self.origin[0],self.mask[0]+self.origin[0]],[self.mask[2]+self.origin[1],self.mask[3]+self.origin[1]], 'black')
            plt.plot([self.mask[0]+self.origin[0],self.mask[1]+self.origin[0]],[self.mask[3]+self.origin[1],self.mask[3]+self.origin[1]], 'black')
            plt.plot([self.mask[1]+self.origin[0],self.mask[1]+self.origin[0]],[self.mask[3]+self.origin[1],self.mask[2]+self.origin[1]], 'black')
            plt.plot([self.mask[1]+self.origin[0],self.mask[0]+self.origin[0]],[self.mask[2]+self.origin[1],self.mask[2]+self.origin[1]], 'black')"""

        xdata,ydata=[],[]
        #print self.exposure_points
        for item in self.exposure_points:
            xdata.append(item[0]/float(1000000))
            ydata.append(item[1]/float(1000000))
        plt.plot(xdata,ydata,'ro',self.origin[0],self.origin[1],'bs')
        #plt.plot()
        #plt.axis()
        plt.axis([-50, 50, -60, 60],'equal')
        plt.grid()
        plt.show()
     
    """def saving(self):
        if not self.shape.exists:
            self.save = raw_input('Would you like to save this pattern?(y/n)\n')
            if self.save == 'y':
                self.writeData()"""
    
    
    def masking(self, x, y=None):
        if y==None:
            self.mask=[x]
        else:
            self.mask = [(x/2),(-x/2), (y/2),(-y/2)]
        
    def setOrigin(self, x, y):
        self.origin = [x,y]
        
    def relativeOrigin(self, x, y):
        self.origin = [self.origin[0]+x, self.origin[1]+y]
        
    def resetOrigin(self):
        self.origin = [0, 0]
        
    def appendPoints(self):
        for item in self.pattern:
            self.exposure_points.append([item[0]+self.origin[0], item[1]+self.origin[1]])
    
    def appendCustom(self,points):
        for item in points:
            self.exposure_points.append([item[0]+self.origin[0], item[1]+self.origin[1]])

    """def repeat(self, pitch_x, pitch_y=0):
        if self.wafer_size == None:
            print "Error: Assisgn a Wafer Size First!!!"
        if pitch_y == 0:
            pitch_y = pitch_x
        dose_series=[]
        print min(self.exposure_points)
        print max(self.exposure_points)"""



    def createShape(self):
        data = raw_input("Enter the list of coordinates:\n Eg:[0,0][46,-14][-4.5,-31]\n")
        data = re.split('([-+]?\d+[\.*\d+]*)\s*', data)
        print data
        index = 0
        self.pattern=[]
        for item in data:
            try:
                if isinstance( float(item), ( int, long, float ) ):
                    self.pattern.append(float(item))
                    index += 1
            except ValueError:
                pass
        index = 0
        for item in self.pattern:
            if index % 2 == 1:
                self.pattern[index-1] = [self.pattern[index-1], self.pattern[index]]
                self.pattern[index] = None
            index += 1
        for item in self.pattern:
            if item == None:
                del self.pattern[self.pattern.index(None)]
        """for item in self.pattern:
            self.exposure_points.append([item[0]+self.origin[0], item[1]+self.origin[1]])"""


    def writeData(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        if self.exists == False:
            exposurefile = open(os.path.join(self.file_path+self.name+'.txt'), 'w')
        else:
            prompt = raw_input("File with same name exists. Overwrite?(y/n)")
            if prompt == 'y':
                exposurefile = open(os.path.join(self.file_path+self.name+'.txt'), 'w')
            else:
                exposurefile = open(os.path.join(self.file_path+self.name+'(1).txt'), 'w')
        for item in self.exposure_points:
            exposurefile.write("%s\t"% item[0])
            exposurefile.write("%s\n"% item[1])
        exposurefile.close()

"""series = design("xyz")
series.createShape()
series.appendPoints()
series.setOrigin(15, -7)
series.createShape()
series.appendPoints()
series.showPreview()
series.writeData()"""
