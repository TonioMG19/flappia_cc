import pygame
import random
import math
import os
import time

BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets","base.png")))

class Base:
	VEL = 5
	WIDTH = BASE.get_width()
	IMG = BASE

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 = self.x1 - self.VEL
		self.x2 = self.x2 - self.VEL

		if ((self.x2 + self.WIDTH) < 0):
			self.x1 = self.x2 + self.WIDTH

		if ((self.x2 + self.WIDTH) < 0):
			self.x2 = self.x1 +self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))

