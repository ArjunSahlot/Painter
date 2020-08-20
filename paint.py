import math

import pygame
import os
import colorsys

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Painter, By: Arjun Sahlot")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))

# Fonts
FONT_B = pygame.font.SysFont("comicsans", 30)
FONT_D = pygame.font.SysFont("comicsans", 25)
FONT_S = pygame.font.SysFont("comicsans", 23)

# Constants
BOTTOMBARHEIGHT = 180
BOXWIDTH = 100
SMALLERBOXWIDTH = 70
BRUSHSIZE = 10
MAXBRUSHSIZE = 50

# Images
ERASER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "eraser_icon.png")), (SMALLERBOXWIDTH, SMALLERBOXWIDTH))
CLEAR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clear_screen.png")), (SMALLERBOXWIDTH - 14, SMALLERBOXWIDTH - 14))
PICKER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "color_picker.png")), (170, 170))
SLIDER = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
COLORPOS = (85, 85)
VALUEPOS = (555, 880)


def get_color(colorpos, valuepos):
    hsv_col = rgb_to_hsv(PICKER.get_at(colorpos))
    hue = hsv_col[0]
    sat = hsv_col[1]
    val = rgb_to_hsv(SLIDER.get_at(valuepos))[2]
    color = hsv_to_rgb((hue, sat, val))
    return color


def hsv_to_rgb(color):
    color = colorsys.hsv_to_rgb(color[0] / 255, color[1] / 255, color[2] / 255)
    return color[0] * 255, color[1] * 255, color[2] * 255


def rgb_to_hsv(color):
    color = colorsys.rgb_to_hsv(color[0] / 255, color[1] / 255, color[2] / 255)
    return color[0] * 255, color[1] * 255, color[2] * 255


# Colors
WHITE = (255, 255, 255)
LIGHTGREY = (200, 200, 200)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)


CURRENTCOLOR = get_color(COLORPOS, VALUEPOS)


def draw_window(win, width, height):
    win.fill(LIGHTGREY, (0, height - BOTTOMBARHEIGHT, width, BOTTOMBARHEIGHT))
    pygame.draw.rect(win, BLACK, (15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    pygame.draw.rect(win, CURRENTCOLOR if not close_to_white() else BLACK, (40, height - BOTTOMBARHEIGHT + 40, BOXWIDTH - 50, BOXWIDTH - 50)) # 50=(40-15)*2
    square_text = FONT_D.render("Square Pen", 1, BLACK)
    win.blit(square_text, (15 + BOXWIDTH - square_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.rect(win, BLACK, (15 + BOXWIDTH + 15 + 15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    circle_text = FONT_D.render("Circle Pen", 1, BLACK)
    win.blit(circle_text, (15 + BOXWIDTH + BOXWIDTH + 15 + 4 - circle_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.circle(win, CURRENTCOLOR if not close_to_white() else BLACK, (15 + BOXWIDTH + 15 + 15 + BOXWIDTH//2, height - BOTTOMBARHEIGHT + 15 + BOXWIDTH//2), 25)
    pygame.draw.rect(win, GREY, (width - 25 - 240, height - BOTTOMBARHEIGHT + 25, 240, 15))  # (735, 845, 240, 15)
    pygame.draw.circle(win, WHITE, (BRUSHSIZE*(240//MAXBRUSHSIZE)+735, 845 + 15//2), 12)
    size_text = FONT_D.render("Brush Size", 1, BLACK)
    win.blit(size_text, (855 - size_text.get_width()//2, height - BOTTOMBARHEIGHT + 25 + 15 + 5))
    pygame.draw.rect(win, BLACK, (735 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height(), SMALLERBOXWIDTH, SMALLERBOXWIDTH), 5)
    win.blit(ERASER, (735 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height()))
    eraser_text = FONT_S.render("Eraser", 1, BLACK)
    win.blit(eraser_text, (735 + SMALLERBOXWIDTH//2 - eraser_text.get_width()//2 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + SMALLERBOXWIDTH + 5))
    pygame.draw.rect(win, BLACK, (975 - SMALLERBOXWIDTH - 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height(), SMALLERBOXWIDTH, SMALLERBOXWIDTH), 5)
    win.blit(CLEAR, (975 - SMALLERBOXWIDTH - 10 + 7, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + 7))
    clear_text = FONT_S.render("Clear Screen", 1, BLACK)
    win.blit(clear_text, (975 - SMALLERBOXWIDTH//2 - clear_text.get_width()//2 - 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + SMALLERBOXWIDTH + 5))
    win.blit(PICKER, (15 + BOXWIDTH*2 + 15 + 15 + 80, height - BOTTOMBARHEIGHT + 5))
    pygame.draw.circle(win, WHITE, (COLORPOS[0] + 15 + BOXWIDTH*2 + 15 + 15 + 80, COLORPOS[1] + height - BOTTOMBARHEIGHT + 5), 5)
    pygame.draw.circle(win, BLACK, (COLORPOS[0] + 15 + BOXWIDTH*2 + 15 + 15 + 80, COLORPOS[1] + height - BOTTOMBARHEIGHT + 5), 6, 1)
    draw_slider(15 + BOXWIDTH*2 + 15 + 15 + 80 + PICKER.get_width() + 50, height - BOTTOMBARHEIGHT + 5, 20, PICKER.get_height())
    win.blit(SLIDER, (0, 0))
    pygame.draw.circle(win, WHITE, (555, VALUEPOS[1]), 5)
    pygame.draw.circle(win, BLACK, (555, VALUEPOS[1]), 6, 1)


def close_to_white():
    if sum(WHITE) > 240*3:
        return True
    return False


def draw_slider(x, y, width, height):
    SLIDER.fill(TRANSPARENT)
    for i in range(x, x + width + 1):
        for j in range(y, y + height + 1):
            SLIDER.set_at((i, j), ((j - (HEIGHT - BOTTOMBARHEIGHT + 5)) * (-255/170) + 255, (j - (HEIGHT - BOTTOMBARHEIGHT + 5)) * (-255/170) + 255, (j - (HEIGHT - BOTTOMBARHEIGHT + 5)) * (-255/170) + 255))


def get_value(color):
    return rgb_to_hsv(color)[2]


def update_picker():
    global PICKER, SLIDER
    w, h = PICKER.get_size()
    for x in range(w):
        for y in range(h):
            if math.sqrt((y - 85)**2 + (x - 85)**2) < 85:
                color = PICKER.get_at((x, y))
                PICKER.set_at((x, y), change_value(color, get_value(get_color(COLORPOS, VALUEPOS))))


def change_value(color, value):
    new_color = list(rgb_to_hsv(color))
    new_color[2] = value
    return hsv_to_rgb(new_color)


def main(win, width, height):
    win.fill(WHITE)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, width, height)
        update_picker()
        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
