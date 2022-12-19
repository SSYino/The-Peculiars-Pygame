import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Load:
    def __init__(self):

        self.py = pygame
        self.py.init()
        self.py.display.set_caption('The Peculiars')
        self.programIcon = self.py.image.load('assets/images/Logo.png')
        self.py.display.set_icon(self.programIcon)

        # self.p.event.set_allowed([self.p.KEYDOWN, self.p.KEYUP, self.p.QUIT])

        self.cursor_normal = self.py.cursors.Cursor(self.py.SYSTEM_CURSOR_ARROW)
        self.cursor_text = self.py.cursors.Cursor(self.py.SYSTEM_CURSOR_IBEAM)

        # SCREEN
        # self.W = config.getresolution()[0]
        # self.H = config.getresolution()[1]
        self.W = 1250
        self.H = 1000

        self.SIZE = (self.W, self.H)
        self.FPS = 60
        self.RUN = True

        # CONFIG
        # self.flags = self.p.HWSURFACE | self.p.DOUBLEBUF
        self.flags = self.py.RESIZABLE
        self.win = self.py.display.set_mode(self.SIZE, self.flags)
        self.clock = self.py.time.Clock()

        # FONTS
        self.FONT_SIZE = 15
        self.COMICSAN =     self.py.font.SysFont('Comic Sans MS', self.FONT_SIZE)
        # self.JETMONO =      self.p.font.Font('assets/fonts/jetMono.ttf', self.FONT_SIZE)
        # self.ARCADE =       self.p.font.Font('assets/fonts/arcade.ttf', self.FONT_SIZE)
