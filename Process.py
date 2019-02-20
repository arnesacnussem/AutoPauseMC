import psutil
import globalVar
from win32gui import *
from win32process import *

found = False
mc_process = None
dmw = None


class Proc:
    def __init__(self, hwnd, pid, name):
        self.hwnd = hwnd
        self.pid = pid
        self.name = name
        if pid != -1:
            self.process = psutil.Process(pid)
        else:
            self.process = None

    def suspend(self):
        if self.process is not None:
            self.process.suspend()

    def resume(self):
        if self.process is not None:
            self.process.resume()

    def __str__(self) -> str:
        return "hwnd = %s | pid = %s | name = %s" % (self.hwnd, self.pid, self.name)


def find_mc(monitor_mod=False, mc_proc=Proc(-1, -1, None)):
    debug = globalVar.get_value("debug", False)
    global found, mc_process
    found = False
    mc_process = Proc(-1, -1, None)

    def check_is_mc(hwnd, pid):
        try:
            name = psutil.Process(pid).name()
            title = GetWindowText(hwnd)
            if "minecraft".upper() in title.upper():
                if debug:
                    print("[DEBUG]find_mc->check_is_mc: hwnd = %s | pid = %s | name = %s | title = %s" % (hwnd, pid, name, title))
                if "java" in name:
                    global found, mc_process
                    mc_process = Proc(hwnd, pid, name)
                    found = True
                    return True
                else:
                    return False
        finally:
            return False

    def get_pid(hwnd, ignored):
        if not found and IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            _hwnd, _pid = GetWindowThreadProcessId(hwnd)
            if check_is_mc(hwnd, _pid):
                if debug:
                    print("[DEBUG]find_mc->get_pid: _hwnd = %s | hwnd = %s | _pid = %s" % (_hwnd, hwnd, _pid))

    if monitor_mod and mc_proc.pid != -1:
        if check_is_mc(mc_proc.hwnd, mc_proc.pid):
            return True
        return False
    EnumWindows(get_pid, 0)
    return mc_process


def find_mc_dwm():
    debug = globalVar.get_value("debug", False)

    def get_pid(hwnd, ignored):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            pid = GetWindowThreadProcessId(hwnd)[1]
            if "dwm" in psutil.Process(pid).name() and "minecraft".upper() in str(GetWindowText(hwnd)).upper():
                if not debug:
                    print("[DEBUG]find_mc_dwm(): pid = %s | hwnd = %s" % (pid, hwnd))
                global dmw
                dmw = hwnd

    EnumWindows(get_pid, 0)
    global dmw
    return dmw
