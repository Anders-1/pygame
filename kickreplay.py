# NOTE: Just copy kick.py and make the changes made in replay.py when compared to firstgame.py (use text-compare.com)
# (I think you just change dump to load and remove player input)
# Also make it so enemies can't spawn on top of the player and add pixel perfect collisions


import pygame
import random
import pickle

pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


screen = pygame.display.set_mode((500,500))

pos = [250, 250]
pos2 = [190, 250]


score = 40
speed_cooldown = -1
speed_delay = -1

pygame.mixer.music.load("sound/ost.wav")
pygame.mixer.music.play(-1)
pop = pygame.mixer.Sound("sound/pop.wav")
oof = pygame.mixer.Sound("sound/oof.wav")
bing = pygame.mixer.Sound("sound/bing.wav")


#
save = True
framerate = 60
framerate_multiplier = 0.25
gamemode = 1
start_speed = 4
show_fps = True
two_players = False
enemy_num = 4
speed_multiplier = 4
speed_length = 25
speed_cooldown_length = 200 + 1
debug = False
show_cooldown = True
show_boost_left = True
speed_increase = 10000
current_frame = 0
hold_frame = 0
frame_length = 5
frames = 2
flipped = False
scale_x = 64
scale_y = 64
#

clock = pygame.time.Clock()

def animate_player(x, y, flip):
	global hold_frame
	global current_frame
	if hold_frame == frame_length:
		hold_frame = 0
		if current_frame == frames:
			current_frame = 0
		else:
			current_frame += 1
	else:
		hold_frame += 1
	player_img = pygame.image.load('img/' + str(current_frame) + ".png")
	if flip:
		player_img = pygame.transform.flip(player_img, True, False)
	player_img = pygame.transform.scale(player_img, (scale_x, scale_y))
	player = player_img.get_rect()
	screen.blit(player_img, (x, y))
	return player


def closest_player(ex, ey, p1x, p1y, p2x, p2y):

	min([p1x, p2x], key=lambda x:abs(x-ex))
	min([p1y, p2y], key=lambda x:abs(x-ey))


def cooldown_text(x):
	if x > -1:
		if show_boost_left:
			return "BOOSTING: " + str(abs(x))
		else:
			return "BOOSTING"
	elif x == -1:
		return "READY"
	elif x < -1:
		return "WAITING: " + str(abs(x))

def rand_decimal(x, y, z = 100):
	x = round(x)
	y = round(y)
	z = round(z)
	# for num in [x, y, z]:
	# 	num = round(num)

	return random.randint(x * z, y * z) / z

def make_enemies(x):
	enemies = []
	for i in range(x):
		enemies.append([random.randint(10, 450), random.randint(-10, 125), random.randint(3, 5), rand_decimal(1, 2), rand_decimal(2, 3), 1])
	return enemies

enemies = make_enemies(enemy_num)

def randomize(pos, variation):
	pos[0] = rand_decimal(pos[0] - variation, pos[0] + variation)
	pos[1] = rand_decimal(pos[1] - variation, pos[1] + variation)
	return pos

def find_player(px, py, ex, ey, change, variation):
	pos = randomize([ex, ey], variation)
	if ex > px:
		pos[0] -= change
	else:
		pos[0] += change
	if ey > py:
		pos[1] -= change
	else:
		pos[1] += change
	return pos

