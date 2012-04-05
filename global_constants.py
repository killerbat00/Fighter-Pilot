import pygame, os
from pygame.locals import *


SCREEN_SIZE = (1280,800)
FPS = 40
clock = pygame.time.Clock()
TIME_PASSED = clock.tick(FPS)
ENEMY_RELOAD = 40
background_image_file = os.path.join('Graphics' ,'extended_sky.png')
bullet_image = os.path.join('Graphics', 'shot.gif')
enemy_image = os.path.join('Graphics', 'enemy.png')
HUD_image = os.path.join('Graphics', 'HUD1.png')
icon_image = os.path.join('Graphics', 'tardis.png')
SCORE = 0