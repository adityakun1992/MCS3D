from Tkinter import *
import tkFileDialog,Tkconstants
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Control import SmarAct
from DesignSimulation import design
import threading
import pickle, json
import Admin
import os
import numpy as np
import itertools
import subprocess
import multiprocessing


def preview_worker(exposure_points,wafer,mask_size):
    fig = plt.figure(2)
    fig.canvas.set_window_title('Preview Window')
    plt.figure(2)
    plt.plot([-50,-50],[60,-60], 'red')
    plt.plot([-50,50],[-60,-60], 'red')
    plt.plot([50,50],[-60,60], 'red')
    plt.plot([50,-50],[60,60], 'red')

    xdata,ydata=[],[]
    for item in exposure_points:
        item=[item[0]/float(1000000), item[1]/float(1000000)]
        if wafer:
            plt.plot([item[0]-mask_size/2,item[0]+mask_size/2],[item[1]-mask_size/2,item[1]-mask_size/2], 'black')
            plt.plot([item[0]+mask_size/2,item[0]+mask_size/2],[item[1]-mask_size/2,item[1]+mask_size/2], 'black')
            plt.plot([item[0]+mask_size/2,item[0]-mask_size/2],[item[1]+mask_size/2,item[1]+mask_size/2], 'black')
            plt.plot([item[0]-mask_size/2,item[0]-mask_size/2],[item[1]+mask_size/2,item[1]-mask_size/2], 'black')
        xdata.append(item[0])
        ydata.append(item[1])
    plt.hold(True)
    plt.plot(xdata,ydata,'ro')#,origin[0],origin[1],'bs')
    #plt.plot()
    #plt.axis()
    plt.axis([-70, 70, -70, 70],'equal')
    plt.grid()
    plt.show()

