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
	
	def drawheadsup(self, screen):
		screen.blit(self.headsup, (0,0))

	def drawcircle(self, screen, angle): 
		screen.blit(self.headsup, (0,0))
		circlerect = pygame.Rect(0,0,165,165)
		circlerect2 = pygame.Rect(0,0,170,170)
		circlerect.center = (640,712)
		circlerect2.center = (640, 712)
		circle2 = pygame.draw.ellipse(screen, (255,255,255), circlerect2, 0)
		self.circle = pygame.draw.ellipse(screen, (0,0,0), circlerect,  2)
		x = 82*math.sin(angle)+640
		y = 82*math.cos(angle)+712
		pygame.draw.line(screen, (0,255,0), (640, 712), (x, y), 2)

	def drawHealth(self, screen, health):
		text = "Health"
		font = pygame.font.Font('freesansbold.ttf', 14)
		surf = font.render(text, True, (255,0,255))
		screen.blit(surf, (205, 729))
		barRect = pygame.Rect(200, 745, 250, 50)
		healthRect = pygame.Rect(210, 755, health - 20, 30)
		pygame.draw.rect(screen, (0,0,0), barRect)
		pygame.draw.rect(screen, (255,0,0), healthRect)


	def updateangle(self, angle):
		angle += .05
		pi = 3.141592653
		if angle > 2*pi:
			angle = angle - 2*pi
		return angle

class Background():
	def __init__(self):
		self.background = pygame.image.load(background_image_file).convert_alpha()
		self.background_rect = self.background.get_rect()
		self.background_y = 0
		self.background_x = 0

	def checkbounds(self, screen, x, y):
		if self.background_x <-1280:
			self.background_x = 0
		if self.background_x >0:
			self.background_x = -1280
		screen.blit(self.background, (x, y))

class Enemy:
	def __init__(self):
		self.enemy = pygame.image.load(enemy_image).convert_alpha()
		self.sizex = 50
		self.sizey = 20
		self.enemy = pygame.transform.scale(self.enemy, (self.sizex, self.sizey))
		self.rect = self.enemy.get_rect()
		self.x = randint(-1280,1280)
		self.y = SCREEN_SIZE[1]/2
		self.health = randint(3, 7)

	def draw(self, screen, (x, y), sizex, sizey):
		if sizex >= 550:
			sizex = 550
			sizey = 180

		scaledenemy = pygame.transform.scale(pygame.image.load(enemy_image).convert_alpha(), (sizex, sizey))
		x -= sizex/2
		screen.blit(scaledenemy, (x, y))
		rect = pygame.Rect(x, y, sizex, sizey)
		return rect

	def get_location(self):
		return (self.x, self.y)


##NON WORKING EXPLOSION CLASS
class Explosion:
	defaultlife = 12
	animcycle = 3
	images = []

	def __init__(self, time):
		for x in range (1,12):
			image = pygame.image.load(os.path.join("Graphics", "Explosion%d.png") %x).convert_alpha()
			image = pygame.transform.scale(image, (200,200))
			self.images.append(image)
		self.life = self.defaultlife
		self.starttime = time

	def update(self, screen, (x,y), time):

		while (time - self.starttime < 2000):
			self.image = self.images[self.life//self.animcycle%2]
			screen.blit(self.image, (x,y))
			break
		#self.life = self.life - 1
		#self.image = self.images[self.life//self.animcycle%2]
		#screen.blit(self.image, (x, y))