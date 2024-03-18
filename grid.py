import pygame
from pygame import Vector2
import random
from globals import SCREEN_X, SCREEN_Y, SQUARE_SIZE

class Grid:
	def __init__(self, scale = SQUARE_SIZE, color = (255, 255, 255)):
		self.xScale = scale if type(scale) != Vector2 else scale.x
		self.yScale = scale if type(scale) != Vector2 else scale.y
		self.xTiles = SCREEN_X//self.xScale
		self.yTiles = SCREEN_Y//self.yScale
		self.color = color
		self.grid = [[Air(x, y) for x in range(self.xTiles)] for y in range(self.yTiles)]

	def update(self, screen):
		for y in range(len(self.grid)-1, 0, -1):
			for x in range(len(self.grid[y])):
				if type(self.grid[y][x]) != Air:
					self.grid[y][x].draw((x*self.xScale, y*self.yScale), screen)
					self.grid[y][x].update(self.grid)

	def drawLines(self, screen):
		for y in range(self.yTiles):
			pygame.draw.line(screen, self.color, (0, self.yScale * y), (SCREEN_X, self.yScale * y))
		for x in range(self.xTiles):
			pygame.draw.line(screen, self.color, (self.xScale * x, 0), (self.xScale * x, SCREEN_Y))

		#draws final lines to prevent the grid's lines being chopped off at the end of the screen.
		pygame.draw.line(screen, self.color, (0, SCREEN_Y - 1), (SCREEN_X, SCREEN_Y - 1))
		pygame.draw.line(screen, self.color, (SCREEN_X - 1, 0), (SCREEN_X - 1, SCREEN_Y))

	def setMaterial(self, y, x, material):
		if (y >= 0 and y < len(self.grid)) and (x >= 0 and x < len(self.grid[y])):
			self.grid[y][x] = material(y, x)

class Particle:
	def __init__(self, y, x, color = None):
		self.x = x
		self.y = y
		self.color = color
		self.xScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.x
		self.yScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.y

	def moveMaterial(self, endY, endX, material, grid):
		if self.onGrid(endY, endX):
			if type(grid[endY][endX]) == Air:
				grid[self.y][self.x] = Air(self.y, self.x)
				grid[endY][endX] = material
				self.y = endY
				self.x = endX
	
	def onGrid(self, y, x):
		if x >= 0 and x < SCREEN_X//self.xScale and y >= 0 and y < SCREEN_Y//self.yScale:
			return True
		else:
			return False

	def draw(self, pos, screen):
		pygame.draw.circle(screen, self.color, pos, self.xScale//2)

class Air(Particle):
	def __init__(self, y, x):
		super().__init__(y, x)

	def update(self, grid):
		pass

class Sand(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (255, 200, 0))
	
	def moveMaterial(self, endY, endX, material, grid):
		super().moveMaterial(endY, endX, material, grid)
		if self.onGrid(endY, endX):
			if type(grid[endY][endX]) == Water:
				if random.randint(0, 100) % 2 == 0:
					tempStorage = grid[endY][endX]
					grid[endY][endX] = material
					grid[self.y][self.x] = tempStorage
					grid[self.y][self.x].y = self.y
					grid[self.y][self.x].x = self.x
					self.y = endY
					self.x = endX

	def update(self, grid):
		self.moveMaterial(self.y+1, self.x, self, grid)
		self.moveMaterial(self.y+1, self.x-1, self, grid)
		self.moveMaterial(self.y+1, self.x+1, self, grid)

class Water(Particle):
	def __init__(self, y, x):
		super().__init__(y, x, (255, 155, 155))#(0, 100, 255))
	
	def update(self, grid):
		self.moveMaterial(self.y+1, self.x, self, grid)
		self.moveMaterial(self.y+1, self.x-1, self, grid)
		self.moveMaterial(self.y+1, self.x+1, self, grid)
		self.moveMaterial(self.y, self.x-1, self, grid)
		self.moveMaterial(self.y, self.x+1, self, grid)
		self.moveMaterial(self.y, self.x-2, self, grid)
		self.moveMaterial(self.y, self.x+2, self, grid)