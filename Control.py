import Status
import globalVar
from Threads import ProcMonitor, FocusMonitor


class Controller:
    def __init__(self, GUI_set_status, GUI_msg):
        self.status = globalVar.set_value("status", Status.stop)
        self.GUI_set_status = GUI_set_status
        self.GUI_msg = GUI_msg
        self.hwnd = None
        self._proc_mon = ProcMonitor(self.on_status_changed)
        self._focus_mon = FocusMonitor(self.on_focus, self.on_focus_loss, self.bridge)
        self.launch_threads()

    def on_status_changed(self):
        self.GUI_set_status(self._proc_mon.status)
        self.status = self._proc_mon.status
        self.hwnd = self._proc_mon.mcProc.hwnd
        if globalVar.get_value("debug", False):
            print("[DEBUG]on_status_changed: => self.status = " + self.status)

    def bridge(self):
        return self.hwnd, self.status

    def send_msg(self, msg):
        self.GUI_msg(msg)

    def on_focus(self):
        self.send_msg("Focused")
        self._proc_mon.mcProc.resume()
        self.on_status_changed()
        self.send_msg("resumed")

    def on_focus_loss(self):
        self.send_msg("Focus loss")
        self._proc_mon.mcProc.suspend()
        self.on_status_changed()
        self.send_msg("paused")

    def on_click(self):
        if self.status is Status.suspend:
            self.send_msg("Resuming")
            self._proc_mon.mcProc.resume()
            return
        if self.status is Status.running:
            self.send_msg("Pausing")
            self._proc_mon.mcProc.suspend()
            return
        else:
            self.send_msg("do nothing...")

    def on_cb_toggled(self, cb_checked):
        if cb_checked:
            self._focus_mon.resume()
        else:
            self._focus_mon.pause()
        pass

    def launch_threads(self):
        self._proc_mon.start()
        self._focus_mon.pause()
        self._focus_mon.start()

    def stop_threads(self):
        self._proc_mon.stop()
        self._focus_mon.stop()
