from menus.overlays.pNotification import Notification
from framework.data.data import *
from framework import glob
from datetime import datetime
from time import time
import platform
import os

class log:
    def __init__(self):

        if not os.path.exists('logs'):
            os.makedirs('logs')
        with open("logs/runtime.log", "w") as f:
            f.write(("-" * 50)+ "\nRunning Delta Dash {}\n".format(glob.Version))
            uname = platform.uname()
            f.write(f"Running on {uname.system} {uname.release} ({uname.version})"+"\n")
            f.write(f"Computer {uname.node} {uname.machine} with {uname.processor}"+"\n")
            f.write(("-" * 50)+"\n")
            if not os.path.exists('.user'):
                f.write("Creating .user folder")
                os.makedirs('.user')
                f.write("Creating .user/maps folder")
                os.makedirs('.user/maps')
                f.write("Creating .user/skins folder")
                os.makedirs('.user/skins')
                f.write("Creating .user/skins/user folder")
                os.makedirs('.user/skins/user')


    def debug(self, text):
        if glob.Debug:
            Notification(str(text), 5000, Color(206, 10, 255)).show()
            with open(glob.currentDirectory+"/logs/runtime.log", "a") as f:
                f.write("\n[{}][DEBUG] : {}".format(datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'),text))


    def write(self, text):
        if glob.Debug:
            Notification(text, 5000, Color(255, 255, 255)).show()
        with open(glob.currentDirectory+"/logs/runtime.log", "a") as f:
            f.write("\n[{}][Log] : {}".format(datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'),text))

    def error(self, text):
        Notification(text, 5000).show()
        with open(glob.currentDirectory+"/logs/runtime.log", "a") as f:
            f.write("\n[{}][Error] : {}".format(datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'),text))

    def info(self, text):
        Notification(text, 5000, Color(0, 255, 64)).show()
        with open(glob.currentDirectory+"/logs/runtime.log", "a") as f:
            f.write("\n[{}][Info] : {}".format(datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'),text))