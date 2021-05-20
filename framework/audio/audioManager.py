import math
from framework import  glob
import os, random, json
from mutagen.mp3 import MP3
import time
from menus.overlays.pNotification import NotificationMassive
from framework.graphics.pSprite import pSprite
from framework.data.data import *
from os import path
import pygame

last = 0
class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.isPlaying = False
        self.currentSong = {}
        MUSIC_END = pygame.USEREVENT + 1
        glob.UserEvents["MUSIC_END"] = MUSIC_END
        pygame.mixer.music.set_endevent(glob.UserEvents["MUSIC_END"])
        self.alreadyPlayed={}
        #self.debugVisualizer = pSprite(glob.PixelWhite,vector2(0,0), SkinSource.local, Positions.bottomCentre, Positions.bottomCentre, Color(255,0,0))
        #self.debugVisualizer.VectorScale(vector2(1920,5))
        #glob.overlaySprites.add(self.debugVisualizer)

    def BeatCount(self):
        beatLength = self.BeatLength()
        return math.ceil(self.currentSong["length"]/beatLength)

    def BeatsSinceBegin(self):
        BeatLength = self.BeatLength()
        return math.ceil(pygame.mixer.music.get_pos()/BeatLength)

    def Restart(self):
        songFolder = self.currentSong["folder"]
        pygame.mixer.music.stop()
        pygame.mixer.music.load(songFolder+"/audio.mp3")
        pygame.mixer.music.set_volume(glob.volume)
        pygame.mixer.music.play(0)
        self.isPlaying = True


    def PlayMusic(self, songFolder, Preview=False):
        songFolder = glob.currentDirectory + songFolder

        pygame.mixer.music.load(songFolder+"/audio.mp3")

        song = MP3(songFolder+"/audio.mp3")
        pygame.mixer.music.set_volume(glob.volume)

        f = open(songFolder+"/metadata.json").read()
        self.currentSong = json.loads(f)
        self.currentSong["folder"] = songFolder
        self.currentSong["filename"] = songFolder + "/audio.mp3"
        self.currentSong["length"] = int(song.info.length*1000)
        if not Preview:
            pygame.mixer.music.play(0)
        else:
            pygame.mixer.music.play(0, self.currentSong["previewpoint"]/100)
        self.isPlaying = True

    def SeekPreview(self):
        pygame.mixer.music.play(start=self.currentSong["previewpoint"]/1000)



    def loadSound(self, filename, skinSource):
        if skinSource == SkinSource.user and path.exists(glob.currentDirectory + "/.user/skins/"+glob.currentSkin+"/"+filename):
            source = glob.currentDirectory + "/.user/skins/"+glob.currentSkin+"/"+filename
        else:
            source = glob.currentDirectory + "/data/sounds/"+filename
        return pygame.mixer.Sound(source)

    def play(self, sound):
        sound.set_volume(glob.volume)
        sound.play()

    def setVolume(self, x):
        x = round(x,2)
        glob.volume = x
        glob.Config.setValue("volume", x, "float")
        pygame.mixer.music.set_volume(x)

    def OnMusicEnd(self):
        global last
        if time.time()*1000-last < 300:
            return
        else:
            last = time.time()*1000
        forceStop = True
        if self.isPlaying == True:
            forceStop = False
        if forceStop:
            self.isPlaying = False
        else:
            songs = os.listdir(glob.currentDirectory + "/.user/maps")

            if len(songs) == 0:
                self.isPlaying = False
                pygame.mixer.music.set_pos(0)
            else:

                if len(self.alreadyPlayed.values()) == len(songs):
                    FirstTime = sorted(self.alreadyPlayed.keys())[0]
                    song = self.alreadyPlayed[FirstTime]
                    self.alreadyPlayed.pop(FirstTime)
                    self.alreadyPlayed[time.time()] = song
                else:
                    found = False
                    while not found:
                        song = random.choice(songs)
                        if song not in self.alreadyPlayed.values():
                            found = True
                            self.alreadyPlayed[time.time()] = song

                self.PlayMusic("/.user/maps/"+song)

    def ChangeBackground(self, Filename, duration=500):
        if not path.exists(Filename):
            Filename = glob.currentDirectory + "/data/sprites/background.png"
        new = pSprite(Filename, vector2(0, 0), SkinSource.absolute, Positions.centre, Positions.centre)
        backgroundScale = glob.windowManager.width / new.image.get_width()
        new.Scale(backgroundScale * 1.3)
        new.Fade(0)
        glob.backgroundSprites.add(new)
        new.FadeTo(1, duration)
        glob.Scheduler.AddDelayed(duration, glob.backgroundSprites.remove, sprite=glob.Background)
        glob.Background = new

    def Stop(self, notif=True):
        if notif:
            NotificationMassive("Stop", 800).show()
        self.isPlaying = False
        pygame.mixer.music.stop()

    def Pause(self, notif=True):
        if notif:
            NotificationMassive("|| Pause", 800).show()
        self.isPlaying = False
        pygame.mixer.music.pause()

    def Unpause(self, notif=True):
        if notif:
            NotificationMassive("> Play", 800).show()
        self.isPlaying = True
        pygame.mixer.music.unpause()

    def Skip(self, notif=True):
        if notif:
            NotificationMassive(">> Skip", 800).show()
        self.isPlaying = False
        pygame.mixer.music.stop()
        self.isPlaying = True
        self.OnMusicEnd()

    def IsNewBeat(self):
        if self.currentSong == {} or not self.isPlaying:
            return False
        bpm = self.currentSong["bpm"]
        offset = self.currentSong["offset"]
        beatLength = 60000/bpm
        if int(((pygame.mixer.music.get_pos()-offset) % beatLength)) == 0:
            return True
        else:
            return  False

    def BeatLength(self):
        if self.currentSong == {} or not self.isPlaying:
            return 1000
        else:
            return 60000/self.currentSong["bpm"]


    def Update(self):
        #self.debugVisualizer.VectorScale(vector2(helper.getSyncValue(1920, 0), 5))
        #self.debugVisualizer.Fade(helper.getSyncValue(1,0))
        pass


    def GetRelativePos(self):
        if self.currentSong == {} or not self.isPlaying:
            return int(time.time()*1000) % 1000
        bpm = self.currentSong["bpm"]
        offset = self.currentSong["offset"]
        beatLength = 60000 / bpm
        return int(((pygame.mixer.music.get_pos()-offset) % beatLength))/beatLength