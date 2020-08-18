import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FONT_B = pygame.font.SysFont("comicsans", 32)
FONT_D = pygame.font.SysFont("comicsans", 25)
FONT_S = pygame.font.SysFont("comicsans", 18)
BOTTOMBARHEIGHT = 180
BOXWIDTH = 100
BRUSHSIZE = 10
MAXBRUSHSIZE = 50

WHITE = (255, 255, 255)
LIGHTGREY = (200, 200, 200)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
CURRENTCOLOR = BLACK


def draw_window(win):
    win.fill(LIGHTGREY, (0, HEIGHT - BOTTOMBARHEIGHT, WIDTH, BOTTOMBARHEIGHT))
    pygame.draw.rect(win, BLACK, (15, HEIGHT - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    pygame.draw.rect(win, CURRENTCOLOR,(40, HEIGHT - BOTTOMBARHEIGHT + 40, BOXWIDTH - 50, BOXWIDTH - 50)) # 50=(40-15)*2
    square_text = FONT_D.render("Square Pen", 1, BLACK)
    win.blit(square_text, (15 + BOXWIDTH - square_text.get_width(), HEIGHT - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.rect(win, BLACK, (15 + BOXWIDTH + 15 + 15, HEIGHT - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    circle_text = FONT_D.render("Circle Pen", 1, BLACK)
    win.blit(circle_text, (15 + BOXWIDTH + BOXWIDTH + 15 + 4 - circle_text.get_width(), HEIGHT - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.circle(win, CURRENTCOLOR, (15 + BOXWIDTH + 15 + 15 + BOXWIDTH//2, HEIGHT - BOTTOMBARHEIGHT + 15 + BOXWIDTH//2), 25)
    pygame.draw.rect(win, GREY, (WIDTH - 25 - 240, HEIGHT - BOTTOMBARHEIGHT + 25, 240, 15))  # (735, 845, 240, 15)
    pygame.draw.circle(win, WHITE, (BRUSHSIZE*(240//MAXBRUSHSIZE)+735, 845 + 15//2), 12)
    size_text = FONT_D.render("Choose Brush Size", 1, BLACK)
    win.blit(size_text, (855 - size_text.get_width()//2, HEIGHT - BOTTOMBARHEIGHT + 25 + 15 + 5))



def main(win, width, height):
    win.fill(WHITE)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win)
        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
