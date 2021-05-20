import  time
from framework import  glob
import threading
import  pygame
from PIL import Image, ImageDraw

from easing_functions import *
from framework.data.data import *
from framework.graphics.pText import pText


def getAudioTimeValue(beginTime, finalTime, beginValue, endValue, easing=EaseTypes.linear):
    if pygame.mixer.music.get_busy():
        now = pygame.mixer.music.get_pos()
    else:
        now = finalTime
    timeSinceBegin = now-beginTime
    duration = finalTime-beginTime

    if timeSinceBegin < 0:
        return beginValue
    if timeSinceBegin > duration:
        return endValue
    advancement = timeSinceBegin/duration
    difference = endValue-beginValue
    return round( getEase(easing, beginValue, endValue, duration, advancement, difference), 4)


def getTimeValue(beginTime, finalTime, beginValue, endValue, easing=EaseTypes.linear):
    now = time.time() * 1000
    timeSinceBegin = now-beginTime
    duration = finalTime-beginTime

    if timeSinceBegin < 0:
        return beginValue
    if timeSinceBegin > duration:
        return endValue
    advancement = timeSinceBegin/duration
    difference = endValue-beginValue
    return round( getEase(easing, beginValue, endValue, duration, advancement, difference), 4)

def getSyncValue(beginValue, endValue, easing=EaseTypes.linear):
    advancement = glob.AudioManager.GetRelativePos()
    difference = endValue-beginValue
    final = round(getEase(easing, beginValue, endValue, glob.AudioManager.BeatLength(), advancement, difference), 4)
    if final < 0: return beginValue
    return final

def getParralax(x, y):
    screenX = glob.windowManager.width
    screenY = glob.windowManager.height
    return x-screenX/2, y-screenY/2


def getEase(type, begin, end, duration, advancement, difference):
    if type == EaseTypes.linear:
        return begin+advancement*difference
    if type == EaseTypes.easeIn:
        return begin+(QuadEaseIn(start=0, end=1, duration=100).ease(advancement*100)*difference)
    if type == EaseTypes.easeOut:
        return begin+(QuadEaseOut(start=0, end=1, duration=100).ease(advancement*100)*difference)
    if type == EaseTypes.easeInOut:
        return begin+(QuadEaseInOut(start=0, end=1, duration=100).ease(advancement*100)*difference)
    if type == EaseTypes.BounceIn:
        return begin+(BounceEaseIn(start=0, end=1, duration=100).ease(advancement*100)*difference)
    if type == EaseTypes.BounceOut:
        return begin+(BounceEaseOut(start=0, end=1, duration=100).ease(advancement*100)*difference)
    if type == EaseTypes.BounceEaseOut:
        return begin+(BounceEaseInOut(start=0, end=1, duration=100).ease(advancement*100)*difference)


def SetParalax(intensity):
    parraX, parraY = getParralax(glob.cursorPos.x, glob.cursorPos.y)
    return vector2(parraX / intensity / glob.windowManager.getPixelSize(), parraY / intensity / glob.windowManager.getPixelSize())

isQuitting = False

def GameQuit():
    global isQuitting
    if isQuitting:
        InstantQuit()
        return
    isQuitting = True
    try:
        glob.WindowLeft.dispose()
        glob.WindowCenter.dispose()
        glob.WindowRight.dispose()
    except:
        pass
    glob.AudioManager.play(glob.AudioManager.loadSound("goodbye.mp3", SkinSource.user))
    glob.AudioManager.Stop()
    glob.MenuManager.activeMenu.Transition = True
    for sprite in glob.foregroundSprites.sprites:
        sprite.FadeTo(0, 1000,EaseTypes.easeInOut)
    for sprite in glob.backgroundSprites.sprites:
        sprite.FadeTo(0, 5000,EaseTypes.easeInOut)
    for sprite in glob.overlaySprites.sprites:
        sprite.FadeTo(0,200, EaseTypes.easeInOut)
    goodbye = pText("Goodbye", 70, FontStyle.regular, vector2(0,0), Positions.centre, Positions.centre)
    glob.overlaySprites.add(goodbye)
    goodbye.FadeTo(0, 6000, EaseTypes.easeIn)
    glob.Scheduler.AddDelayed(6000, InstantQuit)

def InstantQuit():
    glob.Running = False



def getLN(length, approach):
    w, h = 1930, 1930
    shape = [(0, 0), (w, h)]

    # creating new Image object
    img = Image.new("RGBA", (w, h))

    # create pieslice image
    img1 = ImageDraw.Draw(img)
    img1.pieslice(shape, start=-90-(length/approach)*45, end=-90, fill=(255,255,255,150))
    return img.tobytes()

def getLNAngle(length, approach):
    return length/approach*45

def cornerBounds (sprite, rad):
    im = pygame.image.tostring(sprite.image, "RGBA")
    im = Image.frombytes("RGBA", (sprite.image.get_width(),sprite.image.get_height()), im, "raw")

    circle = Image.new ('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw (circle)
    draw.ellipse ((0, 0, rad * 2, rad * 2), fill = 255)
    alpha = Image.new ('L', im.size, 255)
    w, h = im.size
    alpha.paste (circle.crop ((0, 0, rad, rad)), (0, 0))
    alpha.paste (circle.crop ((0, rad, rad, rad * 2)), (0, h-rad))
    alpha.paste (circle.crop ((rad, 0, rad * 2, rad)), (w-rad, 0))
    alpha.paste (circle.crop ((rad, rad, rad * 2, rad * 2)), (w-rad, h-rad))
    im.putalpha (alpha)
    return im.tobytes()

