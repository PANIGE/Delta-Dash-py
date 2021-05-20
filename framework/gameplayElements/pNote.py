from framework import glob
from framework.data import helper
from framework.data.data import *
from framework.graphics.pText import pText
from framework.graphics.pSprite import pSprite
from framework.data.data import *


class pNote:
    """Important gameplay element"""
    def __init__(self, time, position, Approach, refObject):

        self.time = time
        if position == NotePos.Upper:
            color = Color(102, 66, 245)
            Field = Positions.topCentre
            mult = 1
        else:
            mult = -1
            color = Color(245, 64, 64)
            Field = Positions.bottomCentre

        self.Sprite = pSprite("objects/hitObjectBegin.png", vector2(0,200*mult), SkinSource.user, Field, Positions.centre, color, Clocks.audio, False)
        self.Sprite.scale = 0.2
        self.Sprite.loadFrom(refObject)
        self.Sprite.position = vector2(5550,5550)
        self.Sprite.tag = "LowerElement" if position == NotePos.Lower else "UpperElement"


        glob.foregroundSprites.add(self.Sprite)
        #since transformation are for later, like... really later, lets just input it into the transformation manager
        self.Sprite.transformations["position"]["beginTime"] = time-Approach
        self.Sprite.transformations["position"]["endTime"] = time+Approach
        self.Sprite.transformations["position"]["beginValue"] = vector2(1000,0)
        self.Sprite.transformations["position"]["endValue"] = vector2(-1000,0)
        self.Sprite.transformations["position"]["easing"] = EaseTypes.linear
        self.Sprite.transformations["position"]["loop"] = False





    def Miss(self):
        """Handle sprite miss, and already remove it after animation has been called, since it will take space on ram at the moment transformations has been applied, and can be painful on map ending"""
        self.Sprite.Color(Color(255, 0, 0))
        self.Sprite.FadeTo(0, 200)
        glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=self.Sprite)

    def Hit(self):
        """Handle sprite hit, and already remove it after animation has been called, since it will take space on ram at the moment transformations has been applied, and can be painful on map ending"""
        self.Sprite.ClearTransformations()
        self.Sprite.ScaleTo(0.3, 300, EaseTypes.easeOut)
        self.Sprite.FadeTo(0, 300, EaseTypes.easeOut)
        glob.Scheduler.AddDelayed(300, glob.foregroundSprites.remove, sprite=self.Sprite)
