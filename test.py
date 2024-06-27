import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((500,500))


def color_surface(surface, red, green, blue):
	arr = pygame.surfarray.pixels3d(surface)
	arr[:,:,0] = red
	arr[:,:,1] = green
	arr[:,:,2] = blue

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			raise SystemExit

	origSurface = pygame.image.load('img/0.png')
	origSurface = pygame.transform.scale(origSurface, (128, 128))
	origSurface.convert_alpha()

	coloredSurface = origSurface.copy()
	color_surface(coloredSurface, 255, 0, 0)

	screen.blit(coloredSurface, (250, 250))
	pygame.display.flip()

# import pickle
#
# save = False
# x = 0
# i = 0
#
# if save:
# 	with open('testing.pkl', 'wb') as f:
# 		while True:
# 			pickle.dump(x, f)
# 			print(x)
# 			x += 1
# 			if x > 1000:
# 				break
# else:
# 	with open('testing.pkl', 'rb') as f:
# 		while True:
# 			x = pickle.load(f)
# 			print(x)
# 			i += 1
# 			if i > 1000:
# 				break