with open('savegame.pkl', 'rb') as f:
	while True:
		try:
			enemies = pickle.load(f)
			pos = pickle.load(f)
			score = pickle.load(f)
			speed_cooldown = pickle.load(f)
		except:
			pygame.quit()
			raise SystemExit

		# Process player inputs.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit

		# Do logical updates here.
		# ...
		# rate = 1
		keys = pygame.key.get_pressed()
		framerate = 60
		if keys[pygame.K_a]:
			framerate = framerate * framerate_multiplier
		if keys[pygame.K_d]:
			framerate = framerate * (1/framerate_multiplier)
		if keys[pygame.K_w]:
			framerate = 1
		if keys[pygame.K_s]:
			framerate = 960
		# if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (speed_cooldown > 0 or speed_cooldown == -1):
		# 	if speed_cooldown == -1:
		# 		speed_cooldown = speed_length
		# 	speed_cooldown -= rate
		# 	speed = start_speed * speed_multiplier
		# elif speed_cooldown == 0 and not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
		# 		speed_cooldown = -1
		# 		speed = start_speed
		# else:
		# 	if speed_cooldown == 0:
		# 		speed_cooldown = 0 - speed_cooldown_length
		# 	# elif speed_cooldown == -2:
		# 	# 	speed_cooldown = -1
		# 	if speed_cooldown + 1 <= -1:
		# 		speed_cooldown += rate
		# 	speed = start_speed
		#
		#
		# if keys[pygame.K_a]:
		# 	flipped = True
		# 	pos[0] -= speed
		# 	if pos[0] < 0:
		# 		pos[0] = 0
		# if keys[pygame.K_d]:
		# 	flipped = False
		# 	pos[0] += speed
		# 	if pos[0] > 450:
		# 		pos[0] = 450
		# if keys[pygame.K_w]:
		# 	pos[1] -= speed
		# 	if pos[1] < 0:
		# 		pos[1] = 0
		# if keys[pygame.K_s]:
		# 	pos[1] += speed
		# 	if pos[1] > 450:
		# 		pos[1] = 450
		#
		# if two_players:
		# 	if keys[pygame.K_LEFT]:
		# 		pos2[0] -= speed
		# 		if pos2[0] < 0:
		# 			pos2[0] = 0
		# 	if keys[pygame.K_RIGHT]:
		# 		pos2[0] += speed
		# 		if pos2[0] > 450:
		# 			pos2[0] = 450
		# 	if keys[pygame.K_UP]:
		# 		pos2[1] -= speed
		# 		if pos2[1] < 0:
		# 			pos2[1] = 0
		# 	if keys[pygame.K_DOWN]:
		# 		pos2[1] += speed
		# 		if pos2[1] > 450:
		# 			pos2[1] = 450

		screen.fill("white")  # Fill the display with a solid color
		# Render the graphics here.
		# ...
		# player = pygame.draw.rect(screen, (255, 0, 0),
		# 	pygame.Rect(pos[0], pos[1], 60,60))
		player = animate_player(pos[0], pos[1], flipped)
		player_collision = pygame.Rect(pos[0], pos[1], scale_x, scale_y)
		if two_players:
			player2 = pygame.draw.rect(screen, (0, 255, 0),
				pygame.Rect(pos2[0], pos2[1], 60,60))

		if score > 2500 and score < 2505:
			pygame.mixer.Sound.play(bing)
		elif score > 3500 and score < 3505:
			pygame.mixer.Sound.play(oof)


		for enemy in enemies:
			# if gamemode == 1:
				# enemy[3] += score / speed_increase

			if enemy[1] > 500 or enemy[0] == "X":
				pygame.mixer.Sound.play(pop)
				score += 1
				# scale_x += 1
				enemy[0] = random.randint(10, 450)
				enemy[1] = random.randint(10, 100)
				enemy[2] = random.randint(1, 5)
				enemy[3] = random.randint(1, 2)
				enemy[4] = random.randint(2, 5)
				if random.randint(1, 10) == 1:
					enemy[5] += 1
			else:
				if gamemode == 0:
					enemy[1] += enemy[2]
				elif gamemode == 1:
					go_to = find_player(pos[0], pos[1], enemy[0], enemy[1], enemy[3], enemy[4])
					enemy[0] = go_to[0]
					enemy[1] = go_to[1]
			if score / 50 > enemy[5]:
				rect = pygame.draw.rect(screen, (0, 0, 255),
					pygame.Rect(enemy[0], enemy[1], 60,60))
			else:
				rect = pygame.draw.rect(screen, (100 + (enemy[5] * 10), 0, 0),
					pygame.Rect(enemy[0], enemy[1], 60,60))
			# if score / 50 > enemy[5]:
			# 	enemy_check = my_font.render("X", False, (0, 0, 0))
			# 	screen.blit(enemy_check, (enemy[0] + 20, enemy[1] + 20))
			if two_players:
				if player.colliderect(rect) or player2.colliderect(rect):
					score = 0
					speed_cooldown = -1
					speed_delay = -1
					enemies = make_enemies(enemy_num)
			else:
				if player_collision.colliderect(rect):
					if score / 50 > enemy[5]:
						enemy[0] = "X"
					else:
						score = 40
						speed_cooldown = -1
						speed_delay = -1
						enemies = make_enemies(enemy_num)

		score_text = my_font.render(str(round(score)), False, (0, 0, 0))
		if show_fps:
			fps = my_font.render(str(round(clock.get_fps())), False, (0, 0, 0))
			screen.blit(fps, (450,10))
		if debug:

			#
			print(enemies[0])
			var = speed_cooldown
			#

			debug = my_font.render(str(var), False, (0, 0, 0))
			screen.blit(debug, (230,10))
		if show_cooldown:
			cooldown_screen = my_font.render(cooldown_text(speed_cooldown), False, (0, 0, 0))
			screen.blit(cooldown_screen, (80,10))
		if gamemode == 1:
			score += 1/60
		clock.tick(framerate)         # wait until next frame (at 60 FPS)
		screen.blit(score_text, (10,10))
		pygame.display.flip()  # Refresh on-screen display
