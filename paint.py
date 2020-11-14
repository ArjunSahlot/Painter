import math

import pygame
import os
import colorsys

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Painter")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))

# Fonts
FONT_ES = pygame.font.SysFont("comicsans", 15)
FONT_D = pygame.font.SysFont("comicsans", 25)
FONT_S = pygame.font.SysFont("comicsans", 23)

# Constants
BOTTOMBARHEIGHT = 180
BOXWIDTH = 100
SMALLERBOXWIDTH = 70
BRUSHSIZE = 9
MAXBRUSHSIZE = 60

# Images
ERASER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "eraser_icon.png")), (SMALLERBOXWIDTH, SMALLERBOXWIDTH))
CLEAR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "clear_screen.png")), (SMALLERBOXWIDTH - 14, SMALLERBOXWIDTH - 14))
PICKER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "color_picker.png")), (170, 170))
SLIDER = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
COLORPOS = (85, 85)
VALUEPOS = (515, 830)


def get_color(colorpos, valuepos):
    hsv_col = rgb_to_hsv(PICKER.get_at(colorpos))
    hue = hsv_col[0]
    sat = hsv_col[1]
    val = rgb_to_hsv(SLIDER.get_at(valuepos))[2]
    return hsv_to_rgb((hue, sat, val))


def hsv_to_rgb(color):
    color = colorsys.hsv_to_rgb(color[0] / 255, color[1] / 255, color[2] / 255)
    return color[0] * 255, color[1] * 255, color[2] * 255


def rgb_to_hsv(color):
    color = colorsys.rgb_to_hsv(color[0] / 255, color[1] / 255, color[2] / 255)
    return color[0] * 255, color[1] * 255, color[2] * 255


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHTGREY = (200, 200, 200)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)


CURRENTCOLOR = get_color(COLORPOS, VALUEPOS)


