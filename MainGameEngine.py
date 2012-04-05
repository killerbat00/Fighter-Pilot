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

def runGame():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_SIZE), 0, 32)
	screen_rect = pygame.Rect(0,0,1280,800)
	bullet = pygame.transform.scale((pygame.image.load(bullet_image).convert_alpha()), (20, 20))
	bullets = []
	for x in range(50):
		bullets.append(bullet)
	bulletposy = SCREEN_SIZE[1]
	bulletsizex = 20
	bulletsizey = 20
	enemysizex = 100
	enemysizey = 100
	headsupdisplay = HeadsUpDisplay()
	background1 = Background()
	enemy = Enemy()
	done = False
	angle = 0
	firedBullet = None
	score = 0
	blity = 630
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

		background1.checkbounds()
		background1.draw_rotated(screen, background1.background_x, background1.background_y, score)

		#draws enemy 
		if enemy != None:
			enemy.draw(screen, (enemy.x, enemy.y))
			enemy_rect = pygame.Rect(enemy.x, enemy.y, 100, 100)
			

		#Creates, scales and fires a bullet, ensures the bullets list remains full. 
		if firedBullet != None:
			scaledBullet = pygame.transform.scale(firedBullet, (bulletsizex, bulletsizey))
			#scaledBullet = firedBullet
			bullet_rect = screen.blit(scaledBullet, (SCREEN_SIZE[0]/2-10, bulletposy))
			bulletposy -= 30
			bulletsizex -=1
			bulletsizey -=1
			if bulletposy < 400:
				bulletposy = SCREEN_SIZE[1]
				bulletsizex = 20
				bulletsizey = 20
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
					bulletposy = SCREEN_SIZE[1]
					bulletsizex = 20
					bulletsizey = 20
					while len(bullets) < 50:
						bullets.append(firedBullet)
					firedBullet = None


		#scaledenemy = pygame.transform.scale(enemy, (enemysizex, enemysizey))
		#screen.blit(scaledenemy, (enemyposx, enemyposy))
		#screen.blit(enemy, (enemyposx, enemyposy))
		headsupdisplay.draw(screen, angle)
		if enemy != None:
			blitx = enemy.x/10 + 580
			if blitx > 723:
				blitx = 723
			if blitx < 557:
				blitx = 557
			if blity >= 712:
				blity = 712
			enemyblit = pygame.draw.circle(screen, (255,0,0), (blitx, blity), 4, 0)
		if enemy == None:
			blity = 630
		blity += 1
		angle = headsupdisplay.updateangle(angle)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == '__main__':
	main()