import pygame, sys, math
from datetime import datetime
pygame.init()
W, H = 900, 600
UI_H = 70
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint Final")
WHITE = (255,255,255)
BLACK = (0,0,0)
canvas = pygame.Surface((W, H-UI_H))
canvas.fill(WHITE)
tool = "pencil"
color = BLACK
size = 2
drawing = False
start = last = (0,0)
font = pygame.font.SysFont(None, 22)
# --- UI ---
palette = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,165,0)]
sizes = [2,5,10]

# --- text tool ---
typing = False
text = ""
text_pos = (0,0)

# --- flood fill ---
def flood_fill(surface, pos, new_color):
    target = surface.get_at(pos)
    if target == new_color:
        return
    stack = [pos]
    while stack:
        x,y = stack.pop()
        if 0 <= x < W and 0 <= y < H-UI_H:
            if surface.get_at((x,y)) == target:
                surface.set_at((x,y), new_color)
                stack += [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

def draw_ui():
    pygame.draw.rect(screen, (200,200,200), (0,0,W,UI_H))

    # colors
    for i,c in enumerate(palette):
        r = pygame.Rect(10+i*40,10,30,30)
        pygame.draw.rect(screen,c,r)
        if c == color:
            pygame.draw.rect(screen,(0,0,0),r,3)

    # sizes
    for i,s in enumerate(sizes):
        r = pygame.Rect(300+i*50,10,40,30)
        pygame.draw.rect(screen,(150,150,150),r)
        txt = font.render(str(s),True,BLACK)
        screen.blit(txt,(r.x+10,r.y+5))
        if s == size:
            pygame.draw.rect(screen,(0,0,0),r,3)
    txt = font.render("P pencil | L line | R rect | C circle | S square | Q/E tri | D rhomb | F fill | T text | Ctrl+S save",True,BLACK)
    screen.blit(txt,(10,45))
clock = pygame.time.Clock()
while True:
    screen.blit(canvas,(0,UI_H))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas,name)
            if e.key == pygame.K_1: size = 2
            if e.key == pygame.K_2: size = 5
            if e.key == pygame.K_3: size = 10
            if e.key == pygame.K_p: tool="pencil"
            if e.key == pygame.K_l: tool="line"
            if e.key == pygame.K_r: tool="rect"
            if e.key == pygame.K_c: tool="circle"
            if e.key == pygame.K_s: tool="square"
            if e.key == pygame.K_q: tool="rtri"
            if e.key == pygame.K_e: tool="etri"
            if e.key == pygame.K_d: tool="rhomb"
            if e.key == pygame.K_f: tool="fill"
            if e.key == pygame.K_t: tool="text"
            if typing:
                if e.key == pygame.K_RETURN:
                    img = font.render(text,True,color)
                    canvas.blit(img,text_pos)
                    typing=False
                    text=""
                elif e.key == pygame.K_ESCAPE:
                    typing=False
                    text=""
                elif e.key == pygame.K_BACKSPACE:
                    text=text[:-1]
                else:
                    text+=e.unicode

        if e.type == pygame.MOUSEBUTTONDOWN:
            x,y = e.pos
            if y < UI_H:

                for i,c in enumerate(palette):
                    if pygame.Rect(10+i*40,10,30,30).collidepoint(e.pos):
                        color=c

                for i,s in enumerate(sizes):
                    if pygame.Rect(300+i*50,10,40,30).collidepoint(e.pos):
                        size=s

                continue

            y -= UI_H

            if tool=="fill":
                flood_fill(canvas,(x,y),color)

            elif tool=="text":
                typing=True
                text_pos=(x,y)
                text=""

            else:
                drawing=True
                start=last=(x,y)

        if e.type == pygame.MOUSEBUTTONUP and drawing:
            drawing=False
            x1,y1=start
            x2,y2=(e.pos[0], e.pos[1]-UI_H)

            if tool=="line":
                pygame.draw.line(canvas,color,start,(x2,y2),size)

            elif tool=="rect":
                pygame.draw.rect(canvas,color,(min(x1,x2),min(y1,y2),abs(x1-x2),abs(y1-y2)),size)

            elif tool=="circle":
                r=int(math.hypot(x2-x1,y2-y1))
                pygame.draw.circle(canvas,color,start,r,size)

            elif tool=="square":
                s=min(abs(x2-x1),abs(y2-y1))
                pygame.draw.rect(canvas,color,(x1,y1,s,s),size)

            elif tool=="rtri":
                pygame.draw.polygon(canvas,color,[(x1,y1),(x1,y2),(x2,y2)],size)

            elif tool=="etri":
                b=abs(x2-x1)
                h=b*math.sqrt(3)/2
                pygame.draw.polygon(canvas,color,[(x1,y1),(x1+b,y1),(x1+b/2,y1-h)],size)

            elif tool=="rhomb":
                cx,cy=(x1+x2)//2,(y1+y2)//2
                pygame.draw.polygon(canvas,color,[(cx,y1),(x2,cy),(cx,y2),(x1,cy)],size)

        if e.type == pygame.MOUSEMOTION and drawing:
            x,y=e.pos
            y-=UI_H
            if tool=="pencil":
                pygame.draw.line(canvas,color,last,(x,y),size)
                last=(x,y)
    if drawing and tool=="line":
        mx,my=pygame.mouse.get_pos()
        pygame.draw.line(screen,color,(start[0],start[1]+UI_H),(mx,my),size)
    if typing:
        img=font.render(text,True,color)
        screen.blit(img,(text_pos[0],text_pos[1]+UI_H))
    draw_ui()

    pygame.display.update()
    clock.tick(60)