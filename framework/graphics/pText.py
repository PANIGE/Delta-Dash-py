from framework import glob
from framework.data import helper
from framework.data.data import *
import pygame
import  time
originMult = 1
posMult = 1



class pText:


    def __init__(self, text, textSize, style=FontStyle.regular, position=vector2(0,0),  field=Positions.topLeft, origin=Positions.topLeft, color=Color(255,255,255,255), clock=Clocks.game):
        global originMult
        originMult = 1/(glob.windowManager.getPixelSize())

        mult = int(textSize *2.66)



        self.font = pygame.font.Font(glob.currentDirectory+"/data/fonts/Torus-"+style, mult )
        self.text = self.font.render(text, True, (color.r, color.g, color.b, color.a))
        self.text = self.text.convert_alpha()
        self.field = field
        self.origin = origin
        self.Clock = clock
        self.originPosition = position
        self.posMult = posMult
        self.posMultY = posMult
        self.position = vector2(0,0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale" : {}, "fade" : {}, "VectorScale": {}, "position": {}, "colorFade":{}, "rotation":{}}
        self.alpha = 1
        self.vectorScale = vector2(1,1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.textSize = textSize*glob.windowManager.getPixelSize()*3*1.3
        self.offset = vector2(0,0)
        self.effectivePosition = vector2(0,0)
        self.onhover = []
        self.onhoverlost = []
        self.onClick = []
        self.isonHover = False
        self.enabled = True


        width = self.text.get_width()
        height = self.text.get_height()
        self.srcText = self.text.convert_alpha()
        self.unBlendedImg = self.text.convert_alpha()
        colorR = self.color.r
        colorG = self.color.g
        colorB = self.color.b
        colorA = self.color.a
        self.srcText.fill((colorR, colorG, colorB, colorA), special_flags=pygame.BLEND_RGBA_MULT)


        self.text = pygame.transform.scale(self.srcText, (int(width * glob.windowManager.getPixelSize() * (self.scale) / 3), int(height * glob.windowManager.getPixelSize() * (self.scale) / 3)))
        self.UpdateStats()

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](hoverLostAction[1])

    def __onClick__(self):
        for click in self.onClick:
            click[0](click[1])

    def disable(self):
        """
        Disable any transition and every input if enabled
        """
        self.enabled = False
        self.text.set_alpha(int((self.alpha/4)*255))
        self.HiddenColor(Color(self.color.r*0.3, self.color.g*0.3, self.color.b*0.3))


    def enable(self):
        """
        Enable any transition and every input if disabled
        """
        self.enabled = True
        self.text.set_alpha(self.alpha)
        self.HiddenColor(self.color)

    def HiddenColor(self, color):
        """
        Same as Color, but will not register color in variable, so can be cancelled with obj.Color(obj.color)
        :param color: Color of the sprite
        """
        self.srcText = self.unBlendedImg.convert_alpha()
        self.srcText.fill((color.r, color.g, color.b, color.a), special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onClick.append([function, kwargs])



    def Rotate(self, deg, fromScale=False):
        self.rotation = deg
        self.text = pygame.transform.rotate(self.text, deg)
        self.UpdateStats()

    def Text(self,text):
        self.unBlendedImg = self.font.render(text, True, (self.color.r, self.color.g, self.color.b, self.color.a))
        self.srcText = self.font.render(text, True, (self.color.r, self.color.g, self.color.b, self.color.a))
        self.text = self.font.render(text, True, (self.color.r, self.color.g, self.color.b, self.color.a))
        self.UpdateStats()
        self.Scale(self.scale)
        self.Fade(self.alpha)

    def Scale(self, x):
        if glob.windowManager.getPixelSize() > 1:
            sx = (1/glob.windowManager.getPixelSize())/2.2
        else:
            sx = (glob.windowManager.getPixelSize()) / 2.2
        self.scale = x
        width = self.srcText.get_width()
        height = self.srcText.get_height()
        self.text = pygame.transform.scale(self.srcText, (int(width * glob.windowManager.getPixelSize() * sx*x * self.vectorScale.x), int(height * glob.windowManager.getPixelSize() * sx*x * self.vectorScale.y)))
        self.UpdateStats()

    def Color(self, color):
        self.srcText = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcText.fill((color.r, color.g, color.b, color.a), special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)
        

    def VectorScale(self, vectorScale):
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        self.alpha = x
        self.text.set_alpha(255 * x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["position"]["beginTime"] = time.time()*1000
        self.transformations["position"]["endTime"] = time.time()*1000 + duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x,y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop



    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["fade"]["beginTime"] = time.time()*1000
        self.transformations["fade"]["endTime"] = time.time()*1000 + duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["colorFade"]["beginTime"] = time.time()*1000
        self.transformations["colorFade"]["endTime"] = time.time()*1000 + duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop



    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["VectorScale"]["beginTime"] = time.time()*1000
        self.transformations["VectorScale"]["endTime"] = time.time()*1000 + duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop


    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["scale"]["beginTime"] = time.time()*1000
        self.transformations["scale"]["endTime"] = time.time()*1000 + duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop
    def ClearTransformations(self, type=None):
        self.transformations = {"scale" : {}, "fade" : {}, "VectorScale": {}, "position": {}, "colorFade":{}, "rotation":{}}


    def UpdateStats(self):
        if self.field == Positions.topLeft:
            self.offset = vector2(0,0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(glob.windowManager.width/2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(glob.windowManager.width,0)
            self.posMult = -posMult
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, glob.windowManager.height/2)
        elif self.field == Positions.centre:
            self.offset = vector2(glob.windowManager.width/2, glob.windowManager.height/2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(glob.windowManager.width, glob.windowManager.height/2)
            self.posMult = -posMult
        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, glob.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(glob.windowManager.width/2, glob.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomRight:
            self.offset = vector2(glob.windowManager.width, glob.windowManager.height)
            self.posMultY = -posMult
            self.posMult = -posMult
        width = self.text.get_width()
        height = self.text.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width/2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height/2
        elif self.origin == Positions.centre:
            self.offset.x -= width/2
            self.offset.y -= height/2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height/2
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width/2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.originPosition.x + self.offset.x,
                                             self.originPosition.y + self.offset.y)

    def draw(self):
        if self.enabled:
            if self.text.get_rect().collidepoint(pygame.mouse.get_pos()) and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not self.text.get_rect().collidepoint(pygame.mouse.get_pos()) and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()
            if self.Clock == Clocks.game:
                now = time.time()*1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"]["endTime"] - self.transformations["rotation"][
                            "beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"]["endTime"] = now + duration
                        self.transformations["rotation"]["beginValue"] = endValue
                        self.transformations["rotation"]["endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Rotate(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))

            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - self.transformations["scale"][
                            "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"]["endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - self.transformations["fade"][
                            "beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"]["endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"]["beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"]["beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if self.vectorScale.x == endValueX and self.vectorScale.y == endValueY:
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"]["endTime"] - \
                                   self.transformations["VectorScale"][
                                       "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"]["endTime"] = now + duration
                        self.transformations["VectorScale"]["beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"]["endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(
                            vector2(helper.getTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                    helper.getTimeValue(beginTime, endtime, beginValueY, endValueY, easing)))
                    else:
                        self.VectorScale(
                            vector2(helper.getAudioTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                    helper.getAudioTimeValue(beginTime, endtime, beginValueY, endValueY, easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if self.color.r == endValueR and self.color.g == endValueG and self.color.b == endValueB:
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"]["endTime"] - self.transformations["colorFade"][
                            "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"]["endTime"] = now + duration
                        self.transformations["colorFade"]["beginValue"] = Color(endValueR, endValueG, endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime, beginValueR, endValueR, easing),
                            helper.getTimeValue(beginTime, endtime, beginValueG, endValueG, easing),
                            helper.getTimeValue(beginTime, endtime, beginValueB, endValueB, easing)))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime, beginValueR, endValueR, easing),
                            helper.getAudioTimeValue(beginTime, endtime, beginValueG, endValueG, easing),
                            helper.getAudioTimeValue(beginTime, endtime, beginValueB, endValueB, easing)))

            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if self.position.x == endValueX and self.position.y == endValueY:
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"]["endTime"] - self.transformations["position"][
                            "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"]["endTime"] = now + duration
                        self.transformations["position"]["beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(
                            helper.getTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                            helper.getTimeValue(beginTime, endtime, beginValueY, endValueY, easing))
                    else:
                        self.position = vector2(
                            helper.getAudioTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                            helper.getAudioTimeValue(beginTime, endtime, beginValueY, endValueY, easing))
        self.UpdateStats()
        if self.alpha != 0:
            glob.surface.blit(self.text,
                            (self.effectivePosition.x + glob.windowManager.getPixelSize()*
                            int(((self.originPosition.x + self.position.x*originMult) * self.posMult) *(glob.windowManager.getPixelSize()/1.3)),
                            self.effectivePosition.y + glob.windowManager.getPixelSize()*
                            int(((self.originPosition.y+ self.position.y*originMult) * self.posMultY))*(glob.windowManager.getPixelSize()/1.3)))