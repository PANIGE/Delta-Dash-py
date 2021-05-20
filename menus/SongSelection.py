from framework.graphics.pSprite import pSprite
from framework.graphics.pText import pText
from framework.gameplayElements.pButton import pButton
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
import pygame
from os import path
import time
import os


class SongSelection:
    """Song Selection menu"""
    def __init__(self):
        self.Transition = False
        self.disposeTime = 400
        self.SoundHover = glob.AudioManager.loadSound("button-hover.wav", SkinSource.local)
        self.SoundClick = glob.AudioManager.loadSound("button-select.wav", SkinSource.local)
        self.SoundBack = glob.AudioManager.loadSound("button-back.wav", SkinSource.local)
        self.SoundChange = glob.AudioManager.loadSound("song-change.wav", SkinSource.local)

        self.tabBg = None
        self.tabPic = None
        self.tabPicBg = None

        self.PlayButton = None

        self.songTitle = None
        self.songArtist = None
        self.songMapper = None
        self.songBPM = None
        self.ezDefRating = None
        self.hrDefRating = None
        self.inDefRating = None
        self.offset = 0

        self.DifficultyRating = None
        self.NoteSpeed = None
        self.health = None
        self.Accuracy = None
        self.Length = None
        self.objCount = None

        self.isMouseDown = False
        self.oldMousePos = None
        self.selectorLastActive = time.time() * 1000
        self.selectorInPlace = True
        self.selectorInPlaceOffset = 0

        self.scoreScore = None
        self.scoreAcc = None
        self.scoreConsistency = None
        self.scoreCombo = None
        self.scoreRank = None
        self.scorePerf = None
        self.scoreGood = None
        self.scoreMeh = None
        self.scoreMiss = None
        self.diffName = None
        self.diffNameOverlay = None
        self.songList = []

    def init(self):
        if not glob.AudioManager.isPlaying:
            glob.AudioManager.Unpause(False)
        glob.Framerate = 30
        background = pSprite(glob.PixelWhite, vector2(0, 0), SkinSource.local, Positions.topCentre, Positions.topCentre,
                             Color(20, 20, 20))
        background.VectorScale(vector2(glob.windowManager.widthScaled, glob.windowManager.heightScaled))
        background.AlphaMask("songSelectBg.png")
        glob.foregroundSprites.add(background)

        bottomBar = pSprite(glob.PixelWhite, vector2(0, 0), SkinSource.local, Positions.bottomCentre,
                            Positions.bottomCentre, Color(50, 50, 50))
        bottomBar.VectorScale(vector2(1920, 100))
        glob.foregroundSprites.add(bottomBar)

        button = pButton("Back", vector2(200, 100), FontStyle.regular,
                         vector2(100, glob.windowManager.heightScaled - 50),
                         Color(255, 120, 174))
        button.text.position = vector2(0, 20)
        button.onClick(glob.AudioManager.play, sound=self.SoundBack)
        button.onClick(glob.MenuManager.ChangeMenu, type=Menus.MainMenu)
        glob.foregroundSprites.add(button)

        play_button = pButton("Start", vector2(200, 100), FontStyle.regular,
                              vector2(glob.windowManager.widthScaled - 100, glob.windowManager.heightScaled - 50),
                              Color(52, 237, 132))
        play_button.text.position = vector2(-10, 20)
        play_button.onClick(glob.AudioManager.play, sound=self.SoundClick)
        play_button.onClick(glob.MenuManager.ChangeMenu, type=Menus.Playing)
        glob.foregroundSprites.add(play_button)
        self.PlayButton = play_button

        if "/data/files/intro" in glob.AudioManager.currentSong["folder"]:
            glob.AudioManager.Skip()
        glob.AudioManager.ChangeBackground(glob.AudioManager.currentSong["folder"] + "/background.png", 400)

        tab = pSprite(glob.AudioManager.currentSong["folder"] + "/background.png", vector2(45, 0), SkinSource.absolute,
                      Positions.centreLeft, Positions.centreLeft)
        tab.BottomGradiant(Color(50, 50, 50), "half")
        tab.crop(600, 800)
        tab.borderBounds(10)
        glob.foregroundSprites.add(tab)
        self.tabBg = tab
        tab.Fade(0)
        tab.FadeTo(1, 400)
        songSelectionHeader = pSprite("SongSelectionHeader.png", vector2(0, 0), SkinSource.local, Positions.topCentre,
                                      Positions.topCentre, Color(50, 50, 50))

        tabPicBg = pSprite(glob.PixelWhite, vector2(95, 390), SkinSource.local, Positions.centreLeft,
                           Positions.bottomLeft)
        tabPicBg.VectorScale(vector2(500, 500))
        tabPicBg.borderBounds(10)
        self.tabPicBg = tabPicBg
        glob.foregroundSprites.add(tabPicBg)
        tabPic = pSprite(glob.AudioManager.currentSong["folder"] + "/thumb.png", vector2(105, 380), SkinSource.absolute,
                         Positions.centreLeft, Positions.bottomLeft)
        tabPic.Scale(480 / tabPic.image.get_width() * glob.windowManager.getPixelSize())
        tabPic.borderBounds(10)
        glob.foregroundSprites.add(tabPic)
        self.tabPic = tabPic

        SongTitle = pText(glob.AudioManager.currentSong["name"], 45, FontStyle.bold, vector2(20, 0),
                          Positions.centreRight, Positions.centreRight)
        glob.foregroundSprites.add(SongTitle)
        self.songTitle = SongTitle

        SongArtist = pText(glob.AudioManager.currentSong["artist"], 45, FontStyle.regular, vector2(20, 30),
                           Positions.centreRight, Positions.centreRight)
        glob.foregroundSprites.add(SongArtist)

        self.songArtist = SongArtist

        SongBpm = pText(str(glob.AudioManager.currentSong["bpm"]) + "bpm", 45, FontStyle.thin, vector2(20, 60),
                        Positions.centreRight, Positions.centreRight)
        glob.foregroundSprites.add(SongBpm)
        self.songBPM = SongBpm

        SongMapper = pText(str("Map created by " + glob.AudioManager.currentSong["mapper"]), 45, FontStyle.thin,
                           vector2(20, 90), Positions.centreRight, Positions.centreRight)
        glob.foregroundSprites.add(SongMapper)
        self.songMapper = SongMapper

        diffEasy = pSprite(glob.PixelWhite, vector2(300, 250), SkinSource.local, Positions.centre, Positions.topLeft,
                           Color(62, 194, 194))
        diffEasy.VectorScale(vector2(200, 150))
        diffEasy.onHover(glob.AudioManager.play, sound=self.SoundHover)
        diffEasy.onHover(diffEasy.FadeTo, value=1, duration=100)
        diffEasy.onClick(self.loadDiff, difficulty=Difficulty.Normal)
        diffEasy.onHoverLost(diffEasy.FadeTo, value=0.8, duration=100)
        diffEasy.tag = "EasyDifficulty"
        diffEasy.borderBounds(20)

        diffEasy.Fade(0.8)
        glob.foregroundSprites.add(diffEasy)

        diffHard = pSprite(glob.PixelWhite, vector2(510, 250), SkinSource.local, Positions.centre, Positions.topLeft,
                           Color(189, 163, 60))
        diffHard.VectorScale(vector2(200, 150))
        diffHard.onHover(glob.AudioManager.play, sound=self.SoundHover)
        diffHard.onHover(diffHard.FadeTo, value=1, duration=100)
        diffHard.onClick(self.loadDiff, difficulty=Difficulty.Hard)
        diffHard.onHoverLost(diffHard.FadeTo, value=0.8, duration=100)
        diffHard.tag = "HardDifficulty"

        diffHard.Fade(0.8)
        glob.foregroundSprites.add(diffHard)

        diffInsane = pSprite(glob.PixelWhite, vector2(720, 250), SkinSource.local, Positions.centre, Positions.topLeft,
                             Color(147, 60, 194))
        diffInsane.VectorScale(vector2(200, 150))
        diffInsane.onHover(glob.AudioManager.play, sound=self.SoundHover)
        diffInsane.onHover(diffInsane.FadeTo, value=1, duration=100)
        diffInsane.onClick(self.loadDiff, difficulty=Difficulty.Insane)
        diffInsane.onHoverLost(diffInsane.FadeTo, value=0.8, duration=100)
        diffInsane.tag = "InsaneDifficulty"


        diffInsane.Fade(0.8)
        glob.foregroundSprites.add(diffInsane)

        EasyText = pText("Normal", 40, FontStyle.regular, vector2(227, 220), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(EasyText)
        EasyText.tag = "EasyDifficulty"

        EasyDiff = pText("-", 50, FontStyle.heavy, vector2(227, 190), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(EasyDiff)
        EasyDiff.tag = "EasyDifficulty"
        self.ezDefRating = EasyDiff

        HardText = pText("Hard", 40, FontStyle.regular, vector2(347, 220), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(HardText)
        HardText.tag = "HardDifficulty"

        HardDiff = pText("-", 50, FontStyle.heavy, vector2(347, 190), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(HardDiff)
        HardDiff.tag = "HardDifficulty"
        self.hrDefRating = HardDiff

        InsaneText = pText("Insane", 40, FontStyle.regular, vector2(467, 220), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(InsaneText)
        InsaneText.tag = "InsaneDifficulty"

        InsaneDiff = pText("-", 50, FontStyle.heavy, vector2(467, 190), Positions.centre, Positions.bottomCentre)
        glob.foregroundSprites.add(InsaneDiff)
        InsaneDiff.tag = "InsaneDifficulty"
        self.inDefRating = InsaneDiff

        RankLetter = pSprite("/ranks/x.png", vector2(-50, -230), SkinSource.local, Positions.centre, Positions.centre)
        RankLetter.Scale(0.8)
        self.scoreRank = RankLetter
        glob.foregroundSprites.add(RankLetter)

        value = pText("Score: -", 35, FontStyle.regular, vector2(-170, 0), Positions.centre, Positions.centreLeft)
        self.scoreScore = value
        glob.foregroundSprites.add(self.scoreScore)

        value = pText("Accuracy: -", 35, FontStyle.regular, vector2(-170, 30), Positions.centre, Positions.centreLeft)
        self.scoreAcc = value
        glob.foregroundSprites.add(self.scoreAcc)

        value = pText("Unstable Rate: -", 35, FontStyle.regular, vector2(-170, 60), Positions.centre,
                      Positions.centreLeft)
        self.scoreConsistency = value
        glob.foregroundSprites.add(self.scoreConsistency)

        value = pText("Combo: -", 35, FontStyle.regular, vector2(-170, 90), Positions.centre, Positions.centreLeft)
        self.scoreCombo = value
        glob.foregroundSprites.add(self.scoreCombo)

        value = pText("Perfect Hits: -", 35, FontStyle.regular, vector2(-170, 120), Positions.centre,
                      Positions.centreLeft)
        self.scorePerf = value
        glob.foregroundSprites.add(self.scorePerf)

        value = pText("Good Hits: -", 35, FontStyle.regular, vector2(-170, 150), Positions.centre, Positions.centreLeft)
        self.scoreGood = value
        glob.foregroundSprites.add(self.scoreGood)

        value = pText("Meh Hits: -", 35, FontStyle.regular, vector2(-170, 180), Positions.centre, Positions.centreLeft)
        self.scoreMeh = value
        glob.foregroundSprites.add(self.scoreMeh)

        value = pText("Misses: -", 35, FontStyle.regular, vector2(-170, 210), Positions.centre, Positions.centreLeft)
        self.scoreMiss = value
        glob.foregroundSprites.add(self.scoreMiss)

        background.Fade(0)
        button.Fade(0)

        self.DifficultyRating = pText("Difficulty Rating | -", 45, FontStyle.thin, vector2(20, -50),
                                      Positions.centreRight, Positions.centreRight)
        self.NoteSpeed = pText("Note Speed | -", 45, FontStyle.thin, vector2(20, -80), Positions.centreRight,
                               Positions.centreRight)
        self.health = pText("Health Drain | -", 45, FontStyle.thin, vector2(20, -110), Positions.centreRight,
                            Positions.centreRight)
        self.Accuracy = pText("Accuracy needed | -", 45, FontStyle.thin, vector2(20, -140), Positions.centreRight,
                              Positions.centreRight)
        self.objCount = pText("Object count | -", 45, FontStyle.thin, vector2(20, -170), Positions.centreRight,
                              Positions.centreRight)
        self.Length = pText("Length | -", 45, FontStyle.thin, vector2(20, -200), Positions.centreRight,
                            Positions.centreRight)
        self.diffName = pText("-", 120, FontStyle.heavy, vector2(20, -250), Positions.centreRight,
                              Positions.centreRight)
        self.diffNameOverlay = pText("-", 120, FontStyle.heavy, vector2(20, -250), Positions.centreRight,
                              Positions.centreRight)
        self.diffName.Fade(0.5)
        self.diffNameOverlay.Fade(0.5)
        glob.foregroundSprites.add(self.diffName)
        glob.foregroundSprites.add(self.diffNameOverlay)
        glob.foregroundSprites.add(self.DifficultyRating)
        glob.foregroundSprites.add(self.NoteSpeed)
        glob.foregroundSprites.add(self.health)
        glob.foregroundSprites.add(self.Accuracy)
        glob.foregroundSprites.add(self.objCount)
        glob.foregroundSprites.add(self.Length)

        background.FadeTo(1, 400)
        button.FadeTo(1, 400)
        glob.foregroundSprites.add(songSelectionHeader)
        songs = os.listdir(glob.currentDirectory + "/.user/maps")

        indexMin = 0 - 0.5 * len(songs)
        index = 0

        for song in songs:
            songSprite = pSprite(glob.currentDirectory + "/.user/maps/" + song + "/thumb.png", vector2(0, 0),
                                 SkinSource.absolute, Positions.topCentre, Positions.topCentre)
            songSprite.Scale(150 / songSprite.image.get_width()*glob.windowManager.getPixelSize())
            songSprite.position = vector2((indexMin + index) * 160, -20 - abs((indexMin + index) * 10))
            songSprite.tag = "SongSelectSprite"
            if glob.currentDirectory + "/.user/maps/" + song == glob.AudioManager.currentSong["folder"]:
                self.offset = (indexMin + index) * 160
            glob.foregroundSprites.add(songSprite)
            self.songList.append(songSprite)
            songSprite.onHover(songSprite.VectorScaleTo, scale=vector2(1.1, 1.1), duration=200,
                               easing=EaseTypes.BounceOut)
            songSprite.onHover(glob.AudioManager.play, sound=self.SoundHover)
            songSprite.onHoverLost(songSprite.VectorScaleTo, scale=vector2(1, 1), duration=100,
                                   easing=EaseTypes.easeInOut)
            songSprite.onClick(glob.AudioManager.play, sound=self.SoundChange)
            songSprite.onClick(self.GetNewSong, songPath=song, difficulty=Difficulty.Normal, sender=songSprite)
            songSprite.data.append((indexMin + index) * 160)
            songSprite.data.append(glob.currentDirectory + "/.user/maps/" + song)
            index += 1
        self.loadDiffs()

    def GetNewSong(self, songPath, sender, difficulty=None):
        songPath = "/.user/maps/" + songPath
        if not glob.currentDirectory + songPath == glob.AudioManager.currentSong["folder"]:
            glob.AudioManager.Stop(False)
            glob.AudioManager.PlayMusic(songFolder=songPath, Preview=True)
            glob.AudioManager.ChangeBackground(glob.currentDirectory + songPath + "/background.png", 100)
            self.songTitle.Text(glob.AudioManager.currentSong["name"])
            self.songArtist.Text(glob.AudioManager.currentSong["artist"])
            self.songBPM.Text(str(glob.AudioManager.currentSong["bpm"]) + "bpm")
            self.songMapper.Text("Map created by " + glob.AudioManager.currentSong["mapper"])
            tab = pSprite(glob.AudioManager.currentSong["folder"] + "/background.png", vector2(45, 0),
                          SkinSource.absolute, Positions.centreLeft, Positions.centreLeft)
            tab.BottomGradiant(Color(50, 50, 50), "half")
            tab.crop(600, 800)
            self.tabBg.FadeTo(0, 100)
            tab.Fade(0)
            tab.FadeTo(1, 100)
            tab.borderBounds(10)
            glob.Scheduler.AddDelayed(100, glob.foregroundSprites.remove, sprite=self.tabBg)
            self.tabBg = tab
            glob.foregroundSprites.add(self.tabBg)

            tabPic = pSprite(glob.AudioManager.currentSong["folder"] + "/thumb.png", vector2(105, 380),
                             SkinSource.absolute, Positions.centreLeft, Positions.bottomLeft)
            tabPic.Scale(480 / tabPic.image.get_width() * glob.windowManager.getPixelSize())
            self.tabPic.FadeTo(0, 100)
            tabPic.Fade(0)
            tabPic.FadeTo(1, 100)
            tabPic.borderBounds(10)
            glob.foregroundSprites.remove(self.tabPicBg)
            glob.foregroundSprites.add(self.tabPicBg)
            glob.Scheduler.AddDelayed(100, glob.foregroundSprites.remove, sprite=self.tabPic)
            glob.foregroundSprites.add(tabPic)
            self.tabPic = tabPic
            self.selectorInPlaceOffset = sender.data[0]
            glob.Scheduler.AddNow(self.updateOffset, to=sender.data[0], duration=500, easing=EaseTypes.easeOut)
            self.loadDiffs()
            if difficulty is not None:
                self.loadDiff(difficulty)

    def loadDiffs(self):
        seconds = str(int((glob.AudioManager.currentSong["length"] / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0" + seconds
        minutes = str(int((glob.AudioManager.currentSong["length"] / 1000 / 60) % 60))
        self.Length.Text("Length | {}:{}".format(minutes, seconds))
        if path.exists(glob.AudioManager.currentSong["folder"] + "/normal.dd"):
            with open(glob.AudioManager.currentSong["folder"] + "/normal.dd") as f:
                data = f.read().split("\n")
                for sprite in glob.foregroundSprites.sprites:
                    if sprite.tag == "EasyDifficulty":
                        sprite.enable()
                self.ezDefRating.Text(data[0].split("|")[0])
                diffEasy = True
        else:
            diffEasy = False
            for sprite in glob.foregroundSprites.sprites:
                if sprite.tag == "EasyDifficulty":
                    sprite.disable()

        if path.exists(glob.AudioManager.currentSong["folder"] + "/hard.dd"):
            with open(glob.AudioManager.currentSong["folder"] + "/hard.dd") as f:
                data = f.read().split("\n")

                for sprite in glob.foregroundSprites.sprites:
                    if sprite.tag == "HardDifficulty":
                        sprite.enable()
            self.hrDefRating.Text(data[0].split("|")[0])
            diffHard = True
        else:
            diffHard = False
            for sprite in glob.foregroundSprites.sprites:
                if sprite.tag == "HardDifficulty":
                    sprite.disable()

        if path.exists(glob.AudioManager.currentSong["folder"] + "/insane.dd"):
            with open(glob.AudioManager.currentSong["folder"] + "/insane.dd") as f:
                data = f.read().split("\n")

                for sprite in glob.foregroundSprites.sprites:
                    if sprite.tag == "InsaneDifficulty":
                        sprite.enable()
            self.inDefRating.Text(data[0].split("|")[0])
            diffInsane = True
        else:
            diffInsane = False
            for sprite in glob.foregroundSprites.sprites:
                if sprite.tag == "InsaneDifficulty":
                    sprite.disable()
        if diffEasy:
            return self.loadDiff(Difficulty.Normal)
        elif diffHard:
            return self.loadDiff(Difficulty.Hard)
        elif diffInsane:
            return self.loadDiff(Difficulty.Insane)
        else:
            return self.loadDiff(None)

    def updateOffset(self, to, duration, easing=EaseTypes.linear):
        origin = self.offset
        now = time.time() * 1000
        while self.offset != to:
            self.offset = helper.getTimeValue(now, now + duration, origin, to, easing)

    def loadDiff(self, difficulty):
        if difficulty is None:
            self.Accuracy.Text("Accuracy Needed | -")
            self.NoteSpeed.Text("Note Speed | -")
            self.health.Text("Health Drain | -")
            self.DifficultyRating.Text("Difficulty Rating | -")
            self.diffName.Text("-")
            self.diffNameOverlay.Text("-")

            self.PlayButton.disable()

        elif difficulty == Difficulty.Normal:
            if path.exists(glob.AudioManager.currentSong["folder"] + "/normal.dd"):
                with open(glob.AudioManager.currentSong["folder"] + "/normal.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text("Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text("Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Normal")
                    self.diffNameOverlay.Text("Normal")
                    glob.Difficulty = Difficulty.Normal
                    self.PlayButton.enable()
            else:
                self.loadDiff(None)
        elif difficulty == Difficulty.Hard:
            if path.exists(glob.AudioManager.currentSong["folder"] + "/hard.dd"):
                with open(glob.AudioManager.currentSong["folder"] + "/hard.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text("Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text("Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Hard")
                    self.diffNameOverlay.Text("Hard")
                    glob.Difficulty = Difficulty.Hard
                    self.PlayButton.enable()
            else:
                self.loadDiff(None)
        elif difficulty == Difficulty.Insane:
            if path.exists(glob.AudioManager.currentSong["folder"] + "/insane.dd"):
                with open(glob.AudioManager.currentSong["folder"] + "/insane.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text("Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text("Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Insane")
                    self.diffNameOverlay.Text("Insane")
                    glob.Difficulty = Difficulty.Insane
                    self.PlayButton.enable()

            else:
                self.loadDiff(None)
        self.setScore(difficulty)

    def setScore(self, difficulty):
        if difficulty == Difficulty.Normal:
            text = "normal"
        elif difficulty == Difficulty.Hard:
            text = "hard"
        elif difficulty == Difficulty.Insane:
            text = "insane"
        else:
            text = "none"
        sqlData = glob.db.fetch(
            "SELECT * FROM scores WHERE mapid = {} and difficulty = '{}' ORDER BY score DESC".format(glob.AudioManager.currentSong["id"],
                                                                                 text))
        if sqlData is None:
            self.scoreScore.Text("Score: -")
            self.scoreAcc.Text("Accuracy: -")
            self.scoreConsistency.Text("Unstable Rate: -")
            self.scoreCombo.Text("Combo: -")
            self.scorePerf.Text("Perfect Hits: -")
            self.scoreGood.Text("Good Hits: -")
            self.scoreMeh.Text("Meh Hits: -")
            self.scoreMiss.Text("Misses: -")
            RankLetter = pSprite("/ranks/x.png", vector2(-50, -210), SkinSource.local, Positions.centre,
                                 Positions.centre)
            RankLetter.Scale(0.8)
            RankLetter.Fade(0)
            RankLetter.FadeTo(1, 200)
            self.scoreRank.FadeTo(0, 200)
            glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=self.scoreRank)
            glob.foregroundSprites.add(RankLetter)
            self.scoreRank = RankLetter
        else:
            self.scoreScore.Text("Score: {}".format(sqlData["score"]))
            self.scoreAcc.Text("Accuracy: {}%".format(sqlData["accuracy"]))
            self.scoreConsistency.Text("Unstable Rate: {}ms".format(sqlData["consistency"]))
            self.scoreCombo.Text("Combo: {}x".format(sqlData["comboMax"]))
            self.scorePerf.Text("Perfect Hits: {}".format(sqlData["countPerf"]))
            self.scoreGood.Text("Good Hits: {}".format(sqlData["countGood"]))
            self.scoreMeh.Text("Meh Hits: {}".format(sqlData["countMeh"]))
            self.scoreMiss.Text("Misses: {}".format(sqlData["countMiss"]))
            RankLetter = pSprite("/ranks/{}.png".format(sqlData["rank"]), vector2(-50, -210), SkinSource.local,
                                 Positions.centre,
                                 Positions.centre)
            RankLetter.Scale(0.8)
            RankLetter.Fade(0)
            RankLetter.FadeTo(1, 200)
            self.scoreRank.FadeTo(0, 200)
            glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=self.scoreRank)
            glob.foregroundSprites.add(RankLetter)
            self.scoreRank = RankLetter

    def update(self):
        self.diffNameOverlay.Scale(helper.getSyncValue(1,1.1, EaseTypes.easeOut))
        self.diffNameOverlay.Fade(helper.getSyncValue(0.5,0, EaseTypes.easeOut))
        self.tabPicBg.Fade(helper.getSyncValue(1,0.9, EaseTypes.easeOut))
        index = 0
        indexMin = 0 - 0.5 * len(self.songList)
        indexMax = len(self.songList) - 0.5 * len(self.songList)
        if self.isMouseDown:
            self.selectorLastActive = time.time() * 1000
            self.selectorInPlace = False
            move = self.oldMousePos.x - glob.cursorPos.x
            if indexMax * 160 > self.offset + move > indexMin * 160:
                self.offset += move
        self.oldMousePos = glob.cursorPos

        for sprite in self.songList:
            sprite.position = vector2(((indexMin + index) * 160) - self.offset,
                                      -20 - abs((indexMin + index - self.offset / 160) * 10))
            index += 1

        if (time.time() * 1000) - self.selectorLastActive > 5000 and not self.selectorInPlace:
            self.selectorInPlace = True
            glob.Scheduler.AddNow(self.updateOffset, to=self.selectorInPlaceOffset, duration=500,
                                  easing=EaseTypes.easeOut)


    def dispose(self):
        for sprite in glob.foregroundSprites.sprites:
            sprite.FadeTo(0, 400)
        pass

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                glob.AudioManager.play(self.SoundBack)
                glob.MenuManager.ChangeMenu(Menus.MainMenu)
            if event.type == pygame.KEYDOWN:
                if not self.Transition:
                    if event.key == K_ESCAPE:
                        glob.AudioManager.play(self.SoundBack)
                        glob.MenuManager.ChangeMenu(Menus.MainMenu)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 2):
                    self.isMouseDown = True
                if event.button == 4: glob.AudioMeter.ChangeVolume(True)
                if event.button == 5: glob.AudioMeter.ChangeVolume(False)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 2):
                    self.isMouseDown = False
            if event.type == glob.UserEvents["MUSIC_END"]:
                glob.AudioManager.SeekPreview()

