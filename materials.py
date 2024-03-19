import pygame
import random
from pygame import Vector2
from globals import SQUARE_SIZE, SCREEN_X, SCREEN_Y

class Particle:
	def __init__(self, y, x, color = None, grid = [["" for x in range(SCREEN_X//SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.x)] for y in range(SCREEN_Y//SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.y)]):
		self.x = x
		self.y = y
		self.color = color
		self.rng = 0
		self.grid = grid
		self.moved = False
		self.xScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.x
		self.yScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.y
	
	def update(self, grid, rng):
		self.grid = grid
		self.rng = rng

	def draw(self, pos, screen):
		pygame.draw.circle(screen, self.color, pos, self.xScale//2)
	
	def onGrid(self, y, x):
		if x >= 0 and x < SCREEN_X//self.xScale and y >= 0 and y < SCREEN_Y//self.yScale:
			return True
		else:
			return False

	def swap(self, newY, newX):
		if self.onGrid(newY, newX):
			tempMaterial = self.grid[newY][newX]
			self.grid[newY][newX] = self
			self.grid[self.y][self.x] = tempMaterial
			self.grid[self.y][self.x].y = self.y
			self.grid[self.y][self.x].x = self.x
			self.y = newY
			self.x = newX


class Air(Particle):
	def __init__(self, y, x):
		super().__init__(y, x)

	def update(self, grid):
		super().update(grid)
		pass

class Sand(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (255, 200, 0))
	
	def move(self, endY, endX):
		if self.onGrid(endY, endX):
			if type(self.grid[endY][endX]) == Water:
				if random.randint(0, 100) % 2 == 0:
					self.swap(endY, endX)
			elif type(self.grid[endY][endX]) == Air:
				self.swap(endY, endX)

	def update(self, grid, rng):
		super().update(grid, rng)
		self.move(self.y+1, self.x)
		self.move(self.y+1, self.x-1)
		self.move(self.y+1, self.x+1)

class Water(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (0, 100, 255))
		self.direction = "left"

	def move(self, y, x):
		if self.onGrid(y, x):
			if type(self.grid[y][x]) == Air:
				self.swap(y, x)
				self.moved = True
				return True
			else:
				return False
			
	def checkSpot(self, y, x):
		if self.onGrid(y, x) and type(self.grid[y][x]) == Air:
			return True
		else:
			return False

	def draw(self, pos, screen):
		pygame.draw.circle(screen, self.color, pos, self.xScale//2)

	def update(self, grid, rng):
		if self.moved == False:
			super().update(grid, rng)

			# for i in range(len(self.grid)):
			# 	FDFSA = type(self.grid[len(self.grid)-1][i])
			# 	if FDFSA == Water:
			# 		print("W", end = " ")
			# 	elif FDFSA == Air:
			# 		print("_", end = " ")
			# 	elif FDFSA == Sand:
			# 		print("S", end = " ")
			# print()

			# self.move(self.y+1, self.x)
			# if (self.rng + self.y) % 2 == 0:
			# 	self.move(self.y, self.x-1)
			# else:
			# 	self.move(self.y, self.x+1)

			# if (self.checkSpot(self.y, self.x-1) or self.checkSpot(self.y, self.x+1)) and not (self.checkSpot(self.y, self.x-1) and self.checkSpot(self.y, self.x+1)):
			# 	if self.checkSpot(self.y, self.x+1):
			# 		self.move(self.y, self.x+1)
			# 	elif self.checkSpot(self.y, self.x-1):
			# 		self.move(self.y, self.x-1)
			# 	self.move(self.y+1, self.x)
			# elif (self.checkSpot(self.y, self.x-1) and self.checkSpot(self.y, self.x+1)):
			# 	if (self.rng + self.y) % 2 == 0:
			# 		self.move(self.y, self.x-1)
			# 	else:
			# 		self.move(self.y, self.x+1)
			# 	self.move(self.y+1, self.x)
			# else:
			# 	self.move(self.y+1, self.x)

			self.move(self.y+1, self.x-1)
			self.move(self.y+1, self.x+1)

			if (self.rng + self.x) % 2 == 0:
				self.move(self.y, self.x-1)
			else:
				self.move(self.y, self.x+1)

			self.move(self.y+1, self.x)