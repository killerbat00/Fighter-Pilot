import pygame
import random
import os.path
from global_constants import *
from game_objects import *
from pygame.locals import *
from sys import exit
from math import *
from MenuScreen import *

def main():
	pygame.init()
	showstartscreen()
	while True:
		runGame()

def draw_score(screen, score):
	scoreText = 'Score: ' 
	screenFont = pygame.font.Font('freesansbold.ttf', 14)
	screenSurf = screenFont.render('Press F for fullscreen', True, (255,0,255))
	scoreSurf = screenFont.render('Score: '+ str(score), True, (255,0,255))
	screen.blit(screenSurf, (1000, 756))
	screen.blit(scoreSurf, (1000, 770))

#create screen flash when enemy hits player
def screen_flash(screen, time):
	flash = pygame.Surface(SCREEN_SIZE)
	flash.fill((255,255,255))
	flash.set_alpha(200)
	screen.blit(flash, (0,0))

#calculate panning volume
def stereo_pan(x_coord, screen_width):
	right_volume = float(x_coord) / screen_width
	left_volume = 1.0 - right_volume
	return (left_volume, right_volume)

def runGame():
	#initialize
	pygame.init()
	pygame.mixer.init(44100,-16,2,1024*4)

	#various variables
	time_passed = clock.get_time()
	screen = pygame.display.set_mode((SCREEN_SIZE), FULLSCREEN, 32)
	screen_rect = pygame.Rect(0,0,1280,800)
	bullet = pygame.transform.scale((pygame.image.load(bullet_image).convert_alpha()), (10, 15))
	bullets = []
	for x in range(50):
		bullets.append(bullet)
	bulletposy = SCREEN_SIZE[1] -100
	bulletsizex = 20
	bulletsizey = 20
	headsupdisplay = HeadsUpDisplay()
	background1 = Background()
	enemy = Enemy()
	done = False
	angle = 0
	firedBullet = None
	score = 0
	blity = 630
	playerHealth = 250
	#explosion = Explosion()

	#Load & Initialize Sounds and Channels
	pygame.mixer.set_reserved(3)
	boom_sound = pygame.mixer.Sound(os.path.join('Sounds', 'boom.wav'))
	boom_channel = pygame.mixer.Channel(0)
	shoot_sound = pygame.mixer.Sound(os.path.join('Sounds', 'gun_shot.wav'))
	shoot_channel = pygame.mixer.Channel(1)
	enemy_channel = pygame.mixer.Channel(2)
	enemy_sound = pygame.mixer.Sound(os.path.join('Sounds', 'enemy_sound3.wav'))
	enemy_channel.set_volume(0.0,0.0)
	boom_sound.set_volume(1.0)
	shoot_sound.set_volume(1.0)
	volume_l = 0.15
	volume_r = 0.15

	#Joystick error checking.
	joystick_count = pygame.joystick.get_count()
	if joystick_count == 0:
		print("Error, I didn't find any joysticks!")
	else:
		my_joystick = pygame.joystick.Joystick(0)
		my_joystick.init()

	#Main game loop
	while done==False:
		time_passed = pygame.time.get_ticks()
		pressed_keys = pygame.key.get_pressed()
		pygame.key.set_repeat()
		pygame.mouse.set_visible(False)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
				done=True

		#Joystick controls
		if joystick_count > 0:
			horiz_axis_pos = my_joystick.get_axis(0)*10
			joystick_button = my_joystick.get_button(0)
			if horiz_axis_pos <= -2:
				background1.background_x += 15
				if enemy != None:
					enemy.x += 15
			if horiz_axis_pos >= 2:
				background1.background_x -= 15
				if enemy != None:
					enemy.x -=15
			if joystick_button == True:
				firedBullet = bullets.pop()
				shoot_channel.play(shoot_sound)

		#Keyboard controls
		if pressed_keys[K_ESCAPE]:
			exit()        	
		if pressed_keys[K_LEFT]:
			background1.background_x += 15
			if enemy != None:
				enemy.x += 15
		if pressed_keys[K_RIGHT]:
			background1.background_x -= 15
			if enemy != None:
				enemy.x-= 15
		if pressed_keys[K_DOWN]:
			firedBullet = bullets.pop()
			shoot_channel.play(shoot_sound)

		background1.checkbounds(screen, background1.background_x, background1.background_y)

		#draws enemy 
		if enemy != None:
			#play enemy sound
			enemy_channel.play(enemy_sound, -1)
			enemy_channel.set_volume(volume_l, volume_r)
			#checks enemy bounds, plays constant sound if enemy leaves screen
			if enemy.x > SCREEN_SIZE[0]:
				volume_r = volume_r
				volume_l = 0.0
			if enemy.x + enemy.sizex <= 0:
				volume_l = volume_l
				volume_r = 0.0

			#blits enemy
			enemy_rect = enemy.draw(screen, (enemy.x, enemy.y), enemy.sizex, enemy.sizey)

			#scales enemy and pans only when enemy is onscreen
			if screen_rect.contains(enemy_rect):
				#calculate panning
				volume_l, volume_r = stereo_pan(enemy.x, 1280)
				volume_l += .005
				volume_r += .005
				#calculate/update enemy size
				enemy.sizex += 1
				enemy.sizey = int(enemy.sizex/2.5)

			#Reduce health if enemy hits player plane
			if enemy.sizex >= 550:
				#screen_flash(screen)
				boom_channel.play(boom_sound)
				playerHealth -= 42
				volume_r = 0.0
				volume_l = 0.0
				enemy = None
				enemy_rect = None
				blity = 630
				enemy = Enemy()
				if playerHealth <= 0:
					gameOver()

		#Creates, scales and fires a bullet, ensures the bullets list remains full. 
		if firedBullet != None:
			bullet_rect = screen.blit(firedBullet, (SCREEN_SIZE[0]/2-10, bulletposy))
			bulletposy -= 25
			bulletsizex -=1
			bulletsizey -=1
			if bulletposy < 400:
				bulletposy = SCREEN_SIZE[1] - 100
				while len(bullets) < 50:
					bullets.append(firedBullet)
				firedBullet = None
  
			#Detect Bullet/Enemy collisions 
			if enemy_rect != None:
				if enemy_rect.colliderect(bullet_rect):
					enemy.health -= 1
					#enemy dies - reset!
					if enemy.health == 0:
						volume_l = 0.15
						volume_r = 0.15
						#explosionx = enemy.x
						#explosiony = enemy.y
						#explosion.update(screen, (explosionx, explosiony), time_passed)
						enemy = None
						enemy_rect = None
						boom_channel.play(boom_sound)
						score += 1
						enemy = Enemy()
						enemy.health = randint(5, 15)
						blity = 630
					bulletposy = SCREEN_SIZE[1]
					bulletsizex = 20
					bulletsizey = 20
					while len(bullets) < 50:
						bullets.append(firedBullet)
					firedBullet = None

		headsupdisplay.drawcircle(screen, angle)
		angle = headsupdisplay.updateangle(angle)

		#Draw enemy blit
		if enemy != None:
			blitx = enemy.x/10 + 580
			blity = enemy.sizex/4 + 620
			if blitx > 723:
				blitx = 723
			if blitx < 557:
				blitx = 557
			if blity >= 712:
				blity = 712
			enemyblit = pygame.draw.circle(screen, (255,0,0), (blitx, blity), 4)
		
		headsupdisplay.drawheadsup(screen)
		headsupdisplay.drawHealth(screen, playerHealth)
		draw_score(screen, score)

		clock.tick(FPS)
		pygame.display.update()

if __name__ == '__main__':
	main()