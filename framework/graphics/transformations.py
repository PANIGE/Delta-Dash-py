from framework.data.data import *
class Transformation:
    def __init__(self, type, thread, object):
        self.type = type
        self.thread = thread
        self.object = object

    def start(self):
        self.thread.start()

    def stop(self, all=False):
        print("request stop")
        if all:
            self.object.AwaitStop = TransformationType.all
        else:
            self.object.AwaitStop = self.type