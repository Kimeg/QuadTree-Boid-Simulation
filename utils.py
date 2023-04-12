import numpy as np
import math

def calc_dist(boid_1, boid_2):
	pos_1 = [boid_1.x, boid_1.y]
	pos_2 = [boid_2.x, boid_2.y]
	return np.sqrt(np.sum([(i-j)**2 for i, j in zip(pos_1, pos_2)]))

def get_rot_mat(angle):
	return np.array([
		[math.cos(angle), -math.sin(angle)],
		[math.sin(angle), math.cos(angle)],
	])