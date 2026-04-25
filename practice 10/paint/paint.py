import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint App - Fixed Smooth Drawing")

clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

screen.fill(WHITE)

tool = "draw"  
color = BLACK

drawing = False
start_pos = (0, 0)
last_pos = None

font = pygame.font.SysFont(None, 24)

buttons = {
    "rect": pygame.Rect(10, 10, 140, 30),
    "circle": pygame.Rect(160, 10, 140, 30),
    "draw": pygame.Rect(310, 10, 140, 30),
    "eraser": pygame.Rect(460, 10, 140, 30),
}

colors = {
    "black": pygame.Rect(10, 50, 30, 30),
    "red": pygame.Rect(50, 50, 30, 30),
    "green": pygame.Rect(90, 50, 30, 30),
    "blue": pygame.Rect(130, 50, 30, 30),
}


def draw_ui():
    for name, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 7))

    pygame.draw.rect(screen, BLACK, colors["black"])
    pygame.draw.rect(screen, RED, colors["red"])
    pygame.draw.rect(screen, GREEN, colors["green"])
    pygame.draw.rect(screen, BLUE, colors["blue"])


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

       
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # инструмент тандау
            for name, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    tool = name

            if colors["black"].collidepoint(mx, my):
                color = BLACK
            if colors["red"].collidepoint(mx, my):
                color = RED
            if colors["green"].collidepoint(mx, my):
                color = GREEN
            if colors["blue"].collidepoint(mx, my):
                color = BLUE

            
            if my > 100:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

      
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                end_pos = event.pos
                last_pos = None

               
                if tool == "rect":
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(
                            min(start_pos[0], end_pos[0]),
                            min(start_pos[1], end_pos[1]),
                            abs(start_pos[0] - end_pos[0]),
                            abs(start_pos[1] - end_pos[1]),
                        ),
                        2,
                    )

                
                elif tool == "circle":
                    radius = int(math.hypot(
                        end_pos[0] - start_pos[0],
                        end_pos[1] - start_pos[1]
                    ))

                    pygame.draw.circle(screen, color, start_pos, radius, 2)

        
        if event.type == pygame.MOUSEMOTION:

            if drawing and tool == "draw":
                if last_pos is not None:
                    pygame.draw.line(screen, color, last_pos, event.pos, 3)
                last_pos = event.pos

            elif drawing and tool == "eraser":
                if last_pos is not None:
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, 12)
                last_pos = event.pos

    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()