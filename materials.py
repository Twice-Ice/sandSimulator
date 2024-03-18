import pygame
import random
from pygame import Vector2
from globals import SQUARE_SIZE, SCREEN_X, SCREEN_Y

class Particle:
	def __init__(self, y, x, color = None):
		self.x = x
		self.y = y
		self.color = color
		self.xScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.x
		self.yScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.y

	def moveMaterial(self, endY, endX, grid):
		if self.onGrid(endY, endX):
			if type(grid[endY][endX]) == Air:
				grid[self.y][self.x] = Air(self.y, self.x)
				grid[endY][endX] = self
				self.y = endY
				self.x = endX
	
	def onGrid(self, y, x):
		if x >= 0 and x < SCREEN_X//self.xScale and y >= 0 and y < SCREEN_Y//self.yScale:
			return True
		else:
			return False

	def draw(self, pos, screen):
		pygame.draw.circle(screen, self.color, pos, self.xScale//2)

	def swap(self, newY, newX, grid):
		tempMaterial = grid[newY][newX]
		grid[newY][newX] = self
		grid[self.y][self.x] = tempMaterial
		grid[self.y][self.x].y = self.y
		grid[self.y][self.x].x = self.x
		self.y = newY
		self.x = newX
		

class Air(Particle):
	def __init__(self, y, x):
		super().__init__(y, x)

	def update(self, grid):
		pass

class Sand(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (255, 200, 0))
	
	def moveMaterial(self, endY, endX, grid):
		super().moveMaterial(endY, endX, grid)
		if self.onGrid(endY, endX):
			if type(grid[endY][endX]) == Water:
				if random.randint(0, 100) % 2 == 0:
					self.swap(endY, endX, grid)

	def update(self, grid):
		self.moveMaterial(self.y+1, self.x, grid)
		self.moveMaterial(self.y+1, self.x-1, grid)
		self.moveMaterial(self.y+1, self.x+1, grid)

class Water(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (0, 100, 255))
	
	def update(self, grid):
		self.moveMaterial(self.y+1, self.x, grid)
		leftRight = random.randint(0, 100) % 2 == 0
		self.moveMaterial(self.y+1, self.x+1, grid)
		self.moveMaterial(self.y+1, self.x-1, grid)
		if leftRight == True:
			self.moveMaterial(self.y, self.x+1, grid)
			self.moveMaterial(self.y, self.x-1, grid)
			self.moveMaterial(self.y, self.x+2, grid)
			self.moveMaterial(self.y, self.x-2, grid)
		elif leftRight == False:
			self.moveMaterial(self.y, self.x-1, grid)
			self.moveMaterial(self.y, self.x+1, grid)
			self.moveMaterial(self.y, self.x-2, grid)
			self.moveMaterial(self.y, self.x+2, grid)