import Status
import globalVar
from Threads import ProcMonitor


class Controller:

    def __init__(self, GUI_set_status, GUI_msg):
        self.status = globalVar.set_value("status", Status.stop)
        self._proc = None
        self._proc_mon = ProcMonitor(self.on_status_changed)
        self._focus_mon = None
        self.GUI_set_status = GUI_set_status
        self.GUI_msg = GUI_msg
        self.launch_threads()

    def on_status_changed(self):
        self.GUI_set_status(self._proc_mon.status)
        pass

    def send_msg(self, msg):
        pass

    def on_click(self):
        print("msg from control " + str(self.status))

    def launch_threads(self):
        self._proc_mon.start()

    def stop_threads(self):
        self._proc_mon.stop()
