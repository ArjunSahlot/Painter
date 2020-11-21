import math

import pygame
import os
from colorsys import *
import numpy as np


pygame.init()

WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Painter")
pygame.display.set_icon(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "icon.png")))

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


class ColorPicker:
    def __init__(self, wheelPos, wheelRad, sliderPos, sliderSize, sliderHoriz, sliderInvert, cursorRad, displayRectLoc, displayRectSize=(150, 150)):
        self.wheelPos, self.wheelRad = wheelPos, wheelRad
        self.sliderPos, self.sliderSize, self.sliderHoriz, self.sliderInvert = sliderPos, sliderSize, sliderHoriz, sliderInvert
        self.cursorRad = cursorRad
        self.displayRectLoc, self.displayRectSize = displayRectLoc, displayRectSize
        self.wheelCursor, self.sliderCursor = list((wheelPos[0] - cursorRad, wheelPos[1] - cursorRad)), list(
            (sliderPos[0] + sliderSize[0]//2 - cursorRad, sliderPos[1] + sliderSize[1]//2 - cursorRad))
        self.sliderSurf = pygame.Surface(sliderSize)
        self.wheelSurf = pygame.transform.scale(
            pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "color_picker.png")), (wheelRad*2,)*2)
        self.cursorSurf = pygame.Surface(
            (self.cursorRad*2,)*2, pygame.SRCALPHA)
        self.wheelDarken = pygame.Surface((wheelRad*2,)*2, pygame.SRCALPHA)
        self._CreateWheel()
        self._CreateSlider()
        self._CreateCursor()
        self._UpdateWheel()

    def Draw(self, window):
        pygame.draw.rect(window, self.GetRGB(),
                         (*self.displayRectLoc, *self.displayRectSize))
        window.blit(self.sliderSurf, self.sliderPos)
        window.blit(self.cursorSurf, self.sliderCursor)
        window.blit(
            self.wheelSurf, (self.wheelPos[0] - self.wheelRad, self.wheelPos[1] - self.wheelRad))
        window.blit(
            self.wheelDarken, (self.wheelPos[0] - self.wheelRad, self.wheelPos[1] - self.wheelRad))
        window.blit(self.cursorSurf, self.wheelCursor)

    def Update(self, window):
        self.Draw(window)
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if ((self.wheelPos[0] - x)**2 + (self.wheelPos[1] - y)**2)**0.5 < self.wheelRad - 2:
                self.wheelCursor = (x - self.cursorRad, y - self.cursorRad)
            elif self.sliderPos[0] < x < self.sliderPos[0] + self.sliderSize[0] and self.sliderPos[1] < y < self.sliderPos[1] + self.sliderSize[1]:
                self.sliderCursor[1] = y - self.cursorRad
                self._UpdateWheel()

    def GetRGB(self):
        wrgb = self.wheelSurf.get_at((self.wheelCursor[0] - self.wheelPos[0] + self.cursorRad +
                                      self.wheelRad, self.wheelCursor[1] - self.wheelPos[1] + self.cursorRad + self.wheelRad))
        srgb = self.sliderSurf.get_at(
            (self.sliderCursor[0] - self.sliderPos[0] + self.cursorRad, self.sliderCursor[1] - self.sliderPos[1] + self.cursorRad))
        whsv = rgb_to_hsv(*(np.array(wrgb)/255)[:3])
        shsv = rgb_to_hsv(*(np.array(srgb)/255)[:3])
        hsv = (whsv[0], whsv[1], shsv[2])
        rgb = np.array(hsv_to_rgb(*hsv))*255
        return rgb

    def GetHSV(self):
        rgb = (np.array(self.GetRGB())/255)[:3]
        return np.array(rgb_to_hsv(*rgb))*255

    def _UpdateWheel(self):
        pygame.draw.circle(self.wheelDarken, (0, 0, 0, np.interp(
            self.GetHSV()[2], (0, 255), (255, 0))), (self.wheelRad,)*2, self.wheelRad)

    def _CreateWheel(self):
        pygame.draw.circle(self.wheelSurf, (0, 0, 0),
                           (self.wheelRad,)*2, self.wheelRad, 2)

    def _CreateSlider(self):
        w, h = self.sliderSize
        if self.sliderHoriz:
            for x in range(w):
                if self.sliderInvert:
                    value = np.interp(x, (0, w), (0, 255))
                else:
                    value = np.interp(x, (0, w), (255, 0))
                pygame.draw.rect(self.sliderSurf, (value,)*3, (x, 0, 1, h))

        else:
            for y in range(h):
                if self.sliderInvert:
                    value = np.interp(y, (0, h), (0, 255))
                else:
                    value = np.interp(y, (0, h), (255, 0))
                pygame.draw.rect(self.sliderSurf, (value,)*3, (0, y, w, 1))
        pygame.draw.rect(self.sliderSurf, (0, 0, 0), (0, 0, w, h), 1)

    def _CreateCursor(self):
        self.cursorSurf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.cursorSurf, (255, 255, 255),
                           (self.cursorRad,)*2, self.cursorRad)
        pygame.draw.circle(self.cursorSurf, (0, 0, 0),
                           (self.cursorRad,)*2, self.cursorRad, 2)


