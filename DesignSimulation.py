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
        self.exposure_points=[]
        self.dosage=[]
        self.exists = False
        self.origin = [0,0]
        self.mask_size=None
        self.small_num = math.pow(10,-6)
        print self.small_num

    def name(self, name):
        self.name = name

        if (os.path.exists(self.file_path + self.name + '.txt')):
            if self.exposure_points == []:

                imp = raw_input("Import data from existing file?(y/n):")
                if imp == 'y':
                    self.readData()
                self.exists = True
                print "Success"
        else:
            self.exists = False

    def gengrid(self,pitch_x,pitch_y):
        grid=[]
        s=1000000       #scale
        #smallnum to include the end point(in arange) but not add any more points
        small_num = math.pow(10,-10)

        if len(self.wafer)==4:
            x=np.arange(0,self.wafer[1]+small_num,pitch_x)*s
            x=np.append(np.arange(0-pitch_x,self.wafer[0]-small_num,-pitch_x)*s,x)
            y=np.arange(0,self.wafer[3]+small_num,pitch_y)*s
            y=np.append(np.arange(0-pitch_y,self.wafer[2]-small_num,-pitch_y)*s,y)
            #sort to make prints with short movements
            x=np.sort(x,kind='quicksort')
            y=np.sort(y,kind='quicksort')
            print x,y
            for i in x:
                for j in y:
                    grid.append([int(i),int(j)])

        elif len(self.wafer)==1:
            x=np.arange(0,50+small_num,pitch_x)*s
            x=np.append(np.arange(0-pitch_x,-50-small_num,-pitch_x)*s,x)
            y=np.arange(0,60+small_num,pitch_y)*s
            y=np.append(np.arange(0-pitch_y,-60-small_num,-pitch_y)*s,y)
            x=np.sort(x,kind='quicksort')
            y=np.sort(y,kind='quicksort')
            print x,y
            for i in x:
                for j in y:
                    grid.append([i,j])
            #eliminate extra points and confine within radius-distance formula
            grid[:] = [x for x in grid if (math.sqrt(((x[0])**2)  +  ((x[1])**2)  ) <= (self.wafer[0]*1000000))]
        print grid


        if self.origin != [0,0]:
            for i in range(len(grid)):
                grid[i]=[grid[i][0]+(self.origin[0]*s),grid[i][1]+(self.origin[1]*s)]
        self.exposure_points.extend(grid)
        print self.exposure_points
    """def gengrid(self, pitch_x, pitch_y):
        grid = []
        unique=[]
        s=1000000
        if len(self.wafer)==4:
            i = (self.wafer[1])*1000000
            j = (self.wafer[3])*1000000
            while i <= 0:
                while j <= 0:
                    grid.append([i+(self.origin[0]*s), j+(self.origin[1]*s)])
                    grid.append([i+(self.origin[0]*s), -j+(self.origin[1]*s)])
                    grid.append([-i+(self.origin[0]*s), -j+(self.origin[1]*s)])
                    grid.append([-i+(self.origin[0]*s), j+(self.origin[1]*s)])
                    j += (pitch_x*1000000)
                i += (pitch_y*1000000)
                j = (self.wafer[3])*1000000
            #unique[:]=[x for x in self.grid if x not in unique]
            #self.grid = unique
            self.exposure_points.extend(self.grid)


        elif(len(self.wafer)==1):
            i=0
            j=0

            while i <= 50:
                while j <= 60:
                    grid.append([(i+self.origin[0])*s, (j+self.origin[0])*s])
                    grid.append([(i+self.origin[0])*s, (-j+self.origin[0])*s])
                    grid.append([(-i+self.origin[0])*s, (-j+self.origin[0])*s])
                    grid.append([(-i+self.origin[0])*s, (j+self.origin[0])*s])
                    j += pitch_x
                i += pitch_y
                j = self.origin[1]

            for i in grid:
                if i not in unique:
                    unique.append(i)
            grid = unique
            del unique
            grid[:] = [x for x in grid if (math.sqrt(((x[0]-self.origin[0]*1000000)**2)  +  ((x[1]-self.origin[1]*1000000)**2)  ) <= (self.wafer[0]*1000000))]
            self.exposure_points.extend(grid)
        print self.exposure_points"""





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


    def mask(self,s):
        self.mask_size=s*1.0


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
        plt.plot([-50,-50],[60,-60], 'red')
        plt.plot([-50,50],[-60,-60], 'red')
        plt.plot([50,50],[-60,60], 'red')
        plt.plot([50,-50],[60,60], 'red')

        xdata,ydata=[],[]
        print self.exposure_points
        for item in self.exposure_points:
            item=[item[0]/float(1000000), item[1]/float(1000000)]
            if self.wafer:
                plt.plot([item[0]-self.mask_size/2,item[0]+self.mask_size/2],[item[1]-self.mask_size/2,item[1]-self.mask_size/2], 'black')
                plt.plot([item[0]+self.mask_size/2,item[0]+self.mask_size/2],[item[1]-self.mask_size/2,item[1]+self.mask_size/2], 'black')
                plt.plot([item[0]+self.mask_size/2,item[0]-self.mask_size/2],[item[1]+self.mask_size/2,item[1]+self.mask_size/2], 'black')
                plt.plot([item[0]-self.mask_size/2,item[0]-self.mask_size/2],[item[1]+self.mask_size/2,item[1]-self.mask_size/2], 'black')
            xdata.append(item[0])
            ydata.append(item[1])
        plt.hold(True)
        plt.plot(xdata,ydata,'ro')#,self.origin[0],self.origin[1],'bs')
        #plt.plot()
        #plt.axis()
        plt.axis([-70, 70, -70, 70],'equal')
        plt.grid()
        plt.show()

    """def saving(self):
        if not self.shape.exists:
            self.save = raw_input('Would you like to save this pattern?(y/n)\n')
            if self.save == 'y':
                self.writeData()"""


    def substrate(self, x, y=None):
        if y==None:
            self.wafer=[x]
        else:
            self.wafer = [(-float(x)/2),(float(x)/2), (-float(y)/2),(float(y)/2)]

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
            #print item
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

