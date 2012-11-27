from Tkinter  import *                  # Import everything from Tkinter
from Arena    import Arena              # Import our Arena
from Cat      import Cat                # Import our Cat
from Mouse    import Mouse              # Import our Statue
from Statue   import Statue             # Import our Statue
from Vector   import *                  # Import everything from our Vector
from globalVars import *                # Import everything from globalVars
from random   import random             # Import random

tk = Tk()                               # Create a Tk top-level widget
arena = Arena(tk, 800, 600, padx=12, pady=6) # Create an Arena widget, arena
arena.pack()                            # Tell arena to pack itself on screen

midX = arena.width/2                    # Horizontal center of window
midY = arena.height/2                   # Vertical center of window
mouseAngle = random()*360*scaleRad      # Random mouse angle to initialize
catAngle = random()*360*scaleRad        # Random cat angle to initialize
catRadius = 5                           # Random cat radius to initialize

statue = Statue(Vector(midX,midY), 0)   # Create a statue in center of arena, arbitrary heading
arena.add(statue)                       # Add statue

mouse = Mouse(Vector(midX + statue.radius*scalePixel*cos(mouseAngle), midY - statue.radius*scalePixel*sin(mouseAngle)), 0, arena, statue) # Create a mouse at right edge of statue, arbitrary heading since it will be overwritten in initialization
arena.add(mouse)                        # Add mouse
 
cat = Cat(Vector(midX + catRadius*scalePixel*cos(catAngle), midY - catRadius*scalePixel*sin(catAngle)), 0, arena, statue, mouse) # Create a cat at given angle and radius, arbitrary heading since it will be overwritten in initialization
arena.add(cat, "cat")                   # Add cat and specify that it's a cat as extra argument

tk.mainloop()                           # Enter the Tkinter event loop