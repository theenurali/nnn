#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Нужно для main.py
WIDTH  = 400
HEIGHT = 600

#Other Variables for use in the program
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
TOTAL_COINS = 0
OBSTACLE_DELAY = 2000
shield_active = False
oil_active = False
active_powerup = None
powerup_end_time = 0
POWERUP_TIMEOUT = 5000
level = 1
level_up = 0
velocity = 5
distance = 0

#Setting up Fonts
font       = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over  = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\AnimatedStreet.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\Enemy (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED-1)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\coins.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)
        self.value = random.choice([1, 2, 3])

    def move(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > 600:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["oil", "barrier"])
        if self.kind == "oil":
            self.image = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\oil.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\barrier.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED-2)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        if self.kind == "nitro":
            path = r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\nitro.png"
        elif self.kind == "shield":
            path = r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\shield.png"
        else:
            path = r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\repair.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > POWERUP_TIMEOUT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\Player (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -velocity)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, velocity)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-velocity, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(velocity, 0)


def play_game(screen, username):
    global SPEED, SCORE, TOTAL_COINS, OBSTACLE_DELAY
    global shield_active, oil_active, active_powerup
    global powerup_end_time, level, level_up, velocity, distance

    SPEED          = 5
    SCORE          = 0
    TOTAL_COINS    = 0
    OBSTACLE_DELAY = 2000
    shield_active  = False
    oil_active     = False
    active_powerup = None
    powerup_end_time = 0
    level    = 1
    level_up = 0
    velocity = 5
    distance = 0
    oil_end_time = 0

    pygame.mixer.music.load(r'C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\lofi.wav')
    pygame.mixer.music.play(-1)

    P1 = Player()
    E1 = Enemy()
    C1 = Coins()
    O1 = Obstacle()
    N1 = PowerUp()

    enemies     = pygame.sprite.Group(E1)
    coins       = pygame.sprite.Group(C1)
    obstacles   = pygame.sprite.Group(O1)
    powerups    = pygame.sprite.Group(N1)
    all_sprites = pygame.sprite.Group(P1, E1, C1, O1, N1)

    INC_SPEED    = pygame.USEREVENT + 1
    ADDCOIN      = pygame.USEREVENT + 2
    ADD_OBSTACLE = pygame.USEREVENT + 3
    ADD_POWERUP  = pygame.USEREVENT + 4

    pygame.time.set_timer(INC_SPEED,    5000)
    pygame.time.set_timer(ADDCOIN,      1500)
    pygame.time.set_timer(ADD_OBSTACLE, OBSTACLE_DELAY)
    pygame.time.set_timer(ADD_POWERUP,  7000)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == INC_SPEED:
                SPEED += 0.5

            if event.type == ADDCOIN:
                new_coin = Coins()
                coins.add(new_coin)
                all_sprites.add(new_coin)

            if event.type == ADD_OBSTACLE:
                new_obstacle = Obstacle()
                x = random.randint(40, SCREEN_WIDTH - 40)
                while abs(x - P1.rect.centerx) < 60:
                    x = random.randint(40, SCREEN_WIDTH - 40)
                new_obstacle.rect.centerx = x
                new_obstacle.rect.top = 0
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)

            if event.type == ADD_POWERUP:
                if len(powerups) == 0:
                    new_powerup = PowerUp()
                    powerups.add(new_powerup)
                    all_sprites.add(new_powerup)

        now = pygame.time.get_ticks()

        if oil_active and now > oil_end_time:
            velocity = 5
            oil_active = False
        if active_powerup == "nitro" and now > powerup_end_time:
            velocity = 5
            active_powerup = None

        distance += SPEED * 0.05

        screen.blit(background, (0, 0))
        screen.blit(font_small.render(str(SCORE),         True, BLACK), (10, 10))
        screen.blit(font_small.render(str(TOTAL_COINS),   True, BLACK), (10, 30))
        screen.blit(font_small.render(str(int(distance)), True, BLACK), (30, 50))

        if active_powerup:
            if active_powerup == "nitro":
                remaining = max(0, (powerup_end_time - now) // 1000)
                pu_text = font_small.render(f"Power: NITRO {remaining}s", True, BLACK)
            else:
                pu_text = font_small.render("Power: SHIELD", True, BLACK)
            screen.blit(pu_text, (10, 70))

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
            entity.move()

        # COIN COLLECTION
        collected = pygame.sprite.spritecollide(P1, coins, True)
        if collected:
            pygame.mixer.Sound(r'C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\coins.wav').play()
            TOTAL_COINS += collected[0].value

        if TOTAL_COINS // 5 > level_up:
            level    += 1
            level_up  = TOTAL_COINS // 5
            SPEED    += 0.5
            OBSTACLE_DELAY = max(500, OBSTACLE_DELAY - 200)
            pygame.time.set_timer(ADD_OBSTACLE, OBSTACLE_DELAY)

        # obstacle collision
        hit_obs = pygame.sprite.spritecollide(P1, obstacles, True)
        if hit_obs:
            for obs in hit_obs:
                if obs.kind == "oil":
                    oil_active   = True
                    oil_end_time = now + 2000
                    velocity     = max(2, velocity - 3)
                elif obs.kind == "barrier":
                    if shield_active:
                        shield_active = False
                    else:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound(r'C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\crash.wav').play()
                        time.sleep(0.5)
                        return TOTAL_COINS * 10 + int(distance), distance

        # powerup
        hit_powerup = pygame.sprite.spritecollide(P1, powerups, True)
        if hit_powerup and active_powerup is None:
            pu = hit_powerup[0]
            if pu.kind == "nitro":
                active_powerup   = "nitro"
                velocity         = 8
                powerup_end_time = now + 2000
            elif pu.kind == "shield":
                active_powerup   = "shield"
                shield_active    = True
                powerup_end_time = 0
            elif pu.kind == "repair":
                if len(obstacles) > 0:
                    random.choice(obstacles.sprites()).kill()

        # enemy collision
        if pygame.sprite.spritecollideany(P1, enemies):
            if shield_active:
                shield_active = False
                E1.rect.top = 0
                E1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            else:
                pygame.mixer.music.stop()
                pygame.mixer.Sound(r'C:\Users\Nurali\Documents\nnnp2\pp2\TSIS\tsis3\materials\crash.wav').play()
                time.sleep(0.5)
                screen.fill(RED)
                screen.blit(game_over, (30, 250))
                pygame.display.update()
                for entity in all_sprites:
                    entity.kill()
                time.sleep(2)
                return TOTAL_COINS * 10 + int(distance), distance  # ← вместо pygame.quit()

        pygame.display.update()
        FramePerSec.tick(FPS)


# Запуск напрямую без main.py
if __name__ == "__main__":
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Racer Game")
    play_game(DISPLAYSURF, "Player")
    pygame.quit()