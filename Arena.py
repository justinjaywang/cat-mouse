from Tkinter import *
from math import sin, cos, pi
from Vector import *
from Color import *
from globalVars import *

class Arena(Frame):
    """This class provides the user interface for an arena of turtles."""

    def __init__(self, parent, width=400, height=400, **options):
        Frame.__init__(self, parent, **options)
        self.width, self.height = width, height
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
        
        parent.resizable(width=FALSE, height=FALSE)
        parent.title("CS9H Turtle Arena")
        self.menubar = Menu(parent)
        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="About...", command=self.about)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=parent.quit, accelerator="Command+w")
        parent.config(menu=self.menubar)
        
        Button(self, text='reset', command=self.reset, font=("Helvetica")).pack(side=LEFT)
        Button(self, text='step', command=self.step, font=("Helvetica")).pack(side=LEFT)
        Button(self, text='run', command=self.run, font=("Helvetica")).pack(side=LEFT)
        Button(self, text='stop', command=self.stop, font=("Helvetica")).pack(side=LEFT)
        Button(self, text='quit', command=parent.quit, font=("Helvetica")).pack(side=LEFT)
        
        self.stepsSV = StringVar()
        self.catRadiusSV = StringVar()
        self.catAngleSV = StringVar()
        self.mouseAngleSV = StringVar()
        self.checkboxState = IntVar()
        
        Label(self, text=" Time:", font=("Menlo", 12)).pack(side=LEFT)
        Label(self, textvariable=self.stepsSV, font=("Menlo", 12), fg=myRed, width="3").pack(side=LEFT,ipadx=0)
        Label(self, text=" CatRadius:", font=("Menlo", 12)).pack(side=LEFT)
        Label(self, textvariable=self.catRadiusSV, font=("Menlo", 12), fg=myRed, width="6").pack(side=LEFT,ipadx=0)
        Label(self, text=" CatAngle:", font=("Menlo", 12)).pack(side=LEFT)
        Label(self, textvariable=self.catAngleSV, font=("Menlo", 12), fg=myRed, width="6").pack(side=LEFT,ipadx=0)
        Label(self, text=" MouseAngle:", font=("Menlo", 12)).pack(side=LEFT)
        Label(self, textvariable=self.mouseAngleSV, font=("Menlo", 12), fg=myRed, width="6").pack(side=LEFT,ipadx=0)
        Checkbutton(self, text="stop if caught", variable=self.checkboxState, font=("Menlo", 12)).pack(side=RIGHT)
        
        self.turtles = []
        self.cats = []
        self.items = {}
        self.running = 0
        self.period = 10 # milliseconds
        self.canvas.bind('<ButtonPress>', self.press)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<ButtonRelease>', self.release)
        parent.bind('<Command-w>', self.keyQuit)
        self.dragging = None
        self.hovering = None
        self.steps = 0
        
        self.stepsSV.set(self.steps)
        self.checkboxState.set(1)

    def press(self, event):
        dragstart = Vector(event.x, event.y)
        for cat in self.cats:
            if (dragstart - cat.position).length() < 10:
                self.dragging = cat
                self.dragstart = dragstart
                self.start = cat.position
                return

    def motion(self, event):
        cursor = Vector(event.x, event.y)
        for cat in self.cats:
            if (cursor - cat.position).length() < 10:
                cat.style['fill'], cat.style['outline'] = myGrey, myGrey
                self.update(cat)
            else:
                cat.style['fill'], cat.style['outline'] = grey, grey
                self.update(cat)
        if self.dragging:
            self.dragging.angle = (cursor - self.dragging.statue.position).direction() # update angle
            self.dragging.heading = self.dragging.angle + 180
            if (self.dragging.statue.position-cursor).length()>self.dragging.statue.radius*scalePixel: # if cursor outside of statue
                self.dragging.position = self.start + cursor - self.dragstart
            else:
                self.dragging.position = self.dragging.statue.position + unit(self.dragging.angle)*self.dragging.statue.radius*scalePixel # place at base of statue
            self.update(self.dragging)
            self.dragging.arena.catRadiusSV.set(round((self.dragging.statue.position - self.dragging.position).length()*scaleMeter,2)) # update label
            self.dragging.arena.catAngleSV.set(round(self.dragging.angle,1)) # update label

    def release(self, event):
        self.dragging = None

    def update(self, turtle):
        """Update the drawing of a turtle according to the turtle object."""
        item = self.items[turtle]
        vertices = [(v.x, v.y) for v in turtle.getshape()]
        self.canvas.coords(item, sum(vertices, ()))
        self.canvas.itemconfigure(item, **turtle.style)

    def add(self, turtle, type="noncat"):
        """Add a new turtle to this arena."""
        if type=="cat":
            self.cats.append(turtle)
        self.turtles.append(turtle)
        self.items[turtle] = self.canvas.create_polygon(0, 0)
        self.update(turtle)

    def step(self, stop=1):
        """Advance all the turtles one step."""
        self.steps += 1
        self.stepsSV.set(self.steps) # update label
        nextstates = {}
        for turtle in self.turtles:
            nextstates[turtle] = turtle.getnextstate()
        for turtle in self.turtles:
            turtle.setstate(nextstates[turtle])
            self.update(turtle)
        if stop:
            self.running = 0

    def run(self):
        """Start the turtles running."""
        self.running = 1
        self.loop()

    def loop(self):
        """Repeatedly advance all the turtles one step."""
        if self.running:
            self.step(0) # used to be before if statement
            self.tk.createtimerhandler(self.period, self.loop)

    def stop(self):
        """Stop the running turtles."""
        self.running = 0
        
    def reset(self):
        """Stops simulation if running and resets to original values."""
        self.steps = 0
        self.stepsSV.set(self.steps) # update label
        self.running = 0
        resetstates = {}
        for turtle in self.turtles:
            resetstates[turtle] = turtle.getresetstate()
        for turtle in self.turtles:
            turtle.setstate(resetstates[turtle])
            self.update(turtle)
    
    def about(self):
        """Creates a popup menu with the 'About' information."""
        self.about = Toplevel(padx=80,pady=80)
        self.about.title('CS9H Turtle Arena / About')
        self.about.resizable(width=FALSE, height=FALSE)
        self.filemenu.entryconfig(0, state=DISABLED)
        photo = PhotoImage(file="me.gif")
        photoLabel = Label(self.about, image=photo).pack(side=TOP)
        self.image = photo # keep a reference of photo
        Label(self.about, text='\nCS9H Turtle Arena by Justin Wang\nUC Berkeley, Fall 2012\n', font=("Menlo", 12)).pack(side=TOP)
        Button(self.about, text='OK', command=self.closeabout, font=("Helvetica")).pack(side=TOP)
        
    def closeabout(self):
        """Closes about window."""
        self.filemenu.entryconfig(0, state=NORMAL)
        self.about.destroy()
    
    def keyQuit(self, event):
        """Quits from keyboard shortcut."""
        sys.exit(0)