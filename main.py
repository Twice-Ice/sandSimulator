import pygame
from pygame import Vector2
from grid import Grid
from materials import Air, Sand, Water
from mouse import Mouse
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, SQUARE_SIZE
pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("Snake")

doExit = False
clock = pygame.time.Clock()

world = Grid(color = (255, 155, 155))
player = Mouse()
possibleMaterials = [
	Sand,
	Water,
]

print(SCREEN_X/ SQUARE_SIZE)

cooldown = 0

while not doExit:
	delta = clock.tick(60) / 1000
	screen.fill(BG_COLOR)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_p]:
		for y in range(len(world.grid)):
			for x in range(len(world.grid[y])):
				if type(world.grid[y][x]) != Air:
					print(world.grid[y][x], end="")
				else:
					print(" ", end="")
			print()
		print("----------------------------------")
	if keys[pygame.K_o]:
		for y in range(len(world.tree)):
			for x in range(len(world.tree[y])):
				print(str(world.tree[y][x])[0], end="")
			print()
	if keys[pygame.K_UP] and cooldown == 0:
		player.material = possibleMaterials[possibleMaterials.index(player.material) + 1] if possibleMaterials.index(player.material) + 1 < len(possibleMaterials) else possibleMaterials[0]
		cooldown = 25
		print(player.material)

	world.update(screen)
	player.update(world)


	cooldown = cooldown - 1 if cooldown > 0 else 0
	pygame.display.flip()
pygame.quit()