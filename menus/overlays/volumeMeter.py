from framework import glob
import  time
from framework.graphics.pText import pText
from framework.graphics.pSprite import pSprite
from framework.data.data import *
import math



class AudioMeter:
    def __init__(self):
        self.active = False
        self.lastActive = 0
        self.background = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centreRight, Positions.centreRight, Color(0,0,0))
        self.background.VectorScale(vector2(30,600))
        self.foreground = pSprite(glob.PixelWhite, vector2(-13,290), SkinSource.local, Positions.centreRight, Positions.bottomCentre, Color(255, 204, 212))
        self.text = pText("100%", 20, FontStyle.regular, vector2(10,180), Positions.centreRight, Positions.centreRight)
        self.foreground.VectorScale(vector2(10,glob.volume*580))

    def Update(self):
        if (time.time()*1000) - self.lastActive > 3000 and self.active:
            self.hide()
            self.active = None

    def ChangeVolume(self, up):
        if not self.active:
            self.show()
            self.active = True
        self.lastActive = time.time()*1000
        if up:
            if glob.volume <= 1:
                if glob.volume < 0.10:
                    glob.volume += 0.01
                else:
                    glob.volume += 0.05
                if glob.volume > 1:
                    glob.volume = 1
                glob.AudioManager.setVolume(glob.volume)
        else:
            if glob.volume >=0:
                if glob.volume < 0.10:
                    glob.volume -= 0.01
                else:
                    glob.volume -= 0.05
                if glob.volume < 0:
                    glob.volume = 0
                glob.AudioManager.setVolume(glob.volume)
        self.foreground.VectorScaleTo(vector2(10,glob.volume*580), 100, EaseTypes.easeOut)
        self.text.Text(str(math.floor(glob.volume*100))+"%")

    def show(self):
        self.background.Fade(0)
        self.foreground.Fade(0)
        self.text.Fade(0)
        self.background.FadeTo(0.7,200, EaseTypes.easeInOut)
        self.foreground.FadeTo(1,200,EaseTypes.easeInOut)
        self.text.FadeTo(1,200,EaseTypes.easeInOut)
        glob.overlaySprites.add(self.background)
        glob.overlaySprites.add(self.text)
        glob.overlaySprites.add(self.foreground)


    def hide(self):
        self.background.FadeTo(0, 200, EaseTypes.easeInOut)
        self.foreground.FadeTo(0, 200, EaseTypes.easeInOut)
        self.text.FadeTo(0, 200, EaseTypes.easeInOut)
        glob.Scheduler.AddDelayed(200,glob.overlaySprites.remove, sprite=self.background)
        glob.Scheduler.AddDelayed(200,glob.overlaySprites.remove, sprite=self.text)
        glob.Scheduler.AddDelayed(200,glob.overlaySprites.remove, sprite=self.foreground)