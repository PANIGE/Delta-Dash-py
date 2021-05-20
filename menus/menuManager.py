from framework.data.data import *
from menus import MainMenu
from menus import SongSelection
from menus import Play
from menus import rankingPanel
from framework import  glob


class MenuManager:
    def __init__(self):
        self.activeMenu = None
        self.MenuType = None

    def ChangeMenu(self, type):
        """Handle menu changing, disposing the actual menu """
        if self.activeMenu != None:
            self.activeMenu.dispose()
            disposeTime = self.activeMenu.disposeTime
            for sprite in glob.foregroundSprites.sprites:
                glob.Scheduler.AddDelayed(disposeTime, glob.foregroundSprites.remove, sprite=sprite)
        self.MenuType = type
        self.activeMenu = self.getMenuFromType(type)
        self.activeMenu.init()


    def getMenuFromType(self, type):
        if type == Menus.MainMenu:
            return MainMenu.MainMenu()
        elif type == Menus.SongSelection:
            return SongSelection.SongSelection()
        elif type == Menus.Playing:
            return Play.Gameplay()
        elif type == Menus.Ranking:
            return rankingPanel.rankingPanel()

    def HandleEvents(self, events):
        self.activeMenu.HandleEvents(events)


