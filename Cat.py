from Turtle import Turtle
from Vector import *
from Color import *
from globalVars import *

class Cat(Turtle): # inherit behavior from Turtle
  """The cat moves one meter toward the statue (if mouse is seen) or circles 1.25 meters counterclockwise (if mouse is not seen)."""

  def __init__(self, position, heading, arenaObj, statueObj, mouseObj, outline=grey, fill=grey, width=1):
    heading = (position - statueObj.position).direction() + 180 # initialize heading to be facing statue
    Turtle.__init__(self, position, float(heading), outline=outline, fill=fill, width=width)
    self.arena = arenaObj
    self.statue = statueObj
    self.mouse = mouseObj
    self.state = 'start' # string to keep track of state
    self.angle = self.getangle()
    self.heading = heading
    self.radius = self.getradius()
    self.origRadius, self.origAngle = self.radius, self.angle
    self.origPosition, self.origHeading = position, heading
    self.arena.catRadiusSV.set(round(self.origRadius,2)) # update label
    self.arena.catAngleSV.set(round(self.origAngle,1)) # update label

  def getnextstate(self):
    """Move one meter toward statue or circle 1.25 meters counterclockwise."""
    
    self.angle = self.getangle()
    self.radius = self.getradius()
      
    if self.mouseSeen(): # mouse seen, move one meter toward statue
      self.state = 'mouse seen'
      speed = 1.0
      self.newAngle = self.angle
      if self.radius < (self.statue.radius + speed): # if close enough to statue so as to not move full distance
        self.newPosition = self.statue.position + unit(self.newAngle)*self.statue.radius*scalePixel
      else:
        self.newPosition = self.position - unit(self.newAngle)*speed*scalePixel
      self.newHeading = self.newAngle + 180
      self.newRadius = (self.statue.position - self.newPosition).length()*scaleMeter
    else: # mouse not seen, move 1.25 meters counterclockwise
      self.state = 'mouse not seen'
      omega = -1.25/self.radius
      self.newRadius = self.radius
      self.newAngle = self.angle + omega*scaleDeg
      if self.newAngle < 0:
        self.newAngle += 360
      self.newPosition = self.statue.position + unit(self.newAngle)*self.radius*scalePixel
      self.newHeading = self.newAngle - 90
    
    if self.mouseCaught() and self.arena.checkboxState.get(): # if checkbox to stop is selected and mouse is caught
      self.state = 'mouse caught!'
      self.arena.stop()
      
    if debugFlag:
      self.debugPrint()
    
    self.arena.catRadiusSV.set(round(self.newRadius,2)) # update label
    self.arena.catAngleSV.set(round(self.newAngle,1)) # update label
    
    return self.newPosition, self.newHeading
  
  def getresetstate(self):
      """Return the original state of the cat."""
      self.arena.catRadiusSV.set(round(self.origRadius,2)) # update label
      self.arena.catAngleSV.set(round(self.origAngle,1)) # update label
      return self.origPosition, self.origHeading
  
  def getradius(self):
    """Find distance in meters of statue to cat."""
    
    return (self.statue.position - self.position).length()*scaleMeter
  
  def getangle(self):
    """Find angle in degrees from statue to cat."""
    
    return (self.position - self.statue.position).direction()
    
  def mouseSeen(self):
    """Returns boolean whether or not mouse is seen by cat."""
    
    return self.radius*cos((self.angle - self.mouse.angle)*scaleRad) >= 1.0
  
  def mouseCaught(self):
    """Returns boolean whether or not mouse is caught by cat."""
    
    catBase = abs(self.newRadius-1) < 0.001
    theta = self.mouse.angle
    A = self.angle
    B = self.mouse.newAngle
    C = self.newAngle
    if C-A > 180:
      A += 360
    if A-theta > 180:
      theta += 360
    mouseBetween = cos((B-A)*scaleRad)>cos((C-A)*scaleRad) and cos((C-B)*scaleRad)>cos((C-A)*scaleRad)
    catAhead = A-theta < 0 # make sure current angle is not greater than current mouse angle
    return catBase and mouseBetween and not catAhead
    
  def debugPrint(self):
    """Prints state, positions, radius, and angles of cat and mouse for debugging."""
    print 'state:\t\t', self.state
    # print 'mouse position:\t%3.2f, %3.2f' % (self.mouse.newPosition.x, self.mouse.newPosition.y)
    print 'mouse angle:\t%3.2f' % self.mouse.newAngle
    # print 'cat position:\t%3.2f, %3.2f' % (self.newPosition.x, self.newPosition.y)
    print 'cat angle:\t%3.2f' % self.newAngle
    print 'cat radius:\t%3.2f' % self.newRadius