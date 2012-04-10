import pygame
from global_constants import *
from pygame.locals import *
from sys import exit

screen = pygame.display.set_mode((SCREEN_SIZE), 0, 32)
pygame.display.set_caption("Fighter Pilot V0.3")
icon = pygame.transform.scale(pygame.image.load(icon_image), (32, 32))
pygame.display.set_icon(icon)

def showstartscreen():
	pygame.init()
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Version 0.3', True, (40,40,40)).convert_alpha()
	titleFont = pygame.font.Font('freesansbold.ttf', 30)
	titleSurf2 = titleFont.render('Better title screen coming soon!', True, (255, 69, 0)).convert_alpha()
	center = titleSurf1.get_rect().center
	size1 = 101
	size2 = 571

	while True:
		screen.fill((1,1,1))
		rotatedSurf = pygame.transform.rotate(titleSurf2, 45)
		titleRect = titleSurf1.get_rect()
		rotatedRect = rotatedSurf.get_rect()
		rotatedRect.center = screen.get_rect().center
		titleRect.center = screen.get_rect().center
		screen.blit(titleSurf1, titleRect)
		screen.blit(rotatedSurf, rotatedRect)

		drawPressKeyMsg()

		if checkForKeyPresses():
			pygame.event.get()
			return
		pygame.display.update()
		clock.tick(FPS)

def gameOver():
	pygame.init()
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('GAME OVER!', True, (40, 40, 40)).convert_alpha()
	while True:
		screen.fill((1,1,1))
		titleRect = titleSurf1.get_rect()
		titleRect.center = screen.get_rect().center
		screen.blit(titleSurf1, titleRect)

		drawPressKeyMsg()

		if checkForKeyPresses():
			pygame.event.get()
			return
		pygame.display.update()
		clock.tick(FPS)

def drawPressKeyMsg():
	font = pygame.font.Font('freesansbold.ttf', 20)
	pressKeySurf = font.render('Press Any Key to Play.', True, (40,40,40))
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (SCREEN_SIZE[0]-300, SCREEN_SIZE[1] - 100)
	screen.blit(pressKeySurf, pressKeyRect)

def checkForKeyPresses():
	if len(pygame.event.get(QUIT)) > 0:
		pygame.quit()
		exit()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		pygame.quit()
		exit()
	return keyUpEvents[0].key