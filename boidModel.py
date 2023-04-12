from static import *
from utils import *

import numpy as np
import random
import math

class Boid:
	def __init__(self, pg, window, index, x, y, color=(100,100,100)):
		self.pg = pg
		self.window = window 
		self.index = index 
		self.x = x
		self.y = y

		self.vx = random.random()-0.5
		self.vy = random.random()-0.5

		''' coordinates for triangle vertices '''
		self.mat = np.array([
			[-1, 2],
			[-1, -2],
			[6, 0]
		])*BOID_SIZE

		self.group = random.choice([1, 2, 3, 4])

		self.color = BOID_COLORS[self.group]

		self.TURN_FACTOR = TURN_FACTOR

		self.X_OFFSET = X_OFFSET
		self.Y_OFFSET = Y_OFFSET

		self.MAX_SPEED = MAX_SPEED
		self.MIN_SPEED = MIN_SPEED
		self.BIAS = BIAS
		return

	def update(self):
		''' update position '''
		self.x += self.vx
		self.y += self.vy

		''' invoke turning behaviour if boid is near the edges '''
		if self.x < self.X_OFFSET:
			self.vx += self.TURN_FACTOR
		elif self.x > WIDTH-self.X_OFFSET:
			self.vx -= self.TURN_FACTOR

		if self.y < self.Y_OFFSET:
			self.vy += self.TURN_FACTOR
		elif self.y > HEIGHT-self.Y_OFFSET:
			self.vy -= self.TURN_FACTOR

		''' tweak velocity using bias factors '''
		self.vx = (1-self.BIAS)*self.vx + self.group*self.BIAS
		self.vy = (1-self.BIAS)*self.vy + self.group*self.BIAS

		''' restrict speed of the boid '''
		speed = math.sqrt(self.vx**2+self.vy**2)	

		if speed>self.MAX_SPEED:
			self.vx = (self.vx/speed)*self.MAX_SPEED
			self.vy = (self.vy/speed)*self.MAX_SPEED
		if speed<self.MIN_SPEED:
			self.vx = (self.vx/speed)*self.MIN_SPEED
			self.vy = (self.vy/speed)*self.MIN_SPEED
		return

	def render(self):
		''' rotate the boid accordingly '''
		angle = -math.atan2(self.vy, self.vx)

		rotated = np.dot(self.mat, get_rot_mat(angle))
		rotated = [tuple((v[0]+self.x, v[1]+self.y)) for v in rotated]

		self.pg.draw.polygon(self.window, self.color, rotated, 1)
		return
