from framework.graphics.pSprite import pSprite
from menus.overlays.pNotification import Notification
from framework.graphics.pText import pText
from framework.gameplayElements.pButton import pButton
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
import pygame
from os import path
import  time

class rankingPanel:
    def __init__(self):
        self.Transition = False
        self.disposeTime = 400
        self.data = None
        self.panel = None
        self.rank = None
        self.SoundHover = glob.AudioManager.loadSound("button-hover.wav", SkinSource.local)
        self.SoundClick = glob.AudioManager.loadSound("button-select.wav", SkinSource.local)
        self.SoundBack = glob.AudioManager.loadSound("button-back.wav", SkinSource.local)

    def init(self):
        glob.Framerate = 30
        #Get data from cache and empty it to get it ready to free some space
        self.data = glob.cache #To avoiding python to act as reference and not copy when emptying cache
        glob.cache = None
        self.panel = pSprite("ranking-panel.png", vector2(0,0), SkinSource.user, Positions.topLeft, Positions.topLeft)
        glob.foregroundSprites.add(self.panel)
        self.panel.Scale(glob.windowManager.height/self.panel.image.get_height())
        self.rank = pSprite(f"ranks/{(self.data['rank'])}.png", vector2(-50,100), SkinSource.local, Positions.topRight, Positions.topRight)

        glob.foregroundSprites.add(self.rank)


        bottomBar = pSprite(glob.PixelWhite, vector2(0, 0), SkinSource.local, Positions.bottomCentre,
                            Positions.bottomCentre, Color(50, 50, 50))
        bottomBar.VectorScale(vector2(1920, 100))
        glob.foregroundSprites.add(bottomBar)

        button = pButton("Back", vector2(200, 100), FontStyle.regular,
                         vector2(100, glob.windowManager.heightScaled - 50),
                         Color(255, 120, 174))
        button.text.position = vector2(0, 20)
        button.onClick(glob.AudioManager.play, sound=self.SoundBack)
        button.onClick(glob.MenuManager.ChangeMenu, type=Menus.SongSelection)
        glob.foregroundSprites.add(button)

        play_button = pButton("Retry", vector2(200, 100), FontStyle.regular,
                              vector2(glob.windowManager.widthScaled - 100, glob.windowManager.heightScaled - 50),
                              Color(52, 237, 132))
        play_button.text.position = vector2(-10, 20)
        play_button.onClick(glob.AudioManager.play, sound=self.SoundClick)
        play_button.onClick(glob.MenuManager.ChangeMenu, type=Menus.Playing)
        glob.foregroundSprites.add(play_button)

        stat = pText(glob.AudioManager.currentSong["name"] + " [" + ["normal", "hard", "insane"][glob.Difficulty] + "]", 60, FontStyle.thin, vector2(0,0), Positions.topRight, Positions.topRight)
        glob.foregroundSprites.add(stat)

        #Since those are not changing and will never change, just reassign variable to take less ram, even if talking about ram with python is kinda ironic
        stat = pText(str(self.data["score"]), 80, FontStyle.regular, vector2(350,17), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["xmgpRatio"][3]), 60, FontStyle.regular, vector2(200,130), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["xmgpRatio"][2]), 60, FontStyle.regular, vector2(200,220), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["xmgpRatio"][1]), 60, FontStyle.regular, vector2(200,310), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["xmgpRatio"][0]), 60, FontStyle.regular, vector2(500,310), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["combo"])+"x", 60, FontStyle.regular, vector2(100,405), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(str(self.data["accuracy"])+"%", 60, FontStyle.regular, vector2(380,405), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        stat = pText(f"UR : {(self.data['unstableRate'][0][0])}ms /{(self.data['unstableRate'][0][1])}ms /{(self.data['unstableRate'][0][2])}ms", 40, FontStyle.regular, vector2(500,135), Positions.topLeft, Positions.topCentre)
        glob.foregroundSprites.add(stat)

        bg = pSprite(glob.PixelWhite, vector2(-100, 395), SkinSource.local, Positions.topCentre,
                              Positions.topCentre, Color(0,0,0))
        bg.VectorScale(vector2(300, 55))
        bg.Fade(0.7)
        glob.foregroundSprites.add(bg)

        perfectLine = pSprite(glob.PixelWhite, vector2(-100, 420), SkinSource.local, Positions.topCentre,
                            Positions.topCentre, Color(56, 185, 255))
        perfectLine.VectorScale(vector2(100,5))
        glob.foregroundSprites.add(perfectLine)

        goodLine = pSprite(glob.PixelWhite, vector2(-150, 420), SkinSource.local, Positions.topCentre,
                            Positions.topRight, Color(56, 255, 86))
        goodLine.VectorScale(vector2(50, 5))
        glob.foregroundSprites.add(goodLine)

        goodLine = pSprite(glob.PixelWhite, vector2(-50, 420), SkinSource.local, Positions.topCentre,
                            Positions.topLeft, Color(56, 255, 86))
        goodLine.VectorScale(vector2(50, 5))
        glob.foregroundSprites.add(goodLine)

        MehLine = pSprite(glob.PixelWhite, vector2(-199, 420), SkinSource.local, Positions.topCentre,
                            Positions.topRight, Color(255, 142, 77))
        MehLine.VectorScale(vector2(50, 5))
        glob.foregroundSprites.add(MehLine)

        MehLine = pSprite(glob.PixelWhite, vector2(-1, 420), SkinSource.local, Positions.topCentre,
                            Positions.topLeft, Color(255, 142, 77))
        MehLine.VectorScale(vector2(50, 5))
        glob.foregroundSprites.add(MehLine)

        lines = self.data["unstableRate"][1]
        glob.Logger.debug(lines)


        offset = (self.data["mapOD"])/290

        for line in lines:
            positionX = -100 + (line*offset)
            lSprite = pSprite(glob.PixelWhite, vector2(positionX, 422.5), SkinSource.local, Positions.topCentre,
                            Positions.centre)
            lSprite.VectorScale(vector2(2,55))
            lSprite.Fade(0.7)
            glob.foregroundSprites.add(lSprite)




    def update(self):
        pass

    def dispose(self):
        pass

    def HandleEvents(self, events):
        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]:
            glob.MenuManager.ChangeMenu(Menus.SongSelection)

        for event in events:

            if event.type == glob.UserEvents["MUSIC_END"]:
                glob.AudioManager.SeekPreview()
                glob.AudioManager.Pause()

            if event.type == pygame.QUIT:
                glob.MenuManager.ChangeMenu(Menus.SongSelection)