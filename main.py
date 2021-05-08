import pygame
import random
import os
import time

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 600
BG_COLOR = (0, 0, 0)
FRAME_RATES = 60

GAME_FONT = "comicsans"
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)
START_MENU_TEXT_SPACING = 150

INIT_HEALTH = 100
INIT_AMMO = 100

class Player(object):

    def __init__(self, x, y, health, ammo):
        self.x = x
        self.y = y
        self.health = health
        self.ammo = ammo

class Enemy(object):

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health

def draw_start_menu(win):
    win.fill(BG_COLOR)
    font = pygame.font.SysFont(GAME_FONT, FONT_SIZE)

    name = font.render("Game Name", 1, FONT_COLOR)
    win.blit(name, (SCREEN_WIDTH / 2 - name.get_width() / 2, 
                    START_MENU_TEXT_SPACING))

    instr1 = font.render("Press 'Enter' to start the game", 1, FONT_COLOR)
    win.blit(instr1, (SCREEN_WIDTH / 2 - instr1.get_width() / 2, 
                      START_MENU_TEXT_SPACING * 2))

    instr2 = font.render("Press 'F1' for the list of controls", 1, FONT_COLOR)
    win.blit(instr2, (SCREEN_WIDTH / 2 - instr2.get_width() / 2, 
                      START_MENU_TEXT_SPACING * 3))

    pygame.display.update()

def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("") # 想一个窗口的名字
    clock = pygame.time.Clock()

    start_time = time.time()
    game = False
    instr = False
    run = True
    while run:
        clock.tick(FRAME_RATES)
        draw_start_menu(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = True
                    break
                elif event.key == pygame.K_F1:
                    instr = True
                    break

        while instr:
            pass
             
        while game:
            play_time = round(time.time() - start_time)




    pygame.quit()

if __name__ == '__main__':
    main()