import pygame
from pygame import Vector2
from materials import Air, Particle
from globals import SCREEN_X, SCREEN_Y, SQUARE_SIZE

class Grid:
	def __init__(self, scale = SQUARE_SIZE, color = (255, 255, 255)):
		self.xScale = scale if type(scale) != Vector2 else scale.x
		self.yScale = scale if type(scale) != Vector2 else scale.y
		self.xTiles = SCREEN_X//self.xScale
		self.yTiles = SCREEN_Y//self.yScale
		self.color = color
		# self.treeScale = 50
		self.grid = [[Air(y, x) for x in range(self.xTiles)] for y in range(self.yTiles)]
		# self.tree = [[False for x in range(SCREEN_X//(self.xScale*self.treeScale))] for y in range(SCREEN_Y//(self.yScale*self.treeScale))]

	def update(self, screen):
		for y in range(len(self.grid)-1, 0, -1):
			for x in range(len(self.grid[y])):
				if type(self.grid[y][x]) != Air:
					self.grid[y][x].draw((x*self.xScale, y*self.yScale), screen)
					self.grid[y][x].update(self.grid)
					# self.tree[y//10][x//10] = True

		# for yTree in range(len(self.tree)-1, 0, -1):
		# 	for xTree in range(len(self.tree[yTree])):
		# 		if self.tree[yTree][xTree]:
		# 			for y in range(yTree*self.treeScale-1, 0, -1):
		# 				for x in range(xTree*self.treeScale):
		# 					if type(self.grid[y][x]) != Air:
		# 						self.grid[y][x].draw((x*self.xScale, y*self.yScale), screen)
		# 						self.grid[y][x].update(self.grid)
		# 						self.tree[y//self.treeScale][x//self.treeScale] = True

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
			# self.tree[y//self.treeScale][x//self.treeScale] = True