import pygame as pg
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

NORMAL_VIRUS = pg.image.load(os.path.join("assets", "red virus.jpg"))
VIRUS_ATTK = pg.image.load(os.path.join("assets", "infect.png"))
VIRUS_INIT_HEALTH = 1

VAC_SIZE = 40
VACCINE = pg.transform.scale(pg.image.load(os.path.join("assets",
                             "vaccine.png")), (VAC_SIZE, VAC_SIZE))
VAC_ATTK = pg.image.load(os.path.join("assets", "medicine.png"))
VAC_INIT_Y = 900
VAC_INIT_SPEED = 1
VAC_INIT_HEALTH = 100

class Vaccine(object):

    def __init__(self, x, y, speed = VAC_INIT_SPEED, effect = 1,
                 health = VAC_INIT_HEALTH, damage = VIRUS_INIT_HEALTH):
        self.x = x
        self.y = y
        self.speed = speed
        self.effect = effect
        self.health = health
        self.max_health = health
        self.damage = damage
        self.img = VACCINE
        self.med_img = VAC_ATTK
        self.med = []
        self.cd = 0
        self.mask = pg.mask.from_surface(VACCINE)

    def draw(self, win):
        win.blit(VACCINE, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()
        

class Virus(object):
    VARIANT_MAP = {
        "normal": (NORMAL_VIRUS, VIRUS_ATTK)
    }

    def __init__(self, x, y, variant, img, health = VIRUS_INIT_HEALTH):
        self.x = x
        self.y = y
        self.variant = variant
        self.img = img
        self.health = health
        self.max_health = health
        self.infect_img = None
        self.infects = []

    def draw(self, win):
        win.blit(VACCINE, (self.x, self.y))
        

def draw_start_menu(win, font):
    win.fill(BG_COLOR) # could add a background image
    
    name = font.render("Game Name", 1, FONT_COLOR)
    win.blit(name, (SCREEN_WIDTH / 2 - name.get_width() / 2, 
                    START_MENU_TEXT_SPACING))

    instr1 = font.render("Press 'Enter' to start the game", 1, FONT_COLOR)
    win.blit(instr1, (SCREEN_WIDTH / 2 - instr1.get_width() / 2, 
                      START_MENU_TEXT_SPACING * 2))

    instr2 = font.render("Press 'F1' for the list of controls", 1, FONT_COLOR)
    win.blit(instr2, (SCREEN_WIDTH / 2 - instr2.get_width() / 2, 
                      START_MENU_TEXT_SPACING * 3))

    pg.display.update()

def main():
    pg.init()
    win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("") # 想一个窗口的名字
    clock = pg.time.Clock()
    font = pg.font.SysFont(GAME_FONT, FONT_SIZE)

    level = 1
    game = False
    instr = False
    run = True
    while run:
        clock.tick(FRAME_RATES)
        draw_start_menu(win, font)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()

        if keys[pg.K_F1]:
            instr = True

        if keys[pg.K_RETURN]:
            game = True

        while instr:
            game = True

        vac = Vaccine(SCREEN_WIDTH / 2 - VACCINE.get_width() / 2, VAC_INIT_Y)
        start_time = time.time()
        while game:

            def draw_game():
                win.fill((0, 0, 0)) # add game backgrounf later
                vac.draw(win)

                pg.display.update()

            play_time = round(time.time() - start_time)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game = False
                    run = False

            keys = pg.key.get_pressed()

            if (keys[pg.K_a] or keys[pg.K_LEFT]) and vac.x - vac.speed >= 0:
                vac.x -= vac.speed
            if (keys[pg.K_d] or keys[pg.K_RIGHT]) and \
                vac.x + vac.speed + vac.get_width() <= SCREEN_WIDTH:
                vac.x += vac.speed
            if (keys[pg.K_w] or keys[pg.K_UP]) and vac.y - vac.speed >= 0:
                vac.y -= vac.speed
            if (keys[pg.K_s] or keys[pg.K_DOWN]) and \
                vac.y + vac.speed + vac.get_height() <= SCREEN_HEIGHT:
                vac.y += vac.speed

            draw_game()

    pg.quit()

if __name__ == '__main__':
    main()