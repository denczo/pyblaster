import pygame
import os

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

lcd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()
# background, scaled up
BACKGROUND = pygame.image.load('synth/synthlogic/icons/touchpad/touchpad.gif')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
# cursor
MANUAL_CURSOR = pygame.image.load('synth/synthlogic/icons/touchpad/cursor.png').convert_alpha()

cursor_width = MANUAL_CURSOR.get_rect().size[0]
cursor_height = MANUAL_CURSOR.get_rect().size[1]

while True:
    lcd.blit(BACKGROUND, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            print(pygame.mouse.get_pos())
            x, y = pygame.mouse.get_pos()
            lcd.blit(MANUAL_CURSOR, (x - cursor_width / 2, y - cursor_height / 2))
            pygame.display.update()



