import configparser
from os import path
from framework import glob
from pygame.locals import *

class Config:
    def __init__(self):
        self.writer = configparser.ConfigParser()
        if path.exists(glob.currentDirectory + "/DeltaDashConf.ini"):
            self.writer.read(glob.currentDirectory + "/DeltaDashConf.ini")
            self.config = self.writer["Delta Dash Config"]
        else:
            self.writer["Delta Dash Config"] = {}
            self.config = self.writer["Delta Dash Config"]
            self.config["volume"] = "float://"+str(1)
            self.config["blue1"] = "int://"+str(K_d)
            self.config["blue2"] = "int://"+str(str(K_f))
            self.config["red1"] = "int://"+str(str(K_j))
            self.config["red2"] = "int://"+str(str(K_k))
            self.config["username"] = "str://"
            self.config["password"] = "str://"
            self.Save()

    def getValue(self, key:str):
        try:
            value = self.config[key]
            type, value = value.split("://")
            if type == "float":
                return float(value)
            if type == "int":
                return int(value)
            if type == "str":
                return str(value)
            else:
                return value
        except:
            glob.Logger.error("Tried to read unexisting value ({}) in DeltaDashConf.ini".format(key))
            return

    def setValue(self, key, value, type):
        if type == "float":
            ftype = float
        if type == "str":
            ftype = str
        if type == "int":
            ftype = int
        else:
            ftype = str
        self.config[key] = type + "://" + ftype(value)
        self.Save()


    def __getitem__(self, item):
        return self.getValue(item)

    def Save(self):
        with open(glob.currentDirectory + "/DeltaDashConf.ini", "w") as f:
            self.writer.write(f)