def draw_window(win, width, height, picker_changed, slider_changed, erasing, square_cursor, mode):
    win.fill(LIGHTGREY, (0, height - BOTTOMBARHEIGHT, width, BOTTOMBARHEIGHT))

    square_box = pygame.draw.rect(win, BLACK if not square_cursor else GREEN, (15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    pygame.draw.rect(win, CURRENTCOLOR if not close_to_white() else BLACK, (40, height - BOTTOMBARHEIGHT + 40, BOXWIDTH - 50, BOXWIDTH - 50)) # 50=(40-15)*2
    square_text = FONT_D.render("Square Pen", 1, BLACK)
    win.blit(square_text, (15 + BOXWIDTH - square_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))

    circle_box = pygame.draw.rect(win, BLACK if square_cursor else GREEN, (15 + BOXWIDTH + 15 + 15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    circle_text = FONT_D.render("Circle Pen", 1, BLACK)
    win.blit(circle_text, (15 + BOXWIDTH + BOXWIDTH + 15 + 4 - circle_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.circle(win, CURRENTCOLOR if not close_to_white() else BLACK, (15 + BOXWIDTH + 15 + 15 + BOXWIDTH//2, height - BOTTOMBARHEIGHT + 15 + BOXWIDTH//2), 25)

    slider_box = pygame.draw.rect(win, GREY, (width - 25 - 240, height - BOTTOMBARHEIGHT + 25, 240, 15))  # (735, 845, 240, 15)
    pygame.draw.circle(win, WHITE, (BRUSHSIZE*(240//MAXBRUSHSIZE)+735, 845 + 15//2), 12)
    size_text = FONT_D.render(f"Brush Size: {BRUSHSIZE+1}", 1, BLACK)
    win.blit(size_text, (855 - size_text.get_width()//2, height - BOTTOMBARHEIGHT + 25 + 15 + 5))

    eraser_box = pygame.draw.rect(win, BLACK if not erasing else GREEN, (735 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height(), SMALLERBOXWIDTH, SMALLERBOXWIDTH), 5)
    win.blit(ERASER, (735 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height()))
    eraser_text = FONT_S.render("Eraser", 1, BLACK)
    win.blit(eraser_text, (735 + SMALLERBOXWIDTH//2 - eraser_text.get_width()//2 + 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + SMALLERBOXWIDTH + 5))

    clear_box = pygame.draw.rect(win, BLACK, (975 - SMALLERBOXWIDTH - 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height(), SMALLERBOXWIDTH, SMALLERBOXWIDTH), 5)
    win.blit(CLEAR, (975 - SMALLERBOXWIDTH - 10 + 7, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + 7))
    clear_text = FONT_S.render("Clear Screen", 1, BLACK)
    win.blit(clear_text, (975 - SMALLERBOXWIDTH//2 - clear_text.get_width()//2 - 10, height - BOTTOMBARHEIGHT + 25 + 15 + 5 + 15 + size_text.get_height() + SMALLERBOXWIDTH + 5))

    win.blit(PICKER, (15 + BOXWIDTH*2 + 15 + 15 + 80, height - BOTTOMBARHEIGHT + 5))
    pygame.draw.circle(win, WHITE, (COLORPOS[0] + 15 + BOXWIDTH*2 + 15 + 15 + 80, COLORPOS[1] + height - BOTTOMBARHEIGHT + 5), 5)
    pygame.draw.circle(win, BLACK, (COLORPOS[0] + 15 + BOXWIDTH*2 + 15 + 15 + 80, COLORPOS[1] + height - BOTTOMBARHEIGHT + 5), 6, 1)

    if picker_changed:
        draw_slider(15 + BOXWIDTH*2 + 15 + 15 + 80 + PICKER.get_width() + 10, height - BOTTOMBARHEIGHT + 5, 20, PICKER.get_height())
        picker_changed = False
    if slider_changed:
        update_picker()
        slider_changed = False

    win.blit(SLIDER, (0, 0))
    pygame.draw.circle(win, WHITE, (VALUEPOS[0], VALUEPOS[1]), 5)
    pygame.draw.circle(win, BLACK, (VALUEPOS[0], VALUEPOS[1]), 6, 1)

    pygame.draw.rect(win, CURRENTCOLOR, (15 + BOXWIDTH*2 + 15 + 15 + 80 + PICKER.get_width() + 10 + 20 + 15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH + 50, BOXWIDTH + 50))

    info_text1 = FONT_D.render("Left Mouse Button: Normal Drawing", 1, BLACK)
    info_text2 = FONT_D.render("Middle Mouse Button: Draw Line", 1, BLACK)
    info_text3 = FONT_D.render("Right Mouse Button: Draw Dotted Line", 1, BLACK)

    text_x, text_y = (15, 740)
    win.blit(info_text1, (text_x, text_y))
    win.blit(info_text2, (text_x, text_y + info_text1.get_height() + 5))
    win.blit(info_text3, (text_x, text_y + info_text1.get_height() + 5 + info_text2.get_height() + 5))

    return square_box, circle_box, slider_box, eraser_box, clear_box, (15 + BOXWIDTH*2 + 15 + 15 + 80 + PICKER.get_width() + 10, height - BOTTOMBARHEIGHT + 5, 20, PICKER.get_height()), picker_changed, slider_changed


def close_to_white():
    if sum(WHITE) > 240*3:
        return True
    return False


def change_hue_sat(color, hue, sat):
    hsv_col = list(rgb_to_hsv(color))
    hsv_col[1] = hue
    hsv_col[2] = sat
    return hsv_to_rgb(hsv_col)


def get_hue(color):
    return rgb_to_hsv(color)[0]


def get_sat(color):
    return rgb_to_hsv(color)[1]


def draw_slider(x, y, width, height):
    global SLIDER
    SLIDER.fill(TRANSPARENT)
    for i in range(x, x + width + 1):
        for j in range(y, y + height + 1):
            b_w_color = [(j - (HEIGHT - BOTTOMBARHEIGHT + 5)) * (-255/170) + 255] * 3
            SLIDER.set_at((i, j), change_hue_sat(b_w_color, get_hue(CURRENTCOLOR), get_sat(CURRENTCOLOR)))


def get_value(color):
    return rgb_to_hsv(color)[2]


def update_picker():
    global PICKER
    w, h = PICKER.get_size()
    for x in range(w):
        for y in range(h):
            if math.sqrt((y - 85)**2 + (x - 85)**2) < 85:
                color = PICKER.get_at((x, y))
                PICKER.set_at((x, y), change_value(color, get_value(CURRENTCOLOR)))


def change_value(color, value):
    new_color = list(rgb_to_hsv(color))
    new_color[2] = value
    return hsv_to_rgb(new_color)


def main(win, width, height):
    global BRUSHSIZE, COLORPOS, VALUEPOS, CURRENTCOLOR
    win.fill(WHITE)
    prevX, prevY = pygame.mouse.get_pos()
    mode = 1
    picker_changed = True
    slider_changed = True
    erasing = False
    square_cursor = True
    run = True
    while run:
        square_box, circle_box, slider_box, eraser_box, clear_box, value_box, picker_changed, slider_changed = draw_window(win, width, height, picker_changed, slider_changed, erasing, square_cursor, mode)
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and mouseY < height - BOTTOMBARHEIGHT and event.button == 2:
                lineX, lineY = mouseX, mouseY

            if event.type == pygame.MOUSEBUTTONUP and mouseY < height - BOTTOMBARHEIGHT and event.button == 2:
                pygame.draw.line(win, CURRENTCOLOR, (lineX, lineY), (mouseX, mouseY), BRUSHSIZE)

            if square_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    square_cursor = True if square_cursor == False else False

            if circle_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    square_cursor = False if square_cursor == True else True

            if slider_box.collidepoint(mouseX, mouseY):
                if pygame.mouse.get_pressed()[0]:
                    BRUSHSIZE = (mouseX - 735)//(240//MAXBRUSHSIZE)

            if eraser_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    erasing = True if erasing == False else False
                    CURRENTCOLOR = WHITE if erasing else get_color(COLORPOS, VALUEPOS)

            if clear_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    win.fill(WHITE)

            if pygame.mouse.get_pressed()[0]:
                if mouseY < HEIGHT - BOTTOMBARHEIGHT:
                    if square_cursor:
                        pygame.draw.rect(win, CURRENTCOLOR, (mouseX - BRUSHSIZE//2, mouseY - BRUSHSIZE//2, BRUSHSIZE, BRUSHSIZE))
                    else:
                        pygame.draw.circle(win, CURRENTCOLOR, (mouseX, mouseY), BRUSHSIZE*11//20)

                if math.sqrt((mouseY - 910)**2 + (mouseX - 410)**2) < 85:
                    COLORPOS = (mouseX - 325, mouseY - 825)
                    CURRENTCOLOR = get_color(COLORPOS, VALUEPOS)
                    picker_changed = True
                    erasing = False
                if value_box[0] < mouseX < value_box[0] + value_box[2] and value_box[1] < mouseY < value_box[1] + value_box[3]:
                    VALUEPOS = (515, mouseY)
                    CURRENTCOLOR = get_color(COLORPOS, VALUEPOS)
                    slider_changed = True
                    erasing = False

            if pygame.mouse.get_pressed()[2]:
                if mouseY < HEIGHT - BOTTOMBARHEIGHT and math.sqrt((mouseY - prevY)**2 + (mouseX - prevX)**2) > BRUSHSIZE + 10:
                    if square_cursor:
                        pygame.draw.rect(win, CURRENTCOLOR, (mouseX - BRUSHSIZE//2, mouseY - BRUSHSIZE//2, BRUSHSIZE, BRUSHSIZE))
                    else:
                        pygame.draw.circle(win, CURRENTCOLOR, (mouseX, mouseY), BRUSHSIZE*11//20)
                    prevX, prevY = mouseX, mouseY

        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
