from Turtle import Turtle
from Vector import *
from Color import *
from globalVars import *

class Mouse(Turtle): # inherit behavior from Turtle
  """The mouse runs in a circle around the statue, moving one meter counterclockwise."""

  def __init__(self, position, heading, arenaObj, statueObj, outline=myRed, fill=myRed, width=1):
    heading = (position - statueObj.position).direction() - 90 # initialize heading to be in direction of travel
    Turtle.__init__(self, position, float(heading), outline=outline, fill=fill, width=width)
    self.arena = arenaObj
    self.statue = statueObj
    self.angle = self.getangle()
    self.heading = heading
    self.origAngle = self.angle
    self.origPosition, self.origHeading = position, heading
    self.arena.mouseAngleSV.set(round(self.origAngle,1)) # update label

  def getnextstate(self):
    """Move one meter counterclockwise around statue."""
    
    omega = -1 # angular velocity in radians, calculated as distance/radius
    self.angle = self.getangle()
    self.newAngle = self.angle + omega*scaleDeg
    if self.newAngle < 0: # reset newAngle to make positive
      self.newAngle += 360
    self.newPosition = self.statue.position + unit(self.newAngle)*self.statue.radius*scalePixel # set new position to be one meter further along base of statue
    self.newHeading = self.heading + omega*scaleDeg
    self.arena.mouseAngleSV.set(round(self.newAngle,1)) # update label
    return self.newPosition, self.newHeading
    
  def getresetstate(self):
      """Return the original state of the cat."""
      self.arena.mouseAngleSV.set(int(self.origAngle)) # update label
      return self.origPosition, self.origHeading
    
  def getangle(self):
    """Find angle in degrees from statue to mouse."""

    return (self.position - self.statue.position).direction()