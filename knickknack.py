import pygame
from pygame.locals import *

class timer:
  def __init__(self):
    self.starttime = pygame.time.get_ticks()
    self.timeelapsed = 0
  def checktimer(self):
    self.timeelapsed = pygame.time.get_ticks() - self.starttime
  def deletetimer(self):
    del self

def settimer():
  return timer()