if __name__=='__main__':
    if not Admin.isUserAdmin():
        Admin.runAsAdmin()
    stage = SmarAct(0)
    #x, y =stage.getPosition()[0], stage.getPosition()[1]
    #stage.generate_json(0,100,[0,0])
    p = subprocess.Popen(["python", "AtomServer.py"])

    x, y = 0, 0
    series = design()


    class Application(Frame):
        def __init__(self, master=None):
            self.fig = plt.figure(figsize=(3,2.6))
            self.x=0
            self.y=0
            Frame.__init__(self, master)
            self.origin_x = 0
            self.origin_y = 0
            self.pack()
            self.createWidgets(self.fig)
            self.updateOrigin(0, 0)
            #self.mainloop()
            self.ax=FALSE
            self.tracking()


        def execute_code(self):
            main_text = self.T.get("1.0",END)
            text=main_text
            while "series.preview()" in text:
                tex = text[:text.index('series.preview()')]
                tex=''.join(tex)
                if len(tex)>0 and ('stage.printSeries(' in tex):
                    print "Please start printing using the \"Print Series\" button."
                elif len(tex)>0:
                    exec(tex)
                p=multiprocessing.Process(target=preview_worker,args=(series.exposure_points,series.wafer,series.mask_size))
                p.start()
                text=text[(text.index('series.preview()')+16):]
                text=''.join(text)
                print text
            if len(text)>0 and ('stage.printSeries(' in text):
                #tex=[]
                #tex.extend(text[:text.index('stage.')])
                tex = text[:text.index('stage.printSeries(')]
                tex=''.join(tex)
                if len(tex)>0:
                    exec(tex)
                text=text[(text.index('stage.printSeries(')):]
                text=text[text.index('\n'):]
                #self.move_command = text[text.index('stage.'):]
                print "The script has been executed till the first stage command.\nPlease start printing using the \"Print Series\" button"
            elif len(text)>0:
                exec(text)

            """if "stage." in text:
                tex.extend(text[:text.index('stage.')])
                self.move_command = text[text.index('stage.'):]
                tex=''.join(tex)
                print tex
                exec(tex)
                t = threading.Thread(target = self.printSeries)
                t.start()
            else:
                exec(text)"""

        """
            #######################################################################################################
            #Attempts to a neat execution of threads without restrictions on numberor location of preview commands#
            #######################################################################################################
        def execute_code(self):
            text = self.T.get("1.0",END)
            #text = "import numpy as np\nseries.exposure_points = []\nseries.mask(6)\nseries.setOrigin(0,-20)\nseries.substrate(38)\nseries.gengrid(7,7)\nseries.preview()\nseries.dosage=np.ones(len(series.exposure_points))*52\nseries.name('cgrid')\nseries.writeData()"
            # if not("print \"xyz\"" in text):
            #     print text
            #     exec(text)
            # else:
            #     move_index = text.index('print "xyz"')
            #     exec(text[:move_index])
            #     t = threading.Thread(text[move_index])
            #     t.start()
            tex,endswith_preview = self.split_for_thread(text)
            if "stage." in text:
                 tex.extend(text[:text.index('stage.')])
                 self.move_command = text[text.index('stage.'):]
                 tex=''.join(tex)
                 print tex
                 exec(tex)
                 t = threading.Thread(target = self.printSeries)
                 t.start()
            else:
                exec(text)

            for i in range(len(tex)):
                self.text_to_execute = tex[i]
                t = threading.Thread(target = self.execute_newthread)
                t.start()
                if i != 0:
                    t.join()
                if i<len(tex)-1 and len(tex)>1:
                    series.preview()
            if endswith_preview:
                series.preview()

        def split_for_thread(self,text):
            tex = list()
            #matplotlib should rn in main thread - side threads not not allowed dring plotting
            if "series.preview()" in text:
                tex.append(text[:text.index('series.preview()')])
                tex.append(text[(text.index('series.preview()')+16):])
                while "series.preview()" in tex[-1]:
                    text = tex[-1]
                    tex[-1] = ''.join(text[:text.index('series.preview()')])
                    tex.append(text[(text.index('series.preview()')+16):])
            else:
                tex = [''.join(text)]
                print tex
            if text.rstrip('\n')[-17:] == 'series.preview()':
                endswith_preview = True
            else:
                endswith_preview = False
            return tex, endswith_preview


        def execute_newthread(self):
            exec(self.text_to_execute)


        #########################################################
        #Attempts to a neat execution - Ends Here, Not Commplete#
        #########################################################  """


        def printSeries(self):
            exec(self.move_command)

        def askopenfilename(self):
            filename = tkFileDialog.askopenfilename(**self.file_opt)
            if filename:
                script = open(filename, 'r')
                entry = []
                text = self.T.get(1.0,END)
                if text:
                    if text[len(text)-2] != '\n':
                        self.T.insert(END, '\n\n')
                    else:
                        self.T.insert(END, '\n')
                for line in script:
                    self.T.insert(END, line)
                    #text = self.T.get("1.0",END)
                    #text = text + str(entry)

        def stage_manual(self):
            x = self.gotoX.get("1.0",END)
            y = self.gotoY.get("1.0",END)
            stage.move(x*1000000,y*1000000)

        def beam_on(self):
            stage.expose_on()

        def beam_off(self):
            stage.expose_off()


        def asksaveasfilename(self):
            #filename = tkFileDialog.asksaveasfilename(**self.file_opt)
            f = tkFileDialog.asksaveasfile(mode='w', **self.file_opt)
            text2save=str(self.T.get(0.0,END))
            f.write(text2save)
            f.close()

        def print_series(self):
            if len(series.exposure_points) == 0 or len(series.dosage) == 0 or len(series.exposure_points) == len(series.dosage):
                print "Error in print data. Please verify."
            elif threading.active_count()>1:
                    print "Another thread is controlling the stage. Please wait till the command has finished execution or restart the program."
            else:
                t=threading.Thread(target = stage.printSeries, args=(series.exposure_points,series.dosage))
                t.start()

        def bc(self):
            def check_beamcurrent():
                print "Check Beam Current"
                self.beam_off()
                stage.move()
                self.beam_on()
            t = threading.Thread(target = check_beamcurrent)
            if threading.active_count > 1:
                print "Cannot perform stage operations while print process is going on. Will allow to check beam current after the end of the process."
            else:
                t.start()

        def createWidgets(self, fig):
            self.T = Text(root, height=20, width=50)
            self.T.place(x=20, y=10)


            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.get_tk_widget().place(x = 500, y=10)

            self.execute = Button(root, text ="Execute", command = self.execute_code)
            self.execute.pack()
            self.execute.place(x = 20, y=350, bordermode=OUTSIDE)


            button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
            self.openscript = Button(root, text='Open Script', command=self.askopenfilename)
            self.openscript.pack(**button_opt)
            self.openscript.place(x = 170, y=350, bordermode=OUTSIDE)
            self.savescript = Button(root, text='Save Script', command=self.asksaveasfilename)
            self.savescript.pack(**button_opt)
            self.savescript.place(x = 350, y=350, bordermode=OUTSIDE)
            self.file_opt = options = {}
            options['defaultextension'] = '.py'
            options['filetypes'] = [('Python files', '.py'), ('all files', '.*')]
            options['initialdir'] = os.path.dirname(os.path.realpath(__file__)) + '\Scripts'
            options['initialfile'] = ''
            options['parent'] = root
            options['title'] = 'Select a File'

            self.current_x = Label(root, text="Current X Position")
            self.current_x.pack()
            self.current_x.place(x = 500, y=300, bordermode=OUTSIDE)
            self.x_text = Text(root, height=1, width=20)
            self.x_text.place(x=605, y=300)
            self.current_y = Label(root, text="Current Y Position")
            self.current_y.pack()
            self.current_y.place(x = 500, y=320)
            self.y_text = Text(root, height=1, width=20)
            self.y_text.place(x=605, y=320)

            self.desired_x = Label(root, text="Desired X Position")
            self.desired_x.pack()
            self.desired_x.place(x = 500, y=340, bordermode=OUTSIDE)
            self.dx_text = Text(root, height=1, width=20)
            self.dx_text.place(x=605, y=340)
            self.desired_y = Label(root, text="Desired Y Position")
            self.desired_y.pack()
            self.desired_y.place(x = 500, y=360)
            self.dy_text = Text(root, height=1, width=20)
            self.dy_text.place(x=605, y=360)

            self.x_origin = Label(root, text="X Origin")
            self.x_origin.pack()
            self.x_origin.place(x = 800, y=320, bordermode=OUTSIDE)
            self.xorigin_text = Text(root, height=1, width=20)
            self.xorigin_text.place(x=850, y=320)

            self.y_origin = Label(root, text="Y Origin")
            self.y_origin.pack()
            self.y_origin.place(x = 800, y=340, bordermode=OUTSIDE)
            self.yorigin_text = Text(root, height=1, width=20)
            self.yorigin_text.place(x=850, y=340)

            #manual controls
            self.goto_x = Label(root, text="Manual Control")
            self.goto_x.pack()
            self.goto_x.place(x = 770, y=30, bordermode=OUTSIDE)
            self.goto_x = Label(root, text="X:")
            self.goto_x.pack()
            self.goto_x.place(x = 770, y=50, bordermode=OUTSIDE)
            self.gotoX = Text(root, height=1, width=6)
            self.gotoX.place(x=790, y=50)
            self.goto_y = Label(root, text="Y:")
            self.goto_y.pack()
            self.goto_y.place(x = 870, y=50, bordermode=OUTSIDE)
            self.gotoY = Text(root, height=1, width=6)
            self.gotoY.place(x=890, y=50)
            self.goto = Button(root, text ="Goto", command = self.stage_manual)
            self.goto.pack()
            self.goto.place(x = 960, y=47, bordermode=OUTSIDE)

            #manual print
            """self.print_label = Label(root, text="Print Time:")
            self.print_label.pack()
            self.print_label.place(x = 770, y=80, bordermode=OUTSIDE)
            self.print_text = Text(root, height=1, width=6)
            self.print_text.place(x=840, y=80)"""
            self.expose_on = Button(root, text ="Beam On", command = self.beam_on)
            self.expose_on.pack()
            self.expose_on.place(x = 840, y=100, bordermode=OUTSIDE)



            self.expose_off = Button(root, text ="Beam Off", command = self.beam_off)
            self.expose_off.pack()
            self.expose_off.place(x = 920, y=100, bordermode=OUTSIDE)

            self.current_check = Button(root, text='Check Beam Current', command=self.bc)
            self.current_check.pack()
            self.current_check.place(x = 840, y=150, bordermode=OUTSIDE)
            self.ps = Button(root, text='Print Series', command=self.print_series)
            self.ps.pack()
            self.ps.place(x = 840, y=200, bordermode=OUTSIDE)

            self.QUIT = Button(root, text ="Stop", command = self.kill)
            self.QUIT.place(x = 20, y=390, bordermode=OUTSIDE)

        def kill(self):
            p.kill()
            self.quit()


        def updateCurrent(self, x, y):
            self.x_text.delete("1.0", END)
            self.x_text.insert(INSERT, str(x))
            self.y_text.delete("1.0", END)
            self.y_text.insert(INSERT, str(y))

        def updateDesired(self, x, y):
            self.dx_text.delete("1.0", END)
            self.dx_text.insert(INSERT, str(x))
            self.dy_text.delete("1.0", END)
            self.dy_text.insert(INSERT, str(y))

        def updateOrigin(self, x, y):
            self.xorigin_text.delete("1.0", END)
            self.xorigin_text.insert(INSERT, str(x))
            self.yorigin_text.delete("1.0", END)
            self.yorigin_text.insert(INSERT, str(y))

        def _update_plot(self, i):
            while True:
                """self.history.extend([self.getPosition()])
                if len(self.history)>=20:
                    if ((not history or [history[0]]*len(history) == history)):
                        del history
                        stage.reconnect()"""
                self.x, self.y = stage.getPosition()[0], stage.getPosition()[1]
                #self.x, self.y = self.x+series.small_num, self.y+series.small_num
                self.updateCurrent(self.x, self.y)
                self.scat.set_offsets(([self.x/1000000,self.y/1000000]))
                return self.scat,2

        def tracking(self, series1=0,dosage=0):
            if self.ax == FALSE:
                self.ax = self.fig.add_subplot(111)
                self.x=[0,50,100]
                self.y=[0,0,0]
                self.ax.grid()
                self.ax.set_ylim(-60, 60)
                self.ax.set_xlim(-50, 50)
                self.line, = self.ax.plot([], [], lw=1)
                self.scat=plt.scatter(x, y, c=x)
                self.x, self.y =0,0
            self.anim=animation.FuncAnimation(self.fig, self._update_plot, frames=100, interval=100)

        def __del__(self):
            p.kill()


    def pickling():
        """if stage.jsonobj != None:
            pickleobj = pickle.dump(stage.jsonobj)
        else:"""
        data = json.dumps({"current_percentage": 0, "current_point": 0, "noofpoints": 0, "point": [0,0], "msg": "Intialized, Not running"})
        s = pickle.dump( data, open( "progress.p", "wb" ) )
        #p = subprocess.Popen(["python", "AtomServer.py"],stdin = subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    pickling()
    #p.kill()
    #p = subprocess.Popen(["python", "AtomServer.py"],stdin = subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    #xdata=[]
    #ydata=[]
    root = Tk()
    root.geometry("1024x430")
    global app
    app = Application(master=root)
    def merge(x,y):
        points=[]
        for i,j in itertools.product(x,y):
            points.append([i,j])
        return points

    plt.close()

    #ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=2, repeat=False)
    app.mainloop()
    root.destroy()