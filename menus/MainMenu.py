from framework.graphics.pSprite import pSprite
from framework.graphics.pText import pText
from framework.gameplayElements.pButton import pButton
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
import pygame
from os import path
import  time

class MainMenu:
    def __init__(self):
        self.Playbutton = None
        self.exit = None
        self.background = None
        self.logoHero = None
        self.title = None
        self.introLogo = None
        self.introLogoBg = None
        self.clickButton = None
        self.upperBar = None
        self.lowerBar = None
        self.version = None
        self.NowPlaying = None
        self.idle = False
        self.SoundHover = glob.AudioManager.loadSound("button-hover.wav", SkinSource.local)
        self.SoundClick = glob.AudioManager.loadSound("button-select.wav", SkinSource.local)

        self.Transition = False
        self.disposeTime = 400

        self.SongName = None

        self.idleRightText = None
        self.idleLeftText = None
        self.idlePosBar = None
        self.idleDisc = None
        self.idleClickText = None
        pass

    def init(self):
        glob.Framerate = 30
        try:
            self.SongName = glob.AudioManager.currentSong["artist"] + " | "+glob.AudioManager.currentSong["name"]
        except:
            self.SongName = ""
        upperBar = pSprite(glob.PixelWhite,vector2(0,0), SkinSource.local, Positions.topCentre, Positions.topCentre, Color(50,50,50))
        upperBar.VectorScale(vector2(1920,50))
        self.upperBar = upperBar
        glob.foregroundSprites.add(upperBar)

        bottomBar = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.bottomCentre, Positions.bottomCentre, Color(50,50,50))
        bottomBar.VectorScale(vector2(1920,50))
        glob.foregroundSprites.add(bottomBar)
        self.lowerBar = bottomBar

        menuBg = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centreLeft, Positions.centre, Color(50,50,50,230))
        menuBg.Scale(1000)
        menuBg.VectorScale(vector2(3, 1.5))
        menuBg.Rotate(-69.7)
        self.background = menuBg
        glob.foregroundSprites.add(menuBg)


        version = pText("Delta Dash pre-alpha", 50,position=vector2(5,15), field=Positions.bottomLeft, origin=Positions.bottomLeft)
        glob.foregroundSprites.add(version)
        self.version = version


        button = pButton("Play", vector2(475,200),position=vector2(460,660), color=Color(110, 214, 69))
        self.Playbutton = button
        self.Playbutton.onHover(glob.AudioManager.play, sound=self.SoundHover)
        self.Playbutton.onClick(glob.MenuManager.ChangeMenu, type= Menus.SongSelection)
        self.Playbutton.onClick(glob.AudioManager.play, sound=self.SoundClick)
        glob.foregroundSprites.add(button)

        optbutton = pButton("Exit", vector2(550,200),position=vector2(500,870),  color=Color(209, 44, 44))
        self.exit = optbutton
        self.exit.onHover(glob.AudioManager.play, sound=self.SoundHover)
        self.exit.onClick(helper.GameQuit)
        glob.foregroundSprites.add(optbutton)



        LogoHero = pSprite("logo-hero.png", vector2(-500,0), SkinSource.user, Positions.centreRight, Positions.centre)
        self.logoHero = LogoHero
        glob.foregroundSprites.add(LogoHero)

        Title = pSprite("title.png", vector2(400,200), SkinSource.local, Positions.topLeft, Positions.centre)
        self.title = Title
        glob.foregroundSprites.add(Title)

        NowPlaying = pText(self.SongName, 40, position=vector2(50,-3), field=Positions.topRight, origin=Positions.topRight)
        self.NowPlaying = NowPlaying
        glob.foregroundSprites.add(NowPlaying)
        if glob.Starting:
            self.Transition = True
            Title.Fade(0)
            upperBar.Fade(0)
            bottomBar.Fade(0)
            menuBg.Fade(0)
            NowPlaying.Fade(0)


            button.Fade(0)
            button.position = vector2(-500,0)

            optbutton.Fade(0)
            optbutton.position = vector2(-500,0)

         

            version.Fade(0)

            LogoHero.Fade(0)
            LogoHero.position = vector2(500,0)

            glob.Background.Fade(0)

            IntroTitle = pSprite("menu-big-title.png", vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
            IntroTitle.Fade(0)
            IntroTitle.FadeTo(1, 800, EaseTypes.easeInOut)
            self.introLogo = IntroTitle

            ClickButton = pText("Click Anywhere to start", 100, FontStyle.heavy, vector2(0,200), Positions.centre, Positions.centre)
            ClickButton.Fade(0)
            self.clickButton = ClickButton
            IntroTitleBackground = pSprite("menu-big-title-bg.png", vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
            IntroTitleBackground.Fade(0)
            self.introLogoBg = IntroTitleBackground
            glob.Scheduler.AddDelayed(2426, IntroTitleBackground.FadeTo, value=1, duration=800, easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(4415, glob.Background.FadeTo, value=1, duration=800, easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(6234, IntroTitle.MoveTo,x=0, y=-50,  duration=2000,easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(6234, IntroTitleBackground.MoveTo,x=0, y=-50,  duration=2000,easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(6234, ClickButton.FadeTo, value=0.9, duration=2100,easing=EaseTypes.easeInOut, loop=True)
            glob.Scheduler.AddDelayed(7234, NowPlaying.FadeTo, value=1, duration=800,easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(8234, self.endTransformation)
            glob.foregroundSprites.add(IntroTitleBackground)
            glob.foregroundSprites.add(IntroTitle)
            glob.foregroundSprites.add(ClickButton)
        else:
            self.Transition = True
            for sprite in glob.foregroundSprites.sprites:
                sprite.Fade(0)
                sprite.FadeTo(1, 400)
            glob.AudioManager.ChangeBackground("/data/sprites/background.png", 400)
            glob.Scheduler.AddDelayed(400, self.endTransformation)


    def endTransformation(self):
        self.Transition = False

    def endStarting(self):
        glob.Starting = False
        self.Transition = False

    def Unlock(self):
        if not self.Transition:
            self.Transition = True

            self.introLogo.ScaleTo(1.2, 300, EaseTypes.easeOut)
            self.introLogoBg.ScaleTo(1.2, 300, EaseTypes.easeOut)
            self.introLogo.FadeTo(0, 300, EaseTypes.easeOut)
            self.introLogoBg.FadeTo(0, 300, EaseTypes.easeOut)

            self.clickButton.FadeTo(0,200,EaseTypes.easeOut)

            self.logoHero.posMultY = 1
            self.logoHero.posMult = 1
            self.logoHero.MoveTo(0,0,500, EaseTypes.easeInOut)
            self.logoHero.FadeTo(1,700, EaseTypes.easeInOut)
            self.upperBar.MoveTo(0,0,EaseTypes.easeInOut)
            self.upperBar.FadeTo(1, 500, EaseTypes.easeInOut)
            self.lowerBar.FadeTo(1, 500)
            self.lowerBar.MoveTo(0,0,500, EaseTypes.easeInOut)
            self.background.position = vector2(-500,0)
            self.background.MoveTo(0,0,800, EaseTypes.easeOut)
            self.background.FadeTo(1,800, EaseTypes.easeInOut)

            glob.Scheduler.AddDelayed(500, self.Playbutton.FadeTo, value=1, duration=500)

            glob.Scheduler.AddDelayed(700, self.exit.FadeTo, value=1, duration=500)

            glob.Scheduler.AddDelayed(800, self.title.FadeTo, value=1, duration=500)

            glob.Scheduler.AddDelayed(500, self.version.FadeTo, value=1, duration=300)
            glob.Scheduler.AddDelayed(800, self.endStarting)
            glob.Scheduler.AddDelayed(800, glob.foregroundSprites.remove, sprite=self.introLogo)
            glob.Scheduler.AddDelayed(800, glob.foregroundSprites.remove, sprite=self.introLogoBg)
            glob.Scheduler.AddDelayed(800, glob.foregroundSprites.remove, sprite=self.clickButton)


    def removeIdle(self):
        for sprite in glob.foregroundSprites.sprites:
            if sprite.tag in ["idleOverlaySprites", "idleBackgroundSprite"]:
                sprite.FadeTo(0,200)
                glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=sprite)
            else:
                sprite.FadeTo(1,200)
        self.idle = False
        glob.AudioManager.ChangeBackground("/data/sprites/background.png", 400)

    def setIdle(self):
        bgAlreadyPresent = False
        for sprite in glob.foregroundSprites.sprites:
            if sprite.tag not in ["idleOverlaySprites", "idleBackgroundSprite"]:
                sprite.FadeTo(0,1000)
            if sprite.tag == "idleOverlaySprites":
                sprite.FadeTo(0,200)
                glob.Scheduler.AddDelayed(200, glob.foregroundSprites.remove, sprite=sprite)
            if sprite.tag == "idleBackgroundSprite":
                bgAlreadyPresent = True
        if not bgAlreadyPresent:
            bgSprite = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre, Color(0,0,0))
            bgSprite.VectorScale(vector2(1000,500))
            bgSprite.Fade(0)
            bgSprite.FadeTo(0.6,500)
            bgSprite.tag = "idleBackgroundSprite"
            glob.foregroundSprites.add(bgSprite)


        if not path.exists(glob.AudioManager.currentSong["folder"]+"/thumb.png"):
            songLogo = pSprite("defaultThumb.png", vector2(-480,0), SkinSource.local, Positions.centre, Positions.centreLeft)
            songLogo.tag = "idleOverlaySprites"
            glob.foregroundSprites.add(songLogo)

            songLogo.Scale(460/songLogo.image.get_width()*glob.windowManager.getPixelSize())

        else:
            songLogo = pSprite(glob.AudioManager.currentSong["folder"]+"/thumb.png", vector2(-480,0), SkinSource.absolute, Positions.centre, Positions.centreLeft)
            songLogo.Fade(0)
            glob.Scheduler.AddDelayed(200, songLogo.FadeTo, value=1, duration=500)
            songLogo.tag = "idleOverlaySprites"
            songLogo.Scale(460/songLogo.image.get_width() * glob.windowManager.getPixelSize())


            songBg = pSprite(glob.PixelWhite, vector2(-490,0), SkinSource.local, Positions.centre, Positions.centreLeft)
            songBg.VectorScale(vector2(480,480))
            songBg.tag = "idleOverlaySprites"
            songBg.Fade(0)
            glob.Scheduler.AddDelayed(200, songBg.FadeTo, value=1, duration=500)
            glob.foregroundSprites.add(songBg)
            glob.foregroundSprites.add(songLogo)

        glob.AudioManager.ChangeBackground(glob.AudioManager.currentSong["folder"]+"/background.png", 500)
        npName = glob.AudioManager.currentSong["name"]
        if len(npName) > 18:
            npName = npName[:16] + "..."
        songTitle = pText(npName, 50, FontStyle.regular, vector2(5, -140), Positions.centre, Positions.topLeft)
        songTitle.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(songTitle)

        npArtist = glob.AudioManager.currentSong["artist"]
        if len(npArtist) > 18:
            npArtist = npArtist[:16] + "..."
        songArtist = pText(npArtist, 50, FontStyle.regular, vector2(5, -110), Positions.centre, Positions.topLeft)
        songArtist.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(songArtist)
        if not bgAlreadyPresent:
            positionBarBg = pSprite(glob.PixelWhite, vector2(5,240), SkinSource.local, Positions.centre, Positions.bottomLeft, color=Color(0,0,0,150))
            positionBarBg.VectorScale(vector2(485,10))
            positionBarBg.tag = "idleBackgroundSprite"

            glob.foregroundSprites.add(positionBarBg)

        self.idleDisc = pSprite("idleDisc.png", vector2(240, 40), SkinSource.local, Positions.centre, Positions.centre)
        self.idleDisc.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(self.idleDisc)

        self.positionBar = pSprite(glob.PixelWhite, vector2(5, 240), SkinSource.local, Positions.centre,
                                Positions.bottomLeft)
        self.positionBar.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(self.positionBar)
        seconds = str(int((glob.AudioManager.currentSong["length"] / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0"+seconds
        minutes = str(int((glob.AudioManager.currentSong["length"] / 1000 / 60) % 60))
        self.idleLeftText = pText("0", 20, FontStyle.regular, vector2(5, 130), Positions.centre, Positions.bottomLeft)
        self.idleRightText = pText(minutes+":"+seconds, 20, FontStyle.regular, vector2(275, 130), Positions.centre, Positions.bottomRight)
        self.idleLeftText.tag = "idleOverlaySprites"
        self.idleRightText.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(self.idleLeftText)
        glob.foregroundSprites.add(self.idleRightText)

        self.idleClickText = pText("Click anywhere to return to Delta Dash", 40, FontStyle.heavy, vector2(0, 150), Positions.centre, Positions.topCentre)
        self.idleClickText.tag = "idleOverlaySprites"
        glob.foregroundSprites.add(self.idleClickText)


    def update(self):
        if self.SongName != glob.AudioManager.currentSong["artist"] + " | "+glob.AudioManager.currentSong["name"]:
            self.NowPlaying.Text(glob.AudioManager.currentSong["artist"] + " | "+glob.AudioManager.currentSong["name"])
            self.SongName = glob.AudioManager.currentSong["artist"] + " | "+glob.AudioManager.currentSong["name"]
            if self.idle:
                self.setIdle()
                seconds = str(int((glob.AudioManager.currentSong["length"]/1000)%60))
                if len(seconds) == 1:
                    seconds = "0" + seconds
                minutes = str(int((glob.AudioManager.currentSong["length"]/1000/60)%60))
                self.idleRightText.Text(minutes+":"+seconds)


        if self.idle:
            currentWidth = (pygame.mixer.music.get_pos()/glob.AudioManager.currentSong["length"]) * 480
            seconds = str(int((pygame.mixer.music.get_pos() / 1000)%60))
            if len(seconds) == 1:
                seconds = "0" + seconds
            minutes = str(int((pygame.mixer.music.get_pos()/1000/60) % 60))
            self.idleLeftText.Text(minutes+":"+seconds)
            self.positionBar.VectorScale(vector2(currentWidth, 10))
            self.idleDisc.Scale(helper.getSyncValue(0.6, 0.55))
            if glob.AudioManager.BeatsSinceBegin() %2 == 0:
                self.idleDisc.Rotate(helper.getSyncValue(0, 180))
            else:
                self.idleDisc.Rotate(helper.getSyncValue(180, 360))

            self.idleClickText.Fade(helper.getSyncValue(1, 0.7, EaseTypes.easeInOut))
        if glob.Starting and not self.Transition:
            self.introLogoBg.Scale(helper.getSyncValue(1.01, 1, EaseTypes.easeOut))


        if not glob.Starting and not self.Transition and not self.idle:
            if time.time()*1000 - glob.LastActive > 30000 and not self.idle:
                self.idle = True
                self.setIdle()
            self.Playbutton.Position(helper.SetParalax(70))
            self.exit.Position(helper.SetParalax(70))
            self.logoHero.position = helper.SetParalax(40)
            self.logoHero.Scale(helper.getSyncValue(0.99, 1, EaseTypes.easeOut))
            self.title.position = helper.SetParalax(70)
            if glob.AudioManager.isPlaying:
                if glob.AudioManager.BeatsSinceBegin() % 2 == 0:
                    self.logoHero.Rotate(helper.getSyncValue(-3, 3, EaseTypes.easeInOut))
                    self.title.VectorScale(vector2(helper.getSyncValue(1.3, 1, EaseTypes.easeOut), 1))
                    self.title.Rotate(helper.getSyncValue(-5, 0, EaseTypes.easeOut))
                else:
                    self.logoHero.Rotate(helper.getSyncValue(3, -3, EaseTypes.easeInOut))
                    self.title.VectorScale(vector2(helper.getSyncValue(1.2, 1, EaseTypes.easeOut),
                                                   helper.getSyncValue(1.2, 1, EaseTypes.easeOut)))
            self.logoHero.Scale(self.logoHero.scale)
            self.logoHero.posMultY = 1
            self.logoHero.posMult = 1

    def dispose(self):
        self.Transition = True
        for sprite in glob.foregroundSprites.sprites:
            sprite.FadeTo(0,400)
        self.background.MoveTo(-1000,0,400)


    def HandleEvents(self, events):
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                helper.GameQuit()
            if event.type == pygame.KEYDOWN:
                if not self.Transition:
                    if event.key == K_F1:
                        glob.Logger.debug("F1 (prev) Not implemented")
                    if event.key == K_F2:
                        glob.AudioManager.Pause()
                    if event.key == K_F3:
                        glob.AudioManager.Unpause()
                    if event.key == K_F4:
                        if not keys[K_LCTRL]:
                            glob.AudioManager.Stop()
                    if event.key == K_F5:
                        glob.AudioManager.Skip()
            if event.type == glob.UserEvents["MUSIC_END"]:
                glob.AudioManager.OnMusicEnd()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1,2,3):
                    if glob.Starting:
                        self.Unlock()
                    if self.idle:
                        self.removeIdle()