import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL, 0)
next_direction = direction

FOOD_TYPES = [
    {"value": 1, "color": RED, "weight": 60, "time": 300},   # обычная
    {"value": 2, "color": BLUE, "weight": 30, "time": 200},  # средняя
    {"value": 3, "color": (255,215,0), "weight": 10, "time": 120},  # редкая
]

def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            ftype = random.choices(FOOD_TYPES, weights=[f["weight"] for f in FOOD_TYPES])[0]
            return {
                "pos": (x, y),
                "value": ftype["value"],     # сколько очков
                "color": ftype["color"],     # цвет еды
                "timer": ftype["time"]       # сколько живёт (кадры)
            }

food = spawn_food()

score = 0
level = 1
speed = 8

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                next_direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                next_direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                next_direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                next_direction = (CELL, 0)

    direction = next_direction
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False
    if head in snake:
        running = False

    snake.insert(0, head)
    food["timer"] -= 1
    if food["timer"] <= 0:
        food = spawn_food()  
    if head == food["pos"]:
        score += food["value"]
        food = spawn_food()
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))
    pygame.draw.rect(screen, food["color"], (*food["pos"], CELL, CELL))
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()