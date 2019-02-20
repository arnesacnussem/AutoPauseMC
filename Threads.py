import threading

import Status, time
import psutil
from psutil import NoSuchProcess
from abc import ABCMeta, abstractmethod
from win32gui import GetForegroundWindow, GetWindowText

import globalVar
from Process import find_mc, Proc, find_mc_dwm


class ABCThread(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, *args, wait_time=0.5, **kwargs, ):
        super().__init__(*args, **kwargs)
        self._flag = threading.Event()
        self._flag.set()
        self._running = threading.Event()
        self._running.set()
        self.wait_time = wait_time

    @abstractmethod
    def loop(self): pass

    def prepare_job(self): pass

    def set_wait_time(self, t):
        self.wait_time = t

    def run(self):
        self.prepare_job()
        while self._running.isSet():
            self._flag.wait()
            self.loop()
            time.sleep(self.wait_time)

    def pause(self):
        self._flag.clear()

    def resume(self):
        self._flag.set()

    def stop(self):
        self._flag.set()
        self._running.clear()


class ProcMonitor(ABCThread):
    mcProc = Proc(-1, -1, None)
    status = Status.stop
    oldStatus = status

    def __init__(self, on_status_changed_call, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifyStatusChanged = on_status_changed_call

    def loop(self):
        if self.status == Status.stop:
            self.set_wait_time(0.5)
            self.mcProc = find_mc()
            if self.mcProc.pid != -1:
                if self.proc_running():
                    self.notifyStatusChanged()
        else:
            self.set_wait_time(2)
            if not find_mc(monitor_mod=True, mc_proc=self.mcProc):
                self.mcProc = find_mc()
            if self.proc_running():
                if self.oldStatus != self.status:
                    self.oldStatus = self.status
                    self.notifyStatusChanged()
        # if globalVar.get_value("debug", False):
        #     print("[DEBUG]: " + str(self.mcProc))

    def prepare_job(self):
        self.notifyStatusChanged()

    def proc_running(self):
        try:
            pid = self.mcProc.pid
            if pid == -1:
                Exception(NoSuchProcess)
            p = psutil.Process(pid)
            if globalVar.get_value("debug", False):
                print("[DEBUG]proc_running: p.status() = " + p.status())
            if p.status() is 'stopped':
                self.status = Status.suspend
            if p.status() is 'running':
                self.status = Status.running
            return True
        except NoSuchProcess or ValueError:
            self.status = Status.stop
            self.notifyStatusChanged()
            return False


class FocusMonitor(ABCThread):

    def __init__(self, on_focus, on_focus_loss, bridge):
        super().__init__()
        self._enabled = False
        self._hwnd = -1
        self._status = Status.stop
        self._foreground = MonitoredVar(GetForegroundWindow())
        self._dwm = find_mc_dwm()
        self.send_pause = on_focus_loss
        self.send_resume = on_focus
        self._bridge = bridge

    def pause(self):
        self.set_enabled(False)
        super().pause()

    def resume(self):
        self.set_enabled(True)
        super().resume()

    def set_pid(self, pid):
        self._hwnd = pid
        if self._hwnd == -1:
            self.set_enabled(False)

    def set_enabled(self, enabled):
        self._enabled = enabled

    def loop(self):
        # print("Focus monitor thread loop")
        self._hwnd, self._status = self._bridge()
        if not self._enabled or self._status is Status.stop:
            self.set_wait_time(1.5)
            return
        if not globalVar.get_value("debug", False):
            print("[DEBUG]FocusMonitor->loop: _hwnd = %s | _status = %s | Foreground = %s" % (
                self._hwnd, self._status, GetForegroundWindow()))
        if self._foreground.set(GetForegroundWindow()):
            self.set_wait_time(0.5)
            print(find_mc_dwm())
            print(GetWindowText(self._foreground.get()))
            if Status.suspend and ("minecraft".upper() in str(GetWindowText(self._foreground.get())).upper()):
                print("resume!!!!!!!!")
                self.send_resume()
                time.sleep(1)
            else:
                if self._status is Status.running:
                    print("suspend!!!!!!!!!")
                    self.send_pause()
                    time.sleep(1)


class MonitoredVar:
    def __init__(self, default=None, callback=None):
        super().__init__()
        self._value = default
        self._callback = callback

    # if changed ,return true
    def set(self, val):
        if self._value != val:
            old = self._value
            self._value = val
            # before return,call back with old value and new value
            if self._callback is not None:
                self._callback(old, val)
            if globalVar.get_value("debug", False):
                print("[DEBUG]MonitoredVar->set: %s => %s" % (old, val))
            return True
        return False

    def get(self):
        return self._value
