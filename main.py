from static import *
from boidModel import Boid
from boidSystem import System 
from quadTree import Quadtree

import pygame as pg
import numpy as np
import random
import math

def main():
	''' object to hold parameter values and boid objects '''
	system = System(pg, window)

	''' quadtree structure to process and update boid flocking behaviour '''
	quadtree = Quadtree(pg, window, system.boids, 0, 0, 0)

	while system.running:
		for event in pg.event.get():
			if event.type==pg.QUIT:
				system.running = False
				break

			'''
				Keyboard input usage for parameter tuning	
			'''
			if event.type==pg.KEYDOWN:
				if event.key==pg.K_a:
					system.ALIGNMENT_FACTOR += 0.01
				if event.key==pg.K_z:
					system.ALIGNMENT_FACTOR -= 0.01
				if event.key==pg.K_s:
					system.SEPARATION_FACTOR += 0.01
				if event.key==pg.K_x:
					system.SEPARATION_FACTOR -= 0.01
				if event.key==pg.K_c:
					system.COHESION_FACTOR += 0.01
				if event.key==pg.K_d:
					system.COHESION_FACTOR -= 0.01
				if event.key==pg.K_v:
					system.VISIBLE_RANGE += 0.01
				if event.key==pg.K_f:
					system.VISIBLE_RANGE -= 0.01
				if event.key==pg.K_g:
					system.PROTECTED_RANGE += 0.01
				if event.key==pg.K_b:
					system.PROTECTED_RANGE -= 0.01

		clock.tick(FPS)

		window.fill((0, 0 ,0))

		''' Delete previous quadtree info and generate a new one '''
		quadtree.reset()

		''' Iteratively generate sub-quadtrees containing relevant boids '''
		quadtree.update()

		''' For each subtree, update flocking behaviour of its boid(s) '''
		quadtree.update_boids()

		''' Iteratively draw quadtree structures '''
		quadtree.render()

		''' Draw boids '''
		system.render()

		pg.display.update()

	pg.quit()
	return

if __name__=="__main__":
	pg.init()

	window = pg.display.set_mode((WIDTH, HEIGHT))

	pg.display.set_caption("Flocking Boids Simulation")

	clock = pg.time.Clock()

	main()
