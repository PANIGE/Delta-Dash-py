from framework.data.data import *
class SpriteManager:
    def __init__(self):
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
        except:
            pass

    def draw(self):
        for sprite in self.sprites:
            sprite.draw()

    def clearTransformations(self):
        for sprite in self.sprites:
            sprite.ClearTransformations()

    def Clear(self):
        self.sprites.clear()

    def Position(self, x, y):
        for sprite in self.sprites:
            sprite.position = vector2(x, y)