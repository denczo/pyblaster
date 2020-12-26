import pygame
import os
import time


class Touchscreen:
    def __init__(self):
        pass


    # Colors
    BLUE = (0, 255, 0)
    WHITE = (255, 255, 255)

    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
    pygame.init()
    pygame.mouse.set_visible(True)

    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 320

    lcd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # draw text
    font = pygame.font.Font(None, 50)
    text = font.render("TEST", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    lcd.blit(text, text_rect)
    lcd.fill(BLUE)
    pygame.display.update()
    pygame.display.update()

    print("as")
    while True:
        if pygame.mouse.get_pressed():
            x, y = pygame.mouse.get_pos()
            print(x, y)
            time.sleep(0.1)



