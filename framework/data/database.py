import sqlite3 as sl
from os import path
from framework import glob

class Db:
    """Databse is the main way to save scores and some data that don't have to be editable from external sources"""
    def __init__(self):
        if path.exists(glob.currentDirectory+"/scores.db"):
            needinit = False
        else:
            needinit = True

        self.con = sl.connect(glob.currentDirectory+"/scores.db", check_same_thread=False)
        self.con.row_factory = sl.Row
        self.cursor = self.con.cursor()

        if needinit:
            self.con.execute("""
                CREATE TABLE `scores` (
                  `id` INT NOT NULL,
                  `username` VARCHAR(45) NOT NULL,
                  `mapid` INT NOT NULL,
                  `difficulty` VARCHAR(45) NOT NULL,
                  `score` BIGINT NOT NULL,
                  `accuracy` FLOAT NOT NULL,
                  `consistency` FLOAT NOT NULL,
                  `comboMax` INT NOT NULL,
                  `rank` CHAR(1) NOT NULL,
                  `countPerf`INT NOT NULL,
                  `countGood` INT NOT NULL,
                  `countMeh` INT NOT NULL,
                  `countMiss` INT NOT NULL,
                  PRIMARY KEY (`id`));
                """)

    def fetch(self, sql):
        glob.Logger.debug(sql)
        self.cursor.execute(sql)
        r = self.cursor.fetchone()
        if r is None:
            return None
        return dict(r)

    def fetchAll(self, sql):
        glob.Logger.debug(sql)
        self.cursor.execute(sql)
        r = self.cursor.fetchall()
        if r is None:
            return None
        return [dict(x) for x in r]

    def execute(self, sql):
        glob.Logger.debug(sql)
        self.cursor.execute(sql)
        self.con.commit()
