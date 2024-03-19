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
		super().update(grid, rng)
		# if self.onGrid(self.y+1, self.x) and type(grid[self.y+1][self.x]) == Air:
		# 	self.swap(self.y+1, self.x, grid)
		# else:
		# 	if self.onGrid(self.y+1, self.x+1) and type(grid[self.y+1][self.x+1]) == Air:
		# 		self.swap(self.y+1, self.x+1, grid)
		# 	elif self.onGrid(self.y+1, self.x-1) and type(grid[self.y+1][self.x-1]) == Air:
		# 		self.swap(self.y+1, self.x-1, grid)
		# 	if self.onGrid(self.y, self.x+1) and type(grid[self.y][self.x+1]) == Air:
		# 		self.swap(self.y, self.x+1, grid)
		# 	elif self.onGrid(self.y, self.x-1) and type(grid[self.y][self.x-1]) == Air:
		# 		self.swap(self.y, self.x-1, grid)
		# 	if self.onGrid(self.y, self.x+2) and type(grid[self.y][self.x+2]) == Air:
		# 		self.swap(self.y, self.x+2, grid)
		# 	elif self.onGrid(self.y, self.x-2) and type(grid[self.y][self.x-2]) == Air:
		# 		self.swap(self.y, self.x-2, grid)
		# tempMove(self.y, self.x+2)
		# tempMove(self.y, self.x-2)

		movedDown = self.move(self.y+1, self.x)
		if movedDown:
			self.move(self.y, self.x-1)
			self.move(self.y, self.x+1)
		else:
			if self.rng % 2 == 0:
				self.move(self.y, self.x-1)
			else:
				self.move(self.y, self.x+1)