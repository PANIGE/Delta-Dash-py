import os 
from framework.data.data import *
from framework.graphics.spriteManager import SpriteManager

Debug = False

Running = False

currentSkin = "user"
currentDirectory = os.getcwd()
surface = None
windowManager = WindowManager()
clock = None
cursorPos = vector2(0,0)
cursor = None
MenuManager = None
AudioManager = None
UserEvents = {}
PixelWhite = "pixel.png"
Name = "Delta Dash"
Scheduler = None
Background = None
Starting = True
LastActive = None
Afk = False
AudioMeter = None
Version = "20210318alpha"
Logger = None
Config = None
db = None
playing = None
Framerate = 30

volume = 1


#Cache to transit data between menus
cache = None

#SpriteManagers
backgroundSprites = SpriteManager()
foregroundSprites = SpriteManager()
overlaySprites = SpriteManager()


#Windows
WindowLeft = None
WindowCenter = None
WindowRight = None