import  time
from threading import  Thread
from framework.data.ErrorHandler import raiseError
class Scheduler:
    def __init__(self):
        self.threads = []

    def AddNow(self, function, **kwargs):
        self.AddDelayed(0, function, **kwargs)

    def AddDelayed(self, wait, function, **kwargs):
        Thread(target=lambda :self.__DelayedAsync__(wait, function,  **kwargs)).start()

    def __DelayedAsync__(self, wait, function, **kwargs):
        try:
            time.sleep(wait/1000)
            function(**kwargs)
        except Exception as e:
            raiseError(e)
