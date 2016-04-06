#from multiprocessing import Process
from Tkinter import *
import tkFileDialog,Tkconstants
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Control import SmarAct
from DesignSimulation import design
import threading
import Admin

if not Admin.isUserAdmin():
        Admin.runAsAdmin()


stage = SmarAct(0)
x, y =stage.getPosition()[0], stage.getPosition()[1]

#x, y = 0, 0
series = design()


class Application(Frame):
    def __init__(self, master=None):
        self.fig = plt.figure(figsize=(3,2.6))
        self.history=[]
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
        text = self.T.get("1.0",END)

        # if not("print \"xyz\"" in text):
        #     print text
        #     exec(text)
        # else:
        #     move_index = text.index('print "xyz"')
        #     exec(text[:move_index])
        #     t = threading.Thread(text[move_index])
        #     t.start()
        tex=[]
        #text = text.splitlines()
        tex = []
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


    def printSeries(self):
        exec(self.move_command)
            #self.expose(dosage)
        #self.tracking(series1,dosage)

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

    def print_manual(self):
        stage.expose_manual(1)


    def asksaveasfilename(self):
        #filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".py")
        text2save=str(self.T.get(0.0,END))
        f.write(text2save)
        f.close()


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
        options['initialdir'] = 'C:\\'
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
        self.print_label = Label(root, text="Print Time:")
        self.print_label.pack()
        self.print_label.place(x = 770, y=80, bordermode=OUTSIDE)
        self.print_text = Text(root, height=1, width=6)
        self.print_text.place(x=840, y=80)
        self.expose = Button(root, text ="Print", command = self.print_manual)
        self.expose.pack()
        self.expose.place(x = 960, y=80, bordermode=OUTSIDE)

        self.QUIT = Button(root, text ="Stop", command = self.quit)
        self.QUIT.place(x = 20, y=390, bordermode=OUTSIDE)


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
            #print self.x,self.y
            #self.x, self.y = stage.getPosition()[0], stage.getPosition()[1]
            #x, y = 0, 0
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
        self.anim=animation.FuncAnimation(self.fig, self._update_plot, frames=100, interval=100)


#xdata=[]
#ydata=[]
root = Tk()
root.geometry("1024x430")
global app
app = Application(master=root)

plt.close()
"""def data_gen():
    while True:
        x, y =stage.getPosition()[0], stage.getPosition()[1]
        app.updateCurrent(x, y)
        yield x/1000000, y/1000000

        #yield 0,0
def run(data):
    # update the data
    xpos,ypos = data
    xdata.append(xpos)
    ydata.append(ypos)
    xmin, xmax = ax.get_xlim()
    line.set_data(xdata, ydata)
    return line,"""

"""def _update_plot(i, fig, scat):
    print i,fig,scat
    while True:
        #x, y = stage.getPosition()[0], stage.getPosition()[1]
        x, y = 0, 0
        app.updateCurrent(x, y)
        scat.set_offsets(([x/1000000,y/1000000]))
        return scat,2
"""
#ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=2, repeat=False)
app.mainloop()
root.destroy()





"""def exec_process(text):
    print "executing"
    exec(text)
if __name__ == '__main__':
  p1 = Process(target=gui_process)
  p1.start()
  p1.join()"""
