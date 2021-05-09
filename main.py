import pygame as pg
import random
import os
import time

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 600
BG_COLOR = (0, 0, 0)
FRAME_RATES = 60

MENU_FONT = "comicsans"
MENU_SIZE = 40
START_MENU_TEXT_SPACING = 150

GAME_FONT = "comicsans"
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)
LVL_POS = (10, 10)

LOST_MSG_Y = 400
LOST_MSG_SPACING = 100
LOST_PAUSE_TIME = 3

INIT_LIVES = 3
WAV_INCRMT = 5
DOUBLE_HEALTH_WAVE = 10

NRML_SIZE = 40
VIR_BU_SIZE = 40
VIR_BU_VEL = 0.3
VIR_BU_PROB = FRAME_RATES * 4
VIR_BU_CD = FRAME_RATES * 20
NORMAL_VIRUS = pg.transform.scale(pg.image.load(os.path.join("assets", 
                                                             "red virus.png")),
                                  (NRML_SIZE, NRML_SIZE))
INDIA_VIRUS = pg.transform.scale(pg.image.load(os.path.join("assets", 
                                                             "blue virus.png")),
                                 (NRML_SIZE, NRML_SIZE))
VIRUS_ATTK = pg.transform.scale(pg.image.load(os.path.join("assets", 
                                                           "infect.png")),
                                (VIR_BU_SIZE, VIR_BU_SIZE))

VARIANT_MAP = {
    "normal": (NORMAL_VIRUS, VIRUS_ATTK),
    "india": (INDIA_VIRUS, VIRUS_ATTK)
}

VIRUS_INIT_HEALTH = 1
VIRUS_DAMAGE = 15
VIRUS_SPAWN_RANGE_X = (50, SCREEN_WIDTH - 50)
VIRUS_SPAWN_RANGE_Y = (-800, -50)
VIRUS_SPEED_GAP = 100
VIRUS_SPEED_RANGE = (10, 20)

VAC_SIZE = 40
VAC_BU_SIZE = 25
VAC_BU_VEL = -3
VACCINE = pg.transform.scale(pg.image.load(os.path.join("assets",
                             "vaccine.png")), (VAC_SIZE, VAC_SIZE))
VAC_ATTK = pg.transform.scale(pg.image.load(os.path.join("assets", 
                                                         "medicine.png")),
                              (VAC_BU_SIZE, VAC_BU_SIZE))
VAC_INIT_Y = 900
VAC_INIT_SPEED = 1
VAC_INIT_HEALTH = 100

HEALTH_BAR_SHIFT = 10
HEALTH_BAR_HEIGHT = 5

PROP_DROP_PROB = 1
CAPSULE = pg.image.load(os.path.join("assets", "capsule.png"))
CAP_HP_REC = 10
SHIELD = pg.image.load(os.path.join("assets", "shield.png"))

PROP_MAP = {
    'medicine': CAPSULE,
    'shield': SHIELD
}

PROP_TIME = 10 * FRAME_RATES
SHIELD_TIME = 5 * FRAME_RATES

class Prop(object):

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.img = PROP_MAP[kind]
        self.mask = pg.mask.from_surface(self.img)
        self.prop_clock = PROP_TIME
        self.shield_clock = SHIELD_TIME


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        self.prop_clock -= 1

    def effect(obj):
        if self.kind == "medicine":
            obj.health += CAP_HP_REC
        else: pass  #若道具为shield需要在掉血位置加一条判断，if 碰撞 and shield_clock:
                                                        #则只要碰撞效果，不掉血，未找到这部分代码所以未添加


