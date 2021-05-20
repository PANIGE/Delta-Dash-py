########################################################
# Main game script, used to be ran within nothing else #
########################################################
import sys
import time
import ctypes
import pygame

from pygame.locals import *

from framework import glob

from framework.data import helper, ErrorHandler
from framework.data.Scheduler import Scheduler
from framework.data.data import *
from framework.data.database import Db
from framework.data.log import log
from framework.graphics.cursor import cursor
from framework.graphics.pSprite import pSprite
from framework.graphics.pText import pText
from framework.serializers.config import Config
from framework.audio.audioManager import AudioManager
from menus.menuManager import MenuManager
from menus.overlays.volumeMeter import AudioMeter
import traceback

if __name__ == "__main__": #avoid script to be runned in another script

    #Initialize all global variables
    glob.Config = Config()
    glob.db = Db()

    glob.volume = glob.Config["volume"]
    pygame.init()
    pygame.font.init()

    wd, ht = pygame.display.Info().current_w , pygame.display.Info().current_h

    glob.windowManager.width = wd
    glob.windowManager.height = ht
    glob.windowManager.heightScaled = ht / glob.windowManager.getPixelSize()
    glob.windowManager.widthScaled = wd / glob.windowManager.getPixelSize()
    glob.Scheduler = Scheduler()

    #Initialize pygame

    flags = HWSURFACE |  DOUBLEBUF | HWACCEL | NOFRAME
    glob.surface = pygame.display.set_mode((glob.windowManager.width, glob.windowManager.height), display=0, flags=flags)
    pygame.display.set_caption(glob.Name)
    icon = pygame.image.load(glob.currentDirectory+"/data/sprites/icon.png")
    pygame.display.set_icon(icon)


    glob.Logger = log()

    glob.AudioManager = AudioManager()
    glob.MenuManager = MenuManager()

    #Get the background up

    Background = pSprite("background.png", vector2(0, 0), SkinSource.local, Positions.centre, Positions.centre)
    backgroundScale = glob.windowManager.width / Background.image.get_width()
    Background.Scale(backgroundScale*1.3) #for the parralax to work
    cursor = cursor()
    glob.cursor = cursor

    glob.backgroundSprites.add(Background)

    glob.clock = pygame.time.Clock()
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #Transparent cursor to let in game cursor do his work
    Background.posMult = -1
    Background.posMultY = -1
    glob.Background = Background

    #Get the main menu and playing the main audio
    glob.MenuManager.ChangeMenu(Menus.MainMenu)
    glob.AudioManager.PlayMusic("/data/files/intro")

    #setting afk time to now
    glob.LastActive = time.time()*1000

    #get volume meter
    glob.AudioMeter = AudioMeter()

    #fps stuff to keep track of game perfs
    fpsCounterBg = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.bottomRight, Positions.bottomRight, Color(0,0,0))
    fpsCounterBg.VectorScale(vector2(200,30))
    fpsCounterBg.borderBounds(10)
    fpsCounterBg.Fade(0)
    fpsCounter = pText("", 25, FontStyle.thin, vector2(30,10), Positions.bottomRight, Positions.bottomRight)
    lastFpsSpike = time.time()*1000
    timeSpike = False
    glob.overlaySprites.add(fpsCounterBg)
    glob.overlaySprites.add(fpsCounter)

    glob.Running = True
    glob.Logger.write("Initialised")
    try:
        while glob.Running: #Main Loop

            #fps tracking
            glob.clock.tick(glob.Framerate)
            if timeSpike:

                if glob.clock.get_fps() >glob.Framerate-5:
                    fpsCounter.Color(Color(255,255,255))
                elif glob.clock.get_fps() > glob.Framerate/2:
                    fpsCounter.Color(Color(255, 123, 0))
                else:
                    fpsCounter.Color(Color(255, 0, 0))
                fpsCounter.Text("Framerate : {}/{}".format(int(glob.clock.get_fps()), glob.Framerate))
            if glob.clock.get_fps() < glob.Framerate-5:
                lastFpsSpike = time.time() * 1000
                if not timeSpike:
                    timeSpike = True
                    fpsCounterBg.FadeTo(0.7,500)
                    fpsCounter.FadeTo(1, 500)
            if timeSpike and time.time()*1000 - lastFpsSpike > 5000:
                fpsCounter.FadeTo(0, 500)
                fpsCounterBg.FadeTo(0, 500)
                timeSpike = False

            #Update frame behind background
            glob.surface.fill((0, 0, 0))

            glob.AudioMeter.Update()

            cursor.updateCursorPos()

            glob.backgroundSprites.Position(helper.SetParalax(50).x, helper.SetParalax(50).y)

            events =pygame.event.get()
            glob.MenuManager.HandleEvents(events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1,2,3):
                        cursor.onClick()
                    if event.button == 4: glob.AudioMeter.ChangeVolume(True)
                    if event.button == 5: glob.AudioMeter.ChangeVolume(False)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in (1, 2,3):
                        cursor.onRelease()
                if event.type == pygame.MOUSEMOTION:
                    glob.LastActive = time.time()*1000


            glob.MenuManager.activeMenu.update()


            glob.backgroundSprites.draw()
            glob.foregroundSprites.draw()
            glob.overlaySprites.draw()
            cursor.draw()


            pygame.display.flip()
    except Exception as e:
        ErrorHandler.raiseError(e)
        pygame.quit()
        if not glob.Debug:
            ctypes.windll.user32.MessageBoxW(0, "Delta Dash encountered an Error and couldn't continue Working\n\n"+traceback.format_exc()+"\n\nSee logs for further informations", "Delta Dash - Crash", 0)
        



    pygame.quit()
    sys.exit(0)
