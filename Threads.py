import threading
import Status
import psutil
from psutil import NoSuchProcess
from abc import ABCMeta, abstractmethod

import globalVar
from Process import find_mc, Proc


class ABCThread(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._flag = threading.Event()
        self._flag.set()
        self._running = threading.Event()
        self._running.set()

    @abstractmethod
    def loop(self): pass

    def prepare_job(self): pass

    def run(self):
        self.prepare_job()
        while self._running.isSet():
            self._flag.wait()
            self.loop()

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

        if self.status is Status.stop:
            self.mcProc = find_mc()
            if self.mcProc.pid != -1:
                p = psutil.Process(self.mcProc.pid)
                if self.proc_running(p):
                    self.notifyStatusChanged()
        else:
            p = psutil.Process(self.mcProc.pid)
            if self.proc_running(p):
                if self.oldStatus is not self.status:
                    self.notifyStatusChanged()
        if globalVar.get_value("debug", False):
            print(self.mcProc)

    def prepare_job(self):
        self.notifyStatusChanged()

    def proc_running(self, p):
        try:
            if p.status() is 'stopped':
                self.status = Status.suspend
            if p.status() is 'running':
                self.status = Status.running
            return True
        except NoSuchProcess:
            self.status = Status.stop
            return False
