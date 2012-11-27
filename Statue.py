from Turtle import Turtle
from Vector import *
from Color import *
from globalVars import *

class Statue(Turtle): # inherit behavior from Turtle
  """Fixed object, circle of radius one meter."""

  def __init__(self, position, heading, outline=lightGrey, fill=lightGrey, width=1):
    Turtle.__init__(self, position, heading, outline=outline, fill=fill, width=width)
    self.radius = 1 # in meters
      
  def getshape(self): # override default Turtle shape
    """Return a list of vectors giving the polygon for this turtle."""
    vectors = []
    for i in range(360):
      unitVector = unit(self.heading + i)
      vectors.append(self.position + unitVector*scalePixel)
    return vectors
