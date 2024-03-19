import pygame
from pygame import Vector2
from grid import Grid
from materials import Sand, Air
import math
from globals import SCREEN_X, SCREEN_Y, SQUARE_SIZE

def better_round(val:float, n_digits:int = 0):
    val *= 10**n_digits
    result = int(val + (0.50002 if val >= 0 else -0.50002))
    return result / 10**n_digits

class Mouse:
	def __init__(self):
		self.pos = pygame.mouse.get_pos()
		self.xScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.x
		self.yScale = SQUARE_SIZE if type(SQUARE_SIZE) != Vector2 else SQUARE_SIZE.y
		self.material = Sand
		self.brushSize = 20

	def update(self, world : Grid):
		if pygame.mouse.get_pressed()[0]:
			self.pos = Vector2(pygame.mouse.get_pos())

			xStart = int(better_round((self.pos.x - self.brushSize//2)/self.xScale))
			yStart = int(better_round((self.pos.y - self.brushSize//2)/self.yScale))
			#to prevent cases where the range would be 0, these if statements make it so that there's always at least 1 case in the range.
			tempXEnd = int(better_round((self.pos.x + self.brushSize//2)/self.xScale))
			xEnd = tempXEnd if tempXEnd != xStart else xStart + 1
			tempYEnd = int(better_round((self.pos.y + self.brushSize//2)/self.yScale))
			yEnd = tempYEnd if tempYEnd != yStart else yStart + 1

			for y in range(yStart, yEnd):
				for x in range(xStart, xEnd):
					spawnedParticles = 0
					if spawnedParticles <= 10:
						xPos = x * self.xScale + self.xScale//2
						yPos = y * self.yScale + self.yScale//2
						if math.sqrt((xPos - self.pos.x)**2 + (yPos - self.pos.y)**2) <= self.brushSize//2 and (x >= 0 and x < len(world.grid[y]) and y >= 0 and y < len(world.grid) and type(world.grid[y][x]) == Air):
							world.setMaterial(y, x, self.material)