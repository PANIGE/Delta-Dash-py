from menus.overlays.pNotification import Notification
import traceback

def raiseError(Exception:Exception):
    Notification("Unhandled Error [ {} ]".format(Exception), 5000).show()
    with open("logs/runtime.log", "a+") as f:
        f.write("\n[ERROR] UNHANDLED !!! | {} \n{}".format(Exception, traceback.format_exc()))