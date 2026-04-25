import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

player_img = pygame.image.load("C:/Users/Nurali/Documents/nnnp2/pp2/practice 10/racer/images/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 80))

enemy_img = pygame.image.load("C:/Users/Nurali/Documents/nnnp2/pp2/practice 10/racer/images/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 80))
enemy_img = pygame.transform.rotate(enemy_img, 180)

road_img = pygame.image.load("C:/Users/Nurali/Documents/nnnp2/pp2/practice 10/racer/images/road.png").convert()
road_img = pygame.transform.scale(road_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

player = player_img.get_rect()
player.x = 275
player.y = 600

enemy = enemy_img.get_rect()
enemy.x = random.randint(80, 470)
enemy.y = -100

coins = []
for i in range(5):
    coin = pygame.Rect(random.randint(80, 500), random.randint(-600, 0), 20, 20)
    coins.append(coin)

road_y1 = 0
road_y2 = -SCREEN_HEIGHT

speed = 5
score = 0
font = pygame.font.SysFont("Verdana", 20)
game_over = False

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED:
            speed += 0.5

    if not game_over:

        road_y1 += speed
        road_y2 += speed

        if road_y1 >= SCREEN_HEIGHT:
            road_y1 = -SCREEN_HEIGHT
        if road_y2 >= SCREEN_HEIGHT:
            road_y2 = -SCREEN_HEIGHT

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x > 80:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x < 520 - player.width:
            player.x += 5
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y < SCREEN_HEIGHT - player.height:
            player.y += 5

        enemy.y += speed

        if enemy.y > SCREEN_HEIGHT:
            enemy.y = -100
            enemy.x = random.randint(80, 470)

        if player.colliderect(enemy):
            game_over = True

        for coin in coins:
            coin.y += speed

            if coin.y > SCREEN_HEIGHT:
                coin.y = random.randint(-600, 0)
                coin.x = random.randint(80, 500)

            if player.colliderect(coin):
                score += 1
                coin.y = random.randint(-600, 0)
                coin.x = random.randint(80, 500)

        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)

        for coin in coins:
            pygame.draw.circle(screen, YELLOW, coin.center, 10)

        draw_text(f"Coins: {score}", 440, 10)
        draw_text(f"Speed: {speed:.1f}", 440, 35)

    else:
        draw_text("GAME OVER", 220, 300, RED)
        draw_text(f"Score: {score}", 250, 350, BLACK)

    pygame.display.update()