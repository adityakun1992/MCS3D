import os, re
import matplotlib.pyplot as plt


class design:
    def __init__(self):
        self.file_path=os.path.dirname(os.path.realpath(__file__)) + '/ExposureFiles/'
        self.wafer_size = None
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
        i = 0
        j = 0
        self.grid = []
        while i*pitch_x < self.sample_size[0] or i*pitch_x<250000000:
            while j*pitch_y < self.sample_size[1] or j*pitch_y<300000000:
                self.grid.append([i*pitch_x, j*pitch_y])
                j += 1
            i += 1
            j = 0
        self.exposure_points=self.grid





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


    def preview(self):
        fig = plt.figure(2)
        fig.canvas.set_window_title('Preview Window')
        plt.figure(2)
        if self.sample_size:
            plt.plot([self.sample_size[0]/2,self.sample_size[0]/2],[self.sample_size[1]/2,-self.sample_size[1]/2], 'black')
            plt.plot([self.sample_size[0]/2,-self.sample_size[0]/2],[-self.sample_size[1]/2,-self.sample_size[1]/2], 'black')
            plt.plot([-self.sample_size[0]/2,-self.sample_size[0]/2],[-self.sample_size[1]/2,self.sample_size[1]/2], 'black')
            plt.plot([-self.sample_size[0]/2,self.sample_size[0]/2],[self.sample_size[1]/2,self.sample_size[1]/2], 'black')
        xdata,ydata=[],[]
        #print self.exposure_points
        for item in self.exposure_points:
            xdata.append(item[0]/float(1000000))
            ydata.append(item[1]/float(1000000))
        plt.plot(xdata,ydata,'ro')
        plt.axis([-50, 50, -60, 60])
        plt.grid()
        plt.show()
     
    """def saving(self):
        if not self.shape.exists:
            self.save = raw_input('Would you like to save this pattern?(y/n)\n')
            if self.save == 'y':
                self.writeData()"""
    
    
    def wafer(self, x, y):
        self.sample_size = [x, y]
        
    def setOrigin(self, x, y):
        self.origin = [x, y]
        
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
