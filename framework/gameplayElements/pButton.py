from framework import glob
from framework.data.data import *
from framework.graphics.pText import pText
from framework.graphics.pSprite import pSprite
from framework.data.data import *


class pButton:
    def __init__(self, text, size, style=FontStyle.regular, position=vector2(0,0), color=Color(255,255,255,255)):
        self.originPosition = position
        self.position = vector2(0,0)
        self.color = color
        self.size = size

        self.centreButton = pSprite(glob.PixelWhite, position=position, skinSource=SkinSource.local, field=Positions.topLeft, origin=Positions.centre, color=color)
        self.centreButton.VectorScale(size)
        
        
        offset = 0.57
        
        self.text = pText(text, (0.8*size.y), style, position=vector2(position.x*offset,position.y*offset-15), field=Positions.topLeft, origin=Positions.centre) #575
        self.rightButton = pSprite("button-right.png", vector2( position.x + (size.x/2)-1, position.y), SkinSource.local, Positions.topLeft, Positions.centreLeft, color)
        self.rightButton.Scale((1/500)*size.y)

        self.leftButton = pSprite("button-left.png", vector2( position.x - (size.x/2)+1, position.y), SkinSource.local, Positions.topLeft, Positions.centreRight, color)
        self.leftButton.Scale((1/500)*size.y)
        self.tag = ""
        self.onhover = []
        self.onhoverlost = []
        self.onclick = []
        self.isonHover = False
        self.enabled = True

    
    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onclick.append([function, kwargs])

    def enable(self):
        self.enabled = True
        self.centreButton.enable()
        self.rightButton.enable()
        self.leftButton.enable()
        self.text.enable()

    def disable(self):
        self.enabled = False
        self.centreButton.disable()
        self.rightButton.disable()
        self.leftButton.disable()
        self.text.disable()

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](**hoverAction[1])
        self.centreButton.VectorScaleTo(vector2(self.size.x+10, self.size.y), 200)
        self.centreButton.Color(Color(min(self.color.r+30,255),min(self.color.g+30,255),min(self.color.b+30,255)))
        self.rightButton.Color(Color(min(self.color.r+30,255),min(self.color.g+30,255),min(self.color.b+30,255)))
        self.leftButton.Color(Color(min(self.color.r+30,255),min(self.color.g+30,255),min(self.color.b+30,255)))
        
    def ClearTransformations(self):
        pass

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](hoverLostAction[1])
        self.centreButton.VectorScaleTo(vector2(self.size.x+10, self.size.y), 200)
        self.centreButton.Color(self.color)
        self.rightButton.Color(self.color)
        self.leftButton.Color(self.color)

    def __onClick__(self):
        for click in self.onclick:
            if click[1] == {}:
                click[0]()
            else:
                click[0](**click[1])
        self.centreButton.Color(Color(255,255,255))
        self.centreButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)
        self.rightButton.Color(Color(255,255,255))
        self.rightButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)
        self.leftButton.Color(Color(255,255,255))
        self.leftButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)

    def Position(self, position):
        self.position = position
        self.centreButton.position = position
        self.rightButton.position = position
        self.leftButton.position = position
        self.text.position = position

    def Fade(self, x):
        self.centreButton.Fade(x)
        self.text.Fade(x)
        self.leftButton.Fade(x)
        self.rightButton.Fade(x)

    def FadeTo(self, value, duration, easing=EaseTypes.linear):
        self.centreButton.FadeTo(value, duration, easing)
        self.text.FadeTo(value, duration, easing)
        self.leftButton.FadeTo(value, duration, easing)
        self.rightButton.FadeTo(value, duration, easing)

    def draw(self):
        self.centreButton.draw()
        self.rightButton.draw()
        self.leftButton.draw()
        self.text.draw()
        if self.enabled:
            if (self.centreButton.isonHover or self.rightButton.isonHover or self.leftButton.isonHover) and not self.isonHover:
                self.__onHover__()
                self.isonHover = True
            elif not(self.centreButton.isonHover or self.rightButton.isonHover or self.leftButton.isonHover) and self.isonHover:
                self.__onHoverLost__()
                self.isonHover = False