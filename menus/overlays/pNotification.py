from framework import glob
from framework.graphics.pText import pText
from framework.graphics.pSprite import pSprite
from framework.data.data import *



class Notification:
    def __init__(self,text, duration, color=Color(255,0,0)):

        self.length = duration

        text = pText(text, 15, FontStyle.regular, vector2(0, 0), Positions.bottomRight, Positions.bottomRight)
        textHeight, textWidth = max(text.text.get_height(), 10), max(text.text.get_width(),100)

        background = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.bottomRight, Positions.bottomRight,Color(0,0,0))
        background.Fade(0.8)
        background.VectorScale(vector2(textWidth*1.5+20,textHeight+10))

        text.position = vector2(0, 2)
        foreGround = pSprite(glob.PixelWhite, vector2(0,0),SkinSource.local, Positions.bottomRight, Positions.bottomCentre, color)
        foreGround.VectorScale(vector2( background.image.get_width(), 5))



        foreGround.tag = "SNotification"
        background.tag = "SNotification"
        text.tag = "SNotification"
        self.text = text
        self.bg = background
        self.fg = foreGround


    def show(self):
        for sprite in glob.overlaySprites.sprites:
            if sprite.tag == "SNotification":
                sprite.posMult = -1
                sprite.posMultY = -1
                sprite.MoveTo(sprite.position.x, sprite.position.y + self.bg.image.get_height()+2, 200, EaseTypes.easeInOut)
        glob.overlaySprites.add(self.bg)
        glob.overlaySprites.add(self.fg)
        glob.overlaySprites.add(self.text)
        self.fg.FadeTo(1,400,EaseTypes.easeInOut)
        self.fg.VectorScaleTo(vector2(0,5), self.length)
        self.bg.FadeTo(0.7,400,EaseTypes.easeInOut)
        self.text.FadeTo(1,400,EaseTypes.easeInOut)
        self.bg.posMult = -1
        self.bg.posMultY = -1
        self.fg.posMult = -1
        self.fg.posMultY = -1
        glob.Scheduler.AddDelayed(self.length, self.dispose)

    def dispose(self):

        self.text.FadeTo(0,400,EaseTypes.easeOut)
        self.fg.FadeTo(0,400,EaseTypes.easeOut)
        self.bg.FadeTo(0,400,EaseTypes.easeOut)

        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.bg)
        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.fg)
        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.text)


class NotificationMassive:
    def __init__(self,text, duration, type=NotificationType.Info):

        self.length = duration


        background = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.topLeft, Positions.topLeft,Color(0,0,0))
        background.Fade(0.8)
        background.VectorScale(vector2(1920,100))
        if type == NotificationType.Info:
            Fgcolor = Color(0, 142, 250)
            textcolor = Color(255,255,255)
        elif type == NotificationType.Warning:
            Fgcolor = Color(255, 136, 0)
            textcolor = Color(255, 136, 0)
        else:
            Fgcolor = Color(255, 0, 0)
            textcolor = Color(255, 0, 0)
        foreGround = pSprite(glob.PixelWhite, vector2(0,100),SkinSource.local, Positions.topCentre, Positions.bottomCentre, Fgcolor)
        foreGround.VectorScale(vector2( 1900, 10))
        text = pText(text, 30, FontStyle.regular,vector2(0, 25), Positions.topCentre, Positions.centre, textcolor)
        foreGround.tag = "Notification"
        background.tag = "Notification"
        text.tag = "Notification"
        self.text = text
        self.bg = background
        self.fg = foreGround


    def show(self):
        for sprite in glob.overlaySprites.sprites:
            if sprite.tag == "Notification":
                sprite.MoveTo(0,50, 400, EaseTypes.easeOut)
                sprite.FadeTo(0,400,EaseTypes.easeOut)
                glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=sprite)
        glob.overlaySprites.add(self.bg)
        glob.overlaySprites.add(self.fg)
        glob.overlaySprites.add(self.text)
        self.fg.FadeTo(1,400,EaseTypes.easeInOut)
        self.fg.VectorScaleTo(vector2(0,10), self.length)
        self.bg.FadeTo(0.7,400,EaseTypes.easeInOut)
        self.text.FadeTo(1,400,EaseTypes.easeInOut)

        glob.Scheduler.AddDelayed(self.length, self.dispose)

    def dispose(self):

        self.text.FadeTo(0,400,EaseTypes.easeOut)
        self.fg.FadeTo(0,400,EaseTypes.easeOut)
        self.bg.FadeTo(0,400,EaseTypes.easeOut)

        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.bg)
        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.fg)
        glob.Scheduler.AddDelayed(400, glob.overlaySprites.remove, sprite=self.text)