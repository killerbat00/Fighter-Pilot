import pygame
import math
from random import *
from pygame.locals import *
from global_constants import *

class Bullet:
	def __init__(self, x, y):
		self.bullet = pygame.transform.scale((pygame.image.load(bullet_image).convert_alpha()), (20, 20))
		self.speed = 20
		self.x = SCREEN_SIZE[0]/2-10
		self.y = SCREEN_SIZE[1]
		self.bullet_size_x = self.bullet.get_size()[0]
		self.bullet_size_y = self.bullet.get_size()[1]
	def getrect(self):
		return self.bullet.get_rect()

class HeadsUpDisplay:
	def __init__(self):
		self.headsup = pygame.image.load(HUD_image).convert_alpha()
		self.angle = 0
	
	def draw(self, screen, angle): 
		screen.blit(self.headsup, (0,0))
		circlerect = pygame.Rect(0,0,165,165)
		circlerect2 = pygame.Rect(0,0,170,170)
		circlerect.center = (640,712)
		circlerect2.center = (640, 712)
		circle2 = pygame.draw.ellipse(screen, (139,137,137), circlerect2, 0)
		self.circle = pygame.draw.ellipse(screen, (0,255,0), circlerect,  2)
		x = 82*math.sin(angle)+640
		y = 82*math.cos(angle)+712
		pygame.draw.line(screen, (0,255,0), (640, 712), (x, y), 2)

	def updateangle(self, angle):
		angle += .05
		pi = 3.141592653
		if angle > 2*pi:
			angle = angle - 2*pi
		return angle


class Background():
	def __init__(self):
		self.background = pygame.image.load(background_image_file).convert()
		self.background_rect = self.background.get_rect()
		self.background_y = 0
		self.background_x = 0


	def draw_rotated(self, screen, x, y, score):
		scoreText = 'Score: ' 
		screenFont = pygame.font.Font('freesansbold.ttf', 14)
		screenSurf = screenFont.render('Press F for fullscreen.', True, (1,1,1))
		scoreSurf = screenFont.render('Score: '+ str(score), True, (1,1,1))
		screen.blit(self.background, (x, y))
		screen.blit(screenSurf, (1000, 14))
		screen.blit(scoreSurf, (1000, 30))

	def checkbounds(self):
		if self.background_x <-1280:
			self.background_x = 0
		if self.background_x >0:
			self.background_x = -1280
class Enemy:
	def __init__(self):
		self.enemy = pygame.image.load(enemy_image).convert_alpha()
		self.enemy = pygame.transform.scale(self.enemy, (100, 100))
		self.rect = self.enemy.get_rect()
		self.x = randint(-1280,1280)
		self.y = SCREEN_SIZE[1]/2
		self.health = randint(5, 15)

	def draw(self, screen, (x, y)):
		screen.blit(self.enemy, (x, y))

	def get_rect(self):
		return self.enemy.get_rect()

	def get_location(self):
		return (self.x, self.y)
