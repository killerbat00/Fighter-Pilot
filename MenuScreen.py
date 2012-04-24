import pygame
from global_constants import *
from pygame.locals import *
from sys import exit

screen = pygame.display.set_mode((SCREEN_SIZE), FULLSCREEN, 32)
pygame.display.set_caption("Fighter Pilot V0.3")
icon = pygame.transform.scale(pygame.image.load(icon_image), (32, 32))
pygame.display.set_icon(icon)

def showstartscreen():
	pygame.init()
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Version 1.0', True, (40,40,40)).convert_alpha()
	titleFont = pygame.font.Font('freesansbold.ttf', 250)
	titleSurfupper = titleFont.render('Fighter', True, (0, 255, 0)).convert_alpha()
	titleSurflower = titleFont.render('Pilot', True, (0, 255, 0)).convert_alpha()
	center = titleSurf1.get_rect().center
	size1 = 101
	size2 = 571

	while True:
		screen.fill((1,1,1))
		titleRect = titleSurf1.get_rect()
		titleupperRect = titleSurfupper.get_rect()
		titleupperRect.midtop = screen.get_rect().midtop
		titlelowerRect = titleSurflower.get_rect()
		titleRect.center = screen.get_rect().center
		screen.blit(titleSurf1, titleRect)
		screen.blit(titleSurfupper, titleupperRect)
		screen.blit(titleSurflower, ((SCREEN_SIZE[0]/2)-272, SCREEN_SIZE[1]-251))

		drawPressKeyMsg('begin')

		if checkForKeyPresses():
			pygame.event.get()
			return
		pygame.display.update()
		clock.tick(FPS)

def gameOver():
	pygame.init()
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('GAME OVER!', True, (40, 40, 40)).convert_alpha()
	titleFont = pygame.font.Font('freesansbold.ttf', 300)
	titleSurfupper = titleFont.render('GAME', True, (0,255,0)).convert_alpha()
	titleSurflower = titleFont.render('OVER!', True, (0,255,0)).convert_alpha()

	while True:
		screen.fill((1,1,1))
		pygame.mouse.set_visible(True)
		titleRect = titleSurf1.get_rect()
		titlelowerRect = titleSurflower.get_rect()
		titleupperRect = titleSurfupper.get_rect()
		titleupperRect.midtop = screen.get_rect().midtop
		titleRect.center = screen.get_rect().center
		screen.blit(titleSurf1, titleRect)
		screen.blit(titleSurfupper, titleupperRect)
		screen.blit(titleSurflower, ((SCREEN_SIZE[0]/2)-475, SCREEN_SIZE[1]-301))

		drawPressKeyMsg('end')		

		if checkForKeyPresses():
			pygame.event.get()
			return
		pygame.display.update()
		clock.tick(FPS)

def drawPressKeyMsg(input):
	font = pygame.font.Font('freesansbold.ttf', 20)

	if input == 'begin':
		pressKeySurf = font.render('Press Any Key to Play.', True, (40,40,40))
		pressKeyRect = pressKeySurf.get_rect()
		pressKeyRect.topleft = (SCREEN_SIZE[0]-300, SCREEN_SIZE[1] - 100)
		screen.blit(pressKeySurf, pressKeyRect)
	else:
		pressKeySurf = font.render('Press Any Key to Replay.', True, (40,40,40))
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