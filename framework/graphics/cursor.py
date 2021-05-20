from framework.data.data import *
from framework import  glob
from framework.graphics.pSprite import pSprite
import time
from framework.data.data import *
from framework.data import helper
import pygame


class cursor:
    def __init__(self):
        self.sprite = pSprite("cursor.png", vector2(0, 0), SkinSource.user, Positions.topLeft, Positions.topLeft)
        self.additive = pSprite("cursor-additive.png", vector2(0, 0), SkinSource.user, Positions.topLeft, Positions.topLeft, Color(79, 126, 255))
        self.sprite.VectorScale(vector2(0.1,0.1))
        self.additive.VectorScale(vector2(0.1,0.1))



    def draw(self):
        self.additive.draw()
        self.sprite.draw()
        if not glob.Afk:
            self.additive.Fade(helper.getSyncValue(1, 0.5))


    def onClick(self):
        self.sprite.ScaleTo(1.2, 100)
        self.additive.ScaleTo(1.2, 100)
        glob.LastActive = time.time()*1000
        isClicked = False
        for sprite in glob.overlaySprites.sprites:
            if sprite.isonHover:
                isClicked = True
                sprite.__onClick__()

        if not isClicked:
            for sprite in glob.foregroundSprites.sprites:
                if sprite.isonHover:
                    sprite.__onClick__()

    def onRelease(self):
        self.sprite.ScaleTo(1, 100)
        self.additive.ScaleTo(1, 100)

    def updateCursorPos(self):
        x, y = pygame.mouse.get_pos()
        self.sprite.position = vector2(x / glob.windowManager.getPixelSize(), y / glob.windowManager.getPixelSize())
        self.additive.position = vector2(x / glob.windowManager.getPixelSize(), y / glob.windowManager.getPixelSize())
        glob.cursorPos = vector2(x, y)
        if (time.time()*1000)-glob.LastActive > 6000 and not glob.Afk:
            glob.Afk = True
            self.sprite.FadeTo(0, 300)
            self.additive.FadeTo(0, 300)
        elif glob.Afk and (time.time()*1000)-glob.LastActive < 6000:
            glob.Afk = False
            self.sprite.FadeTo(1, 100)