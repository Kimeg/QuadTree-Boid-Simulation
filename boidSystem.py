from static import *
from boidModel import Boid

import random

class System:
	def __init__(self, pg, window):
		self.boids = [Boid(pg, window, i, random.randint(EDGE_WIDTH, WIDTH-EDGE_WIDTH), random.randint(EDGE_HEIGHT, HEIGHT-EDGE_HEIGHT)) for i in range(nBoid)]
		self.running = True

		self.SEPARATION_FACTOR = SEPARATION_FACTOR
		self.ALIGNMENT_FACTOR = ALIGNMENT_FACTOR
		self.COHESION_FACTOR = COHESION_FACTOR

		self.PROTECTED_RANGE = PROTECTED_RANGE
		self.VISIBLE_RANGE = VISIBLE_RANGE

		self.TURN_FACTOR = TURN_FACTOR

		self.X_OFFSET = X_OFFSET
		self.Y_OFFSET = Y_OFFSET

		self.MAX_SPEED = MAX_SPEED
		self.MIN_SPEED = MIN_SPEED
		self.BIAS = BIAS
		return

	def render(self):
		for boid in self.boids:
			boid.render()
		return 
