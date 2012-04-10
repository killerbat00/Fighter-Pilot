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
	screenSurf = screenFont.render('Press F for fullscreen', True, (255,255,255))
	scoreSurf = screenFont.render('Score: '+ str(score), True, (255,255,255))
	screen.blit(screenSurf, (1000, 756))
	screen.blit(scoreSurf, (1000, 770))

def runGame():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_SIZE), 0, 32)
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

	while done==False:
		time_passed = pygame.time.get_ticks()/1000
		pressed_keys = pygame.key.get_pressed()
		rotation_direction = 0
		background_rotation_direction = 0
		pygame.key.set_repeat()
		pygame.mouse.set_visible(False)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
				done=True

		if pressed_keys[K_ESCAPE]:
			exit()        	
		if pressed_keys[K_f]:
			screen = pygame.display.set_mode((SCREEN_SIZE),FULLSCREEN,32)
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

		background1.checkbounds(screen, background1.background_x, background1.background_y)
		#background1.draw_rotated(screen, background1.background_x, background1.background_y, score)

		#draws enemy 
		if enemy != None:
			enemy_rect = enemy.draw(screen, (enemy.x, enemy.y), enemy.sizex, enemy.sizey)
			if screen_rect.contains(enemy_rect):
				enemy.sizex += 1
				enemy.sizey += 1
			#Reduce health if enemy hits player plane
			if enemy.sizex >= 400:
				playerHealth -= 42
				enemy = None
				enemy_rect = None
				blity = 630
				enemy = Enemy()
				if playerHealth <= 0:
					gameOver()

		#Creates, scales and fires a bullet, ensures the bullets list remains full. 
		if firedBullet != None:
			bullet_rect = screen.blit(firedBullet, (SCREEN_SIZE[0]/2-10, bulletposy))
			bulletposy -= 20
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
					if enemy.health == 0:
						enemy = None
						enemy_rect = None
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
			enemyblit = pygame.draw.circle(screen, (255,0,0), (blitx, blity), 4, 0)
		angle = headsupdisplay.updateangle(angle)
		headsupdisplay.drawheadsup(screen)
		headsupdisplay.drawHealth(screen, playerHealth)
		draw_score(screen, score)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == '__main__':
	main()