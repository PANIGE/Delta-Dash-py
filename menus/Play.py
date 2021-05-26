from framework.graphics.pSprite import pSprite
from framework.graphics.pText import pText
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
from framework.gameplayElements.pNote import pNote
from menus.overlays.pNotification import *
import pygame
import time


class Gameplay:
    def __init__(self):
        self.Transition = False
        self.disposeTime = 400
        self.progressBar = None
        self.LengthTime = None
        self.healthBar = None
        self.comboIndicator = None
        self.comboIndicatorOv = None
        self.score = 0
        self.combo = 0
        self.upperOv = None
        self.lowerOv = None
        self.accBar = None
        self.touchSound = glob.AudioManager.loadSound("play-touch.mp3", SkinSource.user)
        self.hitSound = glob.AudioManager.loadSound("play-hit.mp3", SkinSource.user)
        self.failSound = glob.AudioManager.loadSound("failsound.mp3", SkinSource.user)
        self.SoundHover = glob.AudioManager.loadSound("button-hover.wav", SkinSource.local)
        self.SoundClick = glob.AudioManager.loadSound("button-select.wav", SkinSource.local)
        self.key1Holt = False
        self.key2Holt = False
        self.isLoading = True
        self.fileBody = ""
        self.hp = 0
        self.ar = 0
        self.od = 0

        self.unstableRate = []
        self.accList = []
        self.maxCombo = 0

        self.ClosingTime = 0

        self.upperSprites = []
        self.lowerSprites = []


        self.ScoreIndicator = None
        self.LifeBar = None
        self.life = 100
        self.failed = False
        self.finished = False
        self.failOverlay = None
        self.failRetry = None
        self.failQuit = None
        self.Loading = None

        #used for sprite Caching
        self.UpperSprite = None
        self.LowerSprite = None
        self.paused = False

    def init(self):
        glob.AudioManager.Restart()
        glob.AudioManager.Pause()
        difficulties = {Difficulty.Normal : "normal.dd", Difficulty.Hard : "hard.dd", Difficulty.Insane : "insane.dd"}
        difficulty = difficulties[glob.Difficulty]
        with open(glob.AudioManager.currentSong["folder"] + "/" + difficulty) as f:
            file = f.read()
            data = data = file.split("\n")[0].split("|")
            self.fileBody = file.split("\n")[1:]
            if len(self.fileBody) == 0: #Empty map will generate bugs within the menu
                glob.MenuManager.ChangeMenu(type=Menus.SongSelection)
                NotificationMassive(text="Beatmap is empty", duration=5000, type=NotificationType.Error).show()
                return



        self.hp = (float(data[1])+1)*10
        self.ar = 1/(1+float(data[2]))*3000

        self.od = 1/(1+float(data[3])/3)*200


        glob.Framerate = 30
        glob.backgroundSprites.sprites[0].FadeTo(0.1, 400)

        accBar = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre, Color(0, 246, 226))
        accBar.Fade(0.5)
        accBar.VectorScale(vector2(5,glob.windowManager.heightScaled))
        self.accBar = accBar
        glob.foregroundSprites.add(accBar)

        lowerStruct = pSprite("gameplay-struct.png", vector2(0, 0), SkinSource.user, Positions.bottomCentre,
                              Positions.bottomCentre)

        lowerStruct.Scale(0.8)



        glob.foregroundSprites.add(lowerStruct)

        upperStruct = pSprite("gameplay-struct.png", vector2(0,0), SkinSource.user, Positions.topCentre, Positions.topCentre)
        upperStruct.Scale(0.8)
        upperStruct.Rotate(180)



        upperStruct.Color(Color(176, 156, 255))
        lowerStruct.Color(Color(255, 153, 153))


        self.Loading = pText("Beatmap is Loading", 60, FontStyle.bold, vector2(0,0), Positions.topCentre, Positions.topCentre)
        self.Loading.FadeTo(0.5,2000,EaseTypes.easeInOut, True)

        self.lowerOv = pSprite("gameplay-struct-ov.png", vector2(0, 0), SkinSource.user, Positions.bottomCentre,
                          Positions.bottomCentre)
        self.lowerOv .Scale(0.8)
        self.lowerOv.Fade(0)

        self.upperOv = pSprite("gameplay-struct-ov.png", vector2(0, 0), SkinSource.user, Positions.topCentre,
                              Positions.topCentre)
        self.upperOv.Scale(0.8)
        self.upperOv.Fade(0)


        glob.foregroundSprites.add(upperStruct)

        self.progressBar = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.bottomLeft, Positions.bottomLeft)
        glob.foregroundSprites.add(self.progressBar)
        self.progressBar.VectorScale(vector2(0, 5))
        self.LengthTime = pText("00:00", 40, FontStyle.regular,vector2(0,10), Positions.bottomLeft, Positions.bottomLeft)
        glob.foregroundSprites.add(self.LengthTime)
        seconds = str(int((glob.AudioManager.currentSong["length"] / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0" + seconds
        minutes = str(int((glob.AudioManager.currentSong["length"] / 1000 / 60) % 60))
        totalLength = pText("{}:{}".format(minutes, seconds), 40, FontStyle.regular,vector2(0,10), Positions.bottomRight, Positions.bottomRight)
        glob.foregroundSprites.add(totalLength)




        self.upperSprites.sort(key=lambda x: x.time) # Rearrange sprites to be sure it will be handled in the right order


        self.comboIndicator = pText("0x", 100, FontStyle.regular, vector2(0,0), Positions.centre, Positions.centre)
        self.comboIndicatorOv = pText("0x", 100, FontStyle.regular, vector2(0,0), Positions.centre, Positions.centre)

        self.ScoreIndicator = pText("0", 50, FontStyle.regular, vector2(10,0), Positions.topRight, Positions.topRight)
        self.lifeBar = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.topLeft, Positions.topLeft)
        self.lifeBar.VectorScale(vector2(1920,5))

        glob.foregroundSprites.add(self.comboIndicator)
        glob.foregroundSprites.add(self.comboIndicatorOv)
        glob.foregroundSprites.add(self.ScoreIndicator)
        glob.foregroundSprites.add(self.lifeBar)



        glob.foregroundSprites.add(self.upperOv)
        glob.foregroundSprites.add(self.lowerOv)


        self.failOverlay = pSprite("fail-background.png", vector2(0,0), SkinSource.user, Positions.centre, Positions.centre)
        self.failOverlay.Scale(glob.windowManager.width / self.failOverlay.image.get_width())
        self.failOverlay.Fade(0)
        glob.foregroundSprites.add(self.failOverlay)

        self.failRetry = pSprite("fail-retry.png", vector2(0,30), SkinSource.user, Positions.centre, Positions.centre)
        self.failRetry.Scale(0.7)
        self.failRetry.Fade(0)

        self.failRetry.onHover(self.failRetry.ScaleTo, scale=0.75, duration=200)
        self.failRetry.onHover(glob.AudioManager.play, sound=self.SoundHover)
        self.failRetry.onClick(glob.AudioManager.play, sound=self.SoundClick)
        self.failRetry.onClick(glob.MenuManager.ChangeMenu, type=Menus.Playing)
        self.failRetry.onHoverLost(self.failRetry.ScaleTo, scale=0.7, duration=200)

        self.failRetry.enabled = False
        glob.foregroundSprites.add(self.failRetry)

        self.failQuit = pSprite("fail-back.png", vector2(0,260), SkinSource.user, Positions.centre, Positions.centre)
        self.failQuit.Fade(0)
        self.failQuit.Scale(0.7)

        self.failQuit.onHover(self.failQuit.ScaleTo, scale=0.75, duration=200)
        self.failQuit.onHover(glob.AudioManager.play, sound=self.SoundHover)
        self.failQuit.onClick(glob.AudioManager.play, sound=self.SoundClick)
        self.failQuit.onClick(glob.MenuManager.ChangeMenu, type=Menus.SongSelection)
        self.failQuit.onHoverLost(self.failQuit.ScaleTo, scale=0.7, duration=200)

        self.failQuit.enabled = False
        glob.foregroundSprites.add(self.failQuit)
        glob.foregroundSprites.add(self.Loading)


        self.UpperSprite = pSprite("hitObject.png", vector2(0,0), SkinSource.user, Positions.topCentre, Positions.centre, Color(102, 66, 245), Clocks.audio)
        self.UpperSprite.Scale(0.2)
        self.LowerSprite = pSprite("hitObject.png", vector2(0, 0), SkinSource.user, Positions.bottomCentre,
                                   Positions.centre, Color(245, 64, 64), Clocks.audio)
        self.LowerSprite.Scale(0.2)


        glob.Scheduler.AddNow(self.loadElements)







    def Fail(self):
        """To be called when the life drop at 0,
        it blocks key input"""
        #if for any reason it decides to fail if it's finished
        if self.finished:
            return
        self.failed = True
        glob.AudioManager.play(self.failSound)
        glob.AudioManager.Pause(False)
        for sprite in glob.foregroundSprites.sprites:
            sprite.ClearTransformations()
            sprite.FadeTo(0, 200)
        self.failQuit.enabled = True
        self.failRetry.enabled = True
        self.failOverlay.FadeTo(1,200)
        self.failRetry.FadeTo(1,200)
        self.failQuit.FadeTo(1,200)

    def loadElements(self):
        """loads the elements of the game, must be the last thing to do on init and on a separated thread to avoid freeze on big map loading"""
        if not self.isLoading:
            return #let's not try weird stuff
        workToDo = len(self.fileBody)
        workDone = 0
        for note in self.fileBody:
            note = note.split("|")
            # Fun fact about note loading, it was SO LONG before because it was actually re-rendering every sprite,
            # at start, i just though it was python slowness, but then i realised, game was taking like... 9 Go of Ram for a 3 min song
            # So i just modified this for it to take the pre-loaded sprite as base, so it will just contain 2 "really" loaded sprite in ram, the rest of the pSprite are just references, way more optimized
            if int(note[1]) == 1:
                self.upperSprites.append(pNote(int(note[0]), NotePos.Upper, self.ar, self.UpperSprite))
            else:
                self.lowerSprites.append(pNote(int(note[0]), NotePos.Lower, self.ar, self.LowerSprite))
            workDone += 1
            self.lifeBar.VectorScale(vector2(((workDone/workToDo)*100) * 19.2, 5))

        lastElement = max([max(sprite.time for sprite in self.upperSprites), max(sprite.time for sprite in self.lowerSprites)]) #Get the last element by getting the maximum values of those two list of elements
        self.ClosingTime = lastElement+ self.od*3

        self.Loading.ClearTransformations()
        self.Loading.FadeTo(0,200)
        glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=self.Loading)
        self.isLoading = False
        if self.upperSprites[0].time < 3000 or self.lowerSprites[0].time < 3000:
            glob.Scheduler.AddDelayed(3000, glob.AudioManager.Unpause, notif=False)
            NotificationMassive("Starting in 3", 1000, NotificationType.Error).show()
            glob.Scheduler.AddDelayed(1000, NotificationMassive("Starting in 2", 1000, NotificationType.Warning).show)
            glob.Scheduler.AddDelayed(2000, NotificationMassive("Starting in 1", 1000, NotificationType.Info).show)
            glob.Scheduler.AddDelayed(3000, NotificationMassive("Good Luck, Have Fun", 1000, NotificationType.Info).show)
        else:
            glob.AudioManager.Unpause()




    def Finish(self):
        """
        Calculating score, put it into game cache, and get to ranking panel
        Block Key input
        """
        # Check if for any reason it decide to complete even if its failed or if the music ends while the finish is already running
        if self.failed or self.finished:
            return

        #Blocking key imput
        self.finished = True


        glob.backgroundSprites.sprites[0].FadeTo(1, 400)
        for sprite in glob.foregroundSprites.sprites:
            sprite.ClearTransformations()
            sprite.FadeTo(0, 400)

        #Reviewing data and admitting them into vars for future caching
        self.accList.pop(0) #Dirty workaround of a bug that makes a miss after loading elements

        accuracy = round(sum(self.accList)/len(self.accList), 2)
        fullCombo = self.accList.count(0) == 0
        missCount = self.accList.count(0)
        mehCount = self.accList.count(33)
        goodCount = self.accList.count(66)
        perfectCount = self.accList.count(100)

        # Unstablerate is a list [[min, avg, max], entireData]
        unstableRate = [[min(self.unstableRate), round(sum(self.unstableRate)/len(self.unstableRate), 2), max(self.unstableRate)], self.unstableRate]

        #Rank Letters works on the percentage of Perfects and the presence of full combo

        if perfectCount/len(self.accList)*100 > 93:
            rankLetter = "S" if fullCombo else "A"
        elif perfectCount/len(self.accList)*100 > 86:
            rankLetter = "A" if fullCombo else "B"
        elif perfectCount/len(self.accList)*100 > 70:
            rankLetter = "B" if fullCombo else "C"
        else:
            rankLetter = "C" if fullCombo else "D"

        #Caching all stats to show it later on the next Menu

        data = {
            "accuracy" : accuracy,
            "combo" : self.maxCombo,
            "fullCombo" : fullCombo,
            "xmgpRatio" : [missCount, mehCount, goodCount, perfectCount], #Miss / Meh / Good / Perfect ratio
            "unstableRate" : unstableRate,
            "score" : self.score,
            "rank" : rankLetter,
            "mapOD" : self.od
        }
        glob.cache = data

        #get ID to put as PK
        id = int(glob.db.fetch("SELECT count(*) as count FROM scores")["count"])+1

        #get songID
        beatmapID = glob.AudioManager.currentSong["id"]
        diffStr = ["normal", "hard", "insane"][int(glob.Difficulty)]



        glob.db.execute(f"INSERT INTO scores (`id`, `username`, `mapid`, `difficulty`, `score`, `accuracy`, `consistency`, `comboMax`, `rank`, `countPerf`, `countGood`, `countMeh`, `countMiss`) VALUES ('{id}','user','{beatmapID}','{diffStr}','{self.score}','{accuracy}','{(unstableRate[0][1])}','{self.maxCombo}','{rankLetter}','{perfectCount}','{goodCount}','{mehCount}','{missCount}');")

        glob.Scheduler.AddDelayed(1000, glob.MenuManager.ChangeMenu, type=Menus.Ranking)




    def Key1(self, holding):
        """Called each frame to determine tiny visual stuff, and Call handleKey1 when needed"""
        if holding and not self.key1Holt:
            self.upperOv.ClearTransformations()
            self.upperOv.Fade(1)
            glob.AudioManager.play(self.touchSound)
            self.handleKey1()
            self.key1Holt = True
        if not holding and self.key1Holt:
            self.upperOv.FadeTo(0, 200)
            self.key1Holt = False




    def Key2(self, holding):
        """Called each frame to determine tiny visual stuff, and Call handleKey2 when needed"""
        if holding and not self.key2Holt:
            self.lowerOv.ClearTransformations()
            self.lowerOv.Fade(1)
            glob.AudioManager.play(self.touchSound)
            self.handleKey2()
            self.key2Holt = True
        if not holding and self.key2Holt:
            self.lowerOv.FadeTo(0, 200)
            self.key2Holt = False

    def handleKey1(self):
        """Called when circle must be hit.. or not"""
        if len(self.upperSprites) > 0:

            spriteToHandle = self.upperSprites[0]
            delay = spriteToHandle.time - pygame.mixer.music.get_pos()


            if delay < 0:
                late = True
            else:
                late = False

            if abs(delay) > int(self.od)*3:
                return
            self.unstableRate.append(delay)
            glob.AudioManager.play(self.hitSound)
            spriteToHandle.Hit()
            self.upperSprites.pop(0)
            self.combo += 1



            if abs(delay) < int(self.od):
                self.updateCombo(3)
                self.score += 300*self.combo
                self.accList.append(100)
                self.life += self.hp

            elif abs(delay) < int(self.od)*2:
                self.updateCombo(2)
                self.score += 100*self.combo
                self.accList.append(66)
                self.life += self.hp/2

            elif abs(delay) <= int(self.od)*3:
                self.updateCombo(1)
                self.score += 50*self.combo
                self.accList.append(33)
                self.life += self.hp/3

            self.updateScore()

    def handleKey2(self):
        """Called when circle must be hit.. or not"""
        if len(self.lowerSprites) > 0:

            spriteToHandle = self.lowerSprites[0]
            delay = spriteToHandle.time - pygame.mixer.music.get_pos()


            if delay < 0:
                late = True
            else:
                late = False

            if abs(delay) > int(self.od)*3:
                return

            self.unstableRate.append(delay)
            glob.AudioManager.play(self.hitSound)
            spriteToHandle.Hit()
            self.lowerSprites.pop(0)
            self.combo += 1

            if abs(delay) > int(self.od)*3:
                return
            if abs(delay) < int(self.od):
                self.updateCombo(3)
                self.score += 300 * self.combo
                self.accList.append(100)
                self.life += self.hp


            elif abs(delay) < int(self.od) * 2:
                self.updateCombo(2)
                self.score += 100 * self.combo
                self.accList.append(66)
                self.life += self.hp/2

            elif abs(delay) <= int(self.od) * 3:
                self.updateCombo(1)
                self.score += 50 * self.combo
                self.accList.append(33)
                self.life += self.hp/3

            self.updateScore()

    def updateCombo(self, hit):
        """Called when combo is actualised, and should be called ONLY when combo is updated, since it activate tiny animation"""
        self.comboIndicatorOv.ClearTransformations()
        self.comboIndicator.ClearTransformations()
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo
        fadeTime = 300

        hitColor = [Color(255,0,0), Color(255, 106, 0), Color(75, 235, 30), Color(48, 248, 255)][hit]
        self.comboIndicator.Text(str(self.combo) + "x")
        self.comboIndicator.Color(hitColor)
        self.comboIndicator.FadeColorTo(Color(255,255,255),500)

        self.comboIndicatorOv.Text(str(self.combo) + "x")
        self.comboIndicatorOv.Color(hitColor)
        self.comboIndicatorOv.FadeColorTo(Color(255,255,255),500)
        self.comboIndicatorOv.Scale(1.5)
        self.comboIndicatorOv.ScaleTo(1,fadeTime, EaseTypes.easeIn)
        self.comboIndicatorOv.Fade(0.7)
        self.comboIndicatorOv.FadeTo(0, fadeTime, EaseTypes.easeIn)


    def updateScore(self):
        """Simple shortcut to lightweight already heavy code"""
        self.ScoreIndicator.Text(str(self.score))


    def updateLife(self):
        """Simple shortcut to lightweight already heavy code"""
        if not self.finished and not self.isLoading and not pygame.mixer.music.get_pos() < 30 and not self.isPausing: #assuming there is no notes in the 30 first ms
            self.life -= self.hp/100
            self.life = min(self.life, 100)
            self.life = max(self.life, 0)
            self.lifeBar.VectorScale(vector2(self.life*19.2, 5))
            if self.life == 0 and not self.failed:
                self.Fail()

    @property
    def isPausing(self):
        try:
            return not (self.upperSprites[0].time - pygame.mixer.music.get_pos() < 3000 or self.lowerSprites[0].time - pygame.mixer.music.get_pos() < 3000)
        except:
            return False


    def update(self):
        currentWidth = (pygame.mixer.music.get_pos() / glob.AudioManager.currentSong["length"]) * glob.windowManager.widthScaled
        self.progressBar.VectorScale(vector2(currentWidth, 5))
        seconds = str(int((pygame.mixer.music.get_pos() / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0" + seconds
        minutes = str(int((pygame.mixer.music.get_pos() / 1000 / 60) % 60))
        self.LengthTime.Text("{}:{}".format(minutes, seconds))
        self.accBar.Fade(helper.getSyncValue(0.8,0.5, EaseTypes.easeOut))
        self.updateLife()
        #handle missed notes
        if len(self.upperSprites) > 0 and self.upperSprites[0].time - pygame.mixer.music.get_pos() < 0-self.od*3 and pygame.mixer.music.get_pos()>30: #Assuming there is no note in the first 30 miliseconds
            # Handle Missed Notes
            self.upperSprites[0].Miss()
            self.life -= self.hp
            self.upperSprites.pop(0)
            self.combo = 0
            self.updateCombo(0)
            self.accList.append(0)

        if len(self.lowerSprites) > 0 and self.lowerSprites[0].time - pygame.mixer.music.get_pos() < 0-self.od*3 and pygame.mixer.music.get_pos()>30: #Assuming there is no note in the first 30 miliseconds
            self.lowerSprites[0].Miss()
            self.life -= self.hp
            self.lowerSprites.pop(0)
            self.combo = 0
            self.updateCombo(0)
            self.accList.append(0)

        if pygame.mixer.music.get_pos() >= self.ClosingTime and self.ClosingTime != 0 and not self.finished and not self.isLoading: #Avoid finish if song hasn't started
            self.Finish()
        if self.isPausing and not self.paused:
            self.paused = True
            glob.Background.FadeTo(0.7, 400, EaseTypes.easeInOut)
        elif not self.isPausing and self.paused:
            self.paused = False
            glob.Background.FadeTo(0.1, 400, EaseTypes.easeInOut)


    def dispose(self):
        for sprite in glob.foregroundSprites.sprites:
            sprite.FadeTo(0, 400)


    def HandleEvents(self, events):
        keys = pygame.key.get_pressed()
        if not self.failed and not self.finished:
            if keys[K_d] or keys[K_f]:
                self.Key1(True)
            else:
                self.Key1(False)

            if keys[K_j] or keys[K_KP4]:
                self.Key2(True)
            else:
                self.Key2(False)

        if keys[K_ESCAPE] and not self.finished:
            glob.MenuManager.ChangeMenu(type=Menus.SongSelection)

        for event in events:

            if event.type == pygame.QUIT and not self.finished:
                glob.MenuManager.ChangeMenu(type=Menus.SongSelection)