# Images
ERASER = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "eraser_icon.png")), (SMALLERBOXWIDTH, SMALLERBOXWIDTH))
CLEAR = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "clear_screen.png")), (SMALLERBOXWIDTH - 14, SMALLERBOXWIDTH - 14))
picker = ColorPicker(
    (15 + BOXWIDTH * 2 + 100 + 50, HEIGHT - BOTTOMBARHEIGHT + 90),
    85,
    (BOXWIDTH*2 + 270, HEIGHT - BOTTOMBARHEIGHT + 5),
    (20, 170),
    False,
    False,
    5,
    (BOXWIDTH*2 + 330, HEIGHT - BOTTOMBARHEIGHT + 15),
    (BOXWIDTH + 50, BOXWIDTH + 50))
CURRENTCOLOR = picker.GetRGB()


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHTGREY = (200, 200, 200)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)


def draw_window(win, width, height, erasing, square_cursor):
    win.fill(LIGHTGREY, (0, height - BOTTOMBARHEIGHT, width, BOTTOMBARHEIGHT))

    square_box = pygame.draw.rect(win, BLACK if not square_cursor else GREEN, (15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    pygame.draw.rect(win, CURRENTCOLOR, (40, height - BOTTOMBARHEIGHT + 40, BOXWIDTH - 50, BOXWIDTH - 50))
    square_text = FONT_D.render("Square Pen", 1, BLACK)
    win.blit(square_text, (15 + BOXWIDTH - square_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))

    circle_box = pygame.draw.rect(win, BLACK if square_cursor else GREEN, (15 + BOXWIDTH + 15 + 15, height - BOTTOMBARHEIGHT + 15, BOXWIDTH, BOXWIDTH), 5)
    circle_text = FONT_D.render("Circle Pen", 1, BLACK)
    win.blit(circle_text, (15 + BOXWIDTH + BOXWIDTH + 15 + 4 - circle_text.get_width(), height - BOTTOMBARHEIGHT + 15 + BOXWIDTH + 5))
    pygame.draw.circle(win, CURRENTCOLOR, (15 + BOXWIDTH + 15 + 15 + BOXWIDTH//2, height - BOTTOMBARHEIGHT + 15 + BOXWIDTH//2), 25)

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

    info_text1 = FONT_D.render("Left Mouse Button: Normal Drawing", 1, BLACK)
    info_text2 = FONT_D.render("Middle Mouse Button: Draw Line", 1, BLACK)
    info_text3 = FONT_D.render("Right Mouse Button: Draw Dotted Line", 1, BLACK)

    text_x, text_y = (15, 740)
    win.blit(info_text1, (text_x, text_y))
    win.blit(info_text2, (text_x, text_y + info_text1.get_height() + 5))
    win.blit(info_text3, (text_x, text_y + info_text1.get_height() + 5 + info_text2.get_height() + 5))

    return square_box, circle_box, slider_box, eraser_box, clear_box


def main(win, width, height):
    global BRUSHSIZE, CURRENTCOLOR
    win.fill(WHITE)
    prevX, prevY = pygame.mouse.get_pos()
    erasing = False
    square_cursor = True
    run = True
    while run:
        if not erasing:
            CURRENTCOLOR = picker.GetRGB()
        square_box, circle_box, slider_box, eraser_box, clear_box = draw_window(win, width, height, erasing, square_cursor)
        picker.Update(win)
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
                    square_cursor = True if not square_cursor else False

            if circle_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    square_cursor = False if square_cursor else True

            if slider_box.collidepoint(mouseX, mouseY):
                if pygame.mouse.get_pressed()[0]:
                    BRUSHSIZE = (mouseX - 735)//(240//MAXBRUSHSIZE)

            if eraser_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    erasing = True if not erasing else False
                    CURRENTCOLOR = WHITE if erasing else picker.GetRGB()

            if clear_box.collidepoint(mouseX, mouseY):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    win.fill(WHITE)

            if pygame.mouse.get_pressed()[0]:
                if mouseY < HEIGHT - BOTTOMBARHEIGHT:
                    if square_cursor:
                        pygame.draw.rect(win, CURRENTCOLOR, (mouseX - BRUSHSIZE//2, mouseY - BRUSHSIZE//2, BRUSHSIZE, BRUSHSIZE))
                    else:
                        pygame.draw.circle(win, CURRENTCOLOR, (mouseX, mouseY), BRUSHSIZE*11//20)

            if pygame.mouse.get_pressed()[2]:
                if mouseY < HEIGHT - BOTTOMBARHEIGHT and math.sqrt((mouseY - prevY)**2 + (mouseX - prevX)**2) > BRUSHSIZE + 10:
                    if square_cursor:
                        pygame.draw.rect(win, CURRENTCOLOR, (mouseX - BRUSHSIZE//2, mouseY - BRUSHSIZE//2, BRUSHSIZE, BRUSHSIZE))
                    else:
                        pygame.draw.circle(win, CURRENTCOLOR, (mouseX, mouseY), BRUSHSIZE*11//20)
                    prevX, prevY = mouseX, mouseY

        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
