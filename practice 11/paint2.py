import pygame, math
pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

WHITE, BLACK = (255,255,255), (0,0,0)
RED, GREEN, BLUE = (255,0,0), (0,255,0), (0,0,255)
GRAY = (200,200,200)

screen.fill(WHITE)

tool = "draw"
color = BLACK
drawing = False
start = last = (0,0)

font = pygame.font.SysFont(None, 22)

buttons = {
    "draw": pygame.Rect(10,10,80,30),
    "rect": pygame.Rect(100,10,80,30),
    "circle": pygame.Rect(190,10,80,30),
    "eraser": pygame.Rect(280,10,80,30),
    "square": pygame.Rect(370,10,80,30),
    "rtri": pygame.Rect(460,10,80,30),
    "etri": pygame.Rect(10,50,80,30),
    "rhomb": pygame.Rect(100,50,80,30),
}

colors = {
    BLACK: pygame.Rect(200,50,30,30),
    RED: pygame.Rect(240,50,30,30),
    GREEN: pygame.Rect(280,50,30,30),
    BLUE: pygame.Rect(320,50,30,30),
}

def draw_ui():
    for name, r in buttons.items():
        pygame.draw.rect(screen, GRAY, r)
        screen.blit(font.render(name, True, BLACK), (r.x+5, r.y+5))
    for c, r in colors.items():
        pygame.draw.rect(screen, c, r)

running = True
while running:
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            x,y = e.pos

            for name, r in buttons.items():
                if r.collidepoint(x,y):
                    tool = name

            for c, r in colors.items():
                if r.collidepoint(x,y):
                    color = c
            if y > 100:
                drawing = True
                start = last = e.pos


        if e.type == pygame.MOUSEBUTTONUP:
            if drawing: 
                drawing = False
                x1,y1 = start
                x2,y2 = e.pos

                if tool == "rect":
                    pygame.draw.rect(screen, color,
                        (min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)), 2)

                if tool == "square":
                    side = min(abs(x2-x1), abs(y2-y1))
                    pygame.draw.rect(screen, color, (x1, y1, side, side), 2)

                if tool == "circle":
                    r = int(math.hypot(x2-x1, y2-y1))
                    pygame.draw.circle(screen, color, start, r, 2)

                if tool == "rtri":
                    pygame.draw.polygon(screen, color,
                        [(x1,y1), (x1,y2), (x2,y2)], 2)

                if tool == "etri":
                    base = abs(x2-x1)
                    h = base * math.sqrt(3) / 2
                    pygame.draw.polygon(screen, color,
                        [(x1,y1), (x1+base,y1), (x1+base/2, y1-h)], 2)

                if tool == "rhomb":
                    cx, cy = (x1+x2)//2, (y1+y2)//2
                    pygame.draw.polygon(screen, color,
                        [(cx,y1), (x2,cy), (cx,y2), (x1,cy)], 2)
        if e.type == pygame.MOUSEMOTION and drawing:
            if tool == "draw":
                pygame.draw.line(screen, color, last, e.pos, 3)
            if tool == "eraser":
                pygame.draw.line(screen, WHITE, last, e.pos, 10)

            last = e.pos
    draw_ui()
    pygame.display.update()
    clock.tick(60)

pygame.quit()