from static import *
from utils import *

class Quadtree:
	def __init__(self, pg, window, data, x, y, depth):
		self.pg = pg
		self.window = window 
		self.data = data
		self.x = x
		self.y = y 

		self.x_offset = WIDTH/(2**depth)
		self.y_offset = HEIGHT/(2**depth)

		self.x_half = int(self.x_offset/2) 
		self.y_half = int(self.y_offset/2)

		self.depth = depth

		self.SEPARATION_FACTOR = SEPARATION_FACTOR
		self.ALIGNMENT_FACTOR = ALIGNMENT_FACTOR
		self.COHESION_FACTOR = COHESION_FACTOR

		self.PROTECTED_RANGE = PROTECTED_RANGE
		self.VISIBLE_RANGE = VISIBLE_RANGE

		self.reset()
		return

	def reset(self):
		self.subtrees = {
			"NW": {
				"created": False,
				"tree": None,
			},
			"NE": {
				"created": False,
				"tree": None,
			},
			"SW": {
				"created": False,
				"tree": None,
			},
			"SE": {
				"created": False,
				"tree": None,
			},
		}
		return

	def separation(self, boid):
		x_sum, y_sum = 0., 0.
		for other_boid in self.data:
			if boid.index==other_boid.index or calc_dist(boid, other_boid)>=self.PROTECTED_RANGE:
				continue

			x_sum += boid.x - other_boid.x
			y_sum += boid.y - other_boid.y

		boid.vx += x_sum*self.SEPARATION_FACTOR
		boid.vy += y_sum*self.SEPARATION_FACTOR
		return

	def alignment(self, boid):
		x_avg, y_avg = 0., 0.
		count = 0
		for other_boid in self.data:
			dist = calc_dist(boid, other_boid)

			if boid.index==other_boid.index or dist<self.PROTECTED_RANGE or dist>self.VISIBLE_RANGE:
				continue

			x_avg += other_boid.vx
			y_avg += other_boid.vy
			count += 1

		x_avg = x_avg/count if count>0 else x_avg
		y_avg = y_avg/count if count>0 else y_avg

		boid.vx += (x_avg-boid.vx)*self.ALIGNMENT_FACTOR
		boid.vy += (y_avg-boid.vy)*self.ALIGNMENT_FACTOR
		return

	def cohesion(self, boid):
		x_avg, y_avg = 0., 0.
		count = 0
		for other_boid in self.data:
			dist = calc_dist(boid, other_boid)

			if boid.index==other_boid.index or dist<self.PROTECTED_RANGE or dist>self.VISIBLE_RANGE:
				continue

			x_avg += other_boid.x
			y_avg += other_boid.y
			count += 1

		x_avg = x_avg/count if count>0 else x_avg
		y_avg = y_avg/count if count>0 else y_avg

		boid.vx += (x_avg-boid.x)*self.COHESION_FACTOR
		boid.vy += (y_avg-boid.y)*self.COHESION_FACTOR
		return

	def search(self, x, y):
		new_data = []
		for point in self.data:
			if point.x>x and point.x<x+self.x_half and point.y>y and point.y<y+self.y_half:
				new_data.append(point)
		return new_data

	def update_boids(self):
		''' heuristic to select boids satisfying specific conditions '''
		if self.depth>DEPTH-1:
			for boid in self.data:
				self.separation(boid)
				self.alignment(boid)
				self.cohesion(boid)

			[boid.update() for boid in self.data]	

		for subtree in self.subtrees.values():
			if subtree["created"]:
				subtree["tree"].update_boids()
		return

	def update(self):
		if self.depth>DEPTH:
			return

		for subtree in self.subtrees:
			if self.subtrees[subtree]["created"]:
				continue	

			if subtree=="NW":
				x, y = self.x, self.y
			elif subtree=="NE":
				x, y = self.x+self.x_half, self.y
			elif subtree=="SW":
				x, y = self.x, self.y+self.y_half
			elif subtree=="SE":
				x, y = self.x+self.x_half, self.y+self.y_half

			new_data = self.search(x, y)

			if not new_data:
				continue

			self.subtrees[subtree]["created"] = True 
			self.subtrees[subtree]["tree"] = Quadtree(self.pg, self.window, new_data, x, y, self.depth+1)
			self.subtrees[subtree]["tree"].update()
		return

	def render(self):
		self.pg.draw.line(self.window, QUADTREE_COLOR, (self.x, self.y), (self.x+self.x_offset, self.y))
		self.pg.draw.line(self.window, QUADTREE_COLOR, (self.x, self.y), (self.x, self.y+self.y_offset))
		self.pg.draw.line(self.window, QUADTREE_COLOR, (self.x+self.x_offset, self.y), (self.x+self.x_offset, self.y+self.y_offset))
		self.pg.draw.line(self.window, QUADTREE_COLOR, (self.x, self.y+self.y_offset), (self.x+self.x_offset, self.y+self.y_offset))

		for subtree in self.subtrees.values():
			if subtree["created"]:
				subtree["tree"].render()
		return