class Entity(object):
    CD = FRAME_RATES // 2
    
    def __init__(self, x, y, speed, health, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.max_health = health
        self.damage = damage
        self.img = None
        self.attk_img = None
        self.attks = []
        self.cd = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        for attk in self.attks:
            attk.draw(win)

    def move_bullet(self, vel, obj):
        self.cooldown()
        for attk in self.attks:
            attk.move(vel)
            if attk.off_screen(SCREEN_HEIGHT):
                self.attks.remove(attk)
            elif attk.collision(obj):
                obj.health -= self.damage
                self.attks.remove(attk)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def cooldown(self):
        if self.cd >= self.CD:
            self.cd = 0
        elif self.cd > 0:
            self.cd += 1

    def shoot(self):
        if self.cd == 0:
            bullet = Bullet(self.x + self.get_width() / 2 - \
                            self.attk_img.get_width() / 2, 
                            self.y, self.attk_img)
            self.attks.append(bullet)
            self.cd = 1

    def draw_health_bar(self, win):
        pg.draw.rect(win, (255, 0, 0), 
                     (self.x, self.y + self.get_height() + HEALTH_BAR_SHIFT,
                      self.get_width(), HEALTH_BAR_HEIGHT))
        pg.draw.rect(win, (0, 255, 0), 
                     (self.x, self.y + self.get_height() + HEALTH_BAR_SHIFT,
                      self.get_width() * (self.health / self.max_health), 
                      HEALTH_BAR_HEIGHT))


class Vaccine(Entity):

    def __init__(self, x, y, speed = VAC_INIT_SPEED, effect = 1,
                 health = VAC_INIT_HEALTH, damage = VIRUS_INIT_HEALTH):
        super().__init__(x, y, speed, health, damage)
        self.effect = effect
        self.damage = damage
        self.img = VACCINE
        self.attk_img = VAC_ATTK
        self.mask = pg.mask.from_surface(self.img)

    def move_bullet(self, vel, objs, props):
        self.cooldown()
        for attk in self.attks:
            attk.move(vel)
            if attk.off_screen(SCREEN_HEIGHT):
                self.attks.remove(attk)
            else:
                for obj in objs:
                    if attk.collision(obj):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            prop = get_prop(obj.x, obj.y)
                            if prop:
                                props.append(prop)
                            objs.remove(obj)
                        self.attks.remove(attk)

    def draw(self, win):
        super().draw(win)
        self.draw_health_bar(win)
        
    
class Virus(Entity):
    CD = VIR_BU_CD

    def __init__(self, x, y, speed, variant, health,
                 damage = VIRUS_DAMAGE):
        super().__init__(x, y, speed, health, damage)
        self.variant = variant
        self.img, self.attk_img = VARIANT_MAP[variant]
        self.mask = pg.mask.from_surface(self.img)

    def move(self):
        self.y += self.speed
        x_move = random.choice([-1, 0, 1])
        if x_move > 0 and \
           self.x + self.speed + self.img.get_width() < SCREEN_WIDTH:
            self.x += self.speed
        elif x_move < 0 and self.x - self.speed > 0:
            self.x -= self.speed

    def draw_health_bar(self, win):
        pg.draw.rect(win, (255, 0, 0), 
                     (self.x, self.y - HEALTH_BAR_SHIFT,
                      self.get_width(), HEALTH_BAR_HEIGHT))
        pg.draw.rect(win, (0, 255, 0), 
                     (self.x, self.y - HEALTH_BAR_SHIFT,
                      self.get_width() * (self.health / self.max_health), 
                      HEALTH_BAR_HEIGHT))

    def draw(self, win):
        super().draw(win)
        self.draw_health_bar(win)


class Bullet():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pg.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return self.y > height or self.y < 0

    def collision(self, obj):
        return collide(obj, self)
 

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def get_random(range):
    min, max = range
    return random.randrange(min, max)

def get_prop(x, y):
    #if random.randrange(0, PROP_DROP_PROB) == 1:
    return Prop(x, y, random.choice(list(PROP_MAP.keys())))

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

def draw_lost(win, font):
    lost_msg = font.render("YOU LOST!", 1, FONT_COLOR)
    win.blit(lost_msg, (SCREEN_WIDTH / 2 - lost_msg.get_width() / 2,
                        LOST_MSG_Y))
    lost_msg = font.render("Please wear your mask", 1, FONT_COLOR)
    win.blit(lost_msg, (SCREEN_WIDTH / 2 - lost_msg.get_width() / 2,
                        LOST_MSG_Y + LOST_MSG_SPACING))
    lost_msg = font.render("and practice social distancing!", 1, FONT_COLOR)
    win.blit(lost_msg, (SCREEN_WIDTH / 2 - lost_msg.get_width() / 2,
                        LOST_MSG_Y + LOST_MSG_SPACING * 2))

def draw_game(win, font, viruses, vac, lost, lives, level):
    win.fill((0, 0, 0)) # add game backgrounf later

    lives_label = font.render(f"Lives: {lives}", 1, FONT_COLOR)
    level_label = font.render(f"Level: {level}", 1, FONT_COLOR)

    win.blit(lives_label, (SCREEN_WIDTH - lives_label.get_width() - 10, 10))
    win.blit(level_label, LVL_POS)

    for virus in viruses:
        virus.draw(win)

    vac.draw(win)

    if lost:
        draw_lost(win, font)

    pg.display.update()

def game(win):
    clock = pg.time.Clock()
    font = pg.font.SysFont(GAME_FONT, FONT_SIZE)
    
    level = 0
    lives_remaining = INIT_LIVES
    amount_per_wave = 0

    lost = False
    lost_count = 0

    vac = Vaccine(SCREEN_WIDTH / 2 - VACCINE.get_width() / 2, VAC_INIT_Y)
    viruses = []
    props = []

    #start_time = time.time()

    run = True
    while run:
        #play_time = round(time.time() - start_time)

        draw_game(win, font, viruses, vac, lost, lives_remaining, level)

        if lives_remaining <= 0 or vac.health <= 0:
            lost = True

        if lost:
            if lost_count > FRAME_RATES * LOST_PAUSE_TIME:
                run = False
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.KEYDOWN or \
                       event.type == pg.MOUSEBUTTONDOWN:
                        return
                continue

        for prop in props:
            if prop.prop_clock > 0:
                prop.draw(win)
                if collide(vac, prop):
                    props.remove(prop)
            else:
                props.remove(prop)

        if len(viruses) == 0:
            level += 1
            amount_per_wave += WAV_INCRMT
            for i in range(amount_per_wave):
                virus = Virus(get_random(VIRUS_SPAWN_RANGE_X), 
                              get_random(VIRUS_SPAWN_RANGE_Y), # could use a dynamic method with level
                              get_random(VIRUS_SPEED_RANGE) / VIRUS_SPEED_GAP,
                              random.choice(list(VARIANT_MAP.keys())),
                              VIRUS_INIT_HEALTH * \
                                  (level % DOUBLE_HEALTH_WAVE + 1))
                viruses.append(virus)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        keys = pg.key.get_pressed()

        if (keys[pg.K_a] or keys[pg.K_LEFT]) and vac.x - vac.speed >= 0:
            vac.x -= vac.speed
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and \
            vac.x + vac.speed + vac.get_width() <= SCREEN_WIDTH:
            vac.x += vac.speed
        if (keys[pg.K_w] or keys[pg.K_UP]) and vac.y - vac.speed >= 0:
            vac.y -= vac.speed
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and \
            vac.y + vac.speed + vac.get_height() + \
            HEALTH_BAR_HEIGHT + HEALTH_BAR_SHIFT <= SCREEN_HEIGHT:
            vac.y += vac.speed
        if keys[pg.K_SPACE]:
            vac.shoot()

        for virus in viruses:
            virus.move()
            virus.move_bullet(VIR_BU_VEL, vac)

            if random.randrange(0, VIR_BU_PROB) == 1:
                virus.shoot()

            if collide(virus, vac):
                vac.health -= virus.damage
                viruses.remove(virus)
            elif virus.y + virus.get_height() > SCREEN_HEIGHT:
                lives_remaining -= 1
                viruses.remove(virus) 


        vac.move_bullet(VAC_BU_VEL, viruses, props)

def main():
    pg.init()

    win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("") # 想一个窗口的名字

    menu_font = pg.font.SysFont(MENU_FONT, MENU_SIZE)

    run = True
    while run:
        draw_start_menu(win, menu_font)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    game(win)
                if event.key == pg.K_F1:
                    pass
    
    pg.quit()


if __name__ == '__main__':
    main()