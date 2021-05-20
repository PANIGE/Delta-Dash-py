"""
Contain all small assets that are useful everywhere
"""


import wx
app = wx.App(False)
class Positions:
    topLeft = 0
    topCentre = 1
    topRight = 2
    centreLeft = 3
    centre = 4
    centreRight = 5
    bottomLeft = 6
    bottomCentre = 7
    bottomRight = 8

class SkinSource:
    local = 0
    user = 1
    absolute = 2


class EaseTypes:
    linear = 0
    easeIn = 1
    easeOut = 2
    easeInOut = 3
    BounceIn = 4
    BounceOut = 5


class vector2:
    """Used to determine a position, but more explicit than tuples"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, x):
        if type(x) not in (vector2, int, float):
            raise TypeError("can only multiply vector2 by another vector2 or int/floats")
        if type(x) in (int, float):
            return vector2(self.x * x, self.y * x)
            
        else:
            return vector2(self.x * x.x, self.y * x.y)

    def __str__(self):
        return "Vector2({},{})".format(self.x, self.y)


class vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Vector3({},{},{})".format(self.x, self.y, self.z)

class Color:

    def __init__(self, r,g,b,a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return "Color({},{},{},{})".format(self.r, self.g, self.b, self.a)

    def __mul__(self, x):
        if type(x) not in (vector2, int, float):
            raise TypeError("can only multiply color by  int/floats or color object")
        if type(x) in (int, float):
            return Color(self.r * x, self.g * x, self.b * x)

        else:
            return Color(self.r * x.r, self.g * x.g, self.b * x.b)

class WindowManager:
    def __init__(self):
        self.width, self.height = 0,0
        self.widthScaled, self.heightScaled = 1920,1080

    def getPixelSize(self):
        return self.width/1920

class Clocks:
    game = 0
    audio = 1

class Direction:
    forward = 1
    backward = -1


class Notes:
    short = 0
    long = 1
    double = 2

class NotePos:
    Upper = 0
    Lower = 1

class TransformationType:
    all = 0
    fade = 1
    scale = 2
    VectorScale = 3
    Translation = 4

class Menus:
    MainMenu = 0
    SongSelection = 1
    Playing = 2
    Ranking = 3


class FontStyle:
    bold = "Bold.otf"
    regular = "Regular.otf"
    heavy = "Heavy.otf"
    light = "Light.otf"
    semiBold = "SemiBold.otf"
    thin = "Thin.otf"

class NotificationType:
    Info = 0
    Warning = 1
    Error = 2

class Difficulty:
    Normal = 0
    Hard = 1
    Insane = 2