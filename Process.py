import psutil
import globalVar
from win32gui import *
from win32process import *

found = False
mc_process = None


class Proc:
    def __init__(self, hwnd, pid, name):
        self.hwnd = hwnd
        self.pid = pid
        self.name = name
        if pid != -1:
            self.process = psutil.Process(pid)

    def suspend(self):
        self.process.suspend()

    def resume(self):
        self.process.resume()

    def __str__(self) -> str:
        return "hwnd = %s | pid = %s | name = %s" % (self.hwnd, self.pid, self.name)


def find_mc():
    debug = globalVar.get_value("debug", False)
    global found, mc_process
    found = False
    mc_process = Proc(-1, -1, None)

    def check_is_mc(hwnd, pid):
        name = psutil.Process(pid).name()
        title = GetWindowText(hwnd)
        if "minecraft".upper() in title.upper():
            print("Gotcha one,checking if it's minecraft: %s, %s" % (title, name))
            if debug:
                print("[DEBUG]: pid = %s | name = %s | title = %s" % (pid, name, title))
            if "java" in name:
                print("I've got you")
                global found, mc_process
                mc_process = Proc(hwnd, pid, name)
                found = True
                return True
            else:
                print("No,it's doesn't")
                return False

    def get_pid(hwnd, ignored):
        if not found and IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            _hwnd, _pid = GetWindowThreadProcessId(hwnd)
            if check_is_mc(hwnd, _pid):
                if debug:
                    print("[DEBUG]: _hwnd = %s | hwnd = %s | _pid = %s" % (_hwnd, hwnd, _pid))

    EnumWindows(get_pid, 0)
    return mc_process
