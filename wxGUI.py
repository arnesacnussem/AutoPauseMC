import globalVar
from Control import Controller
import wx

_style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX ^ wx.SYSTEM_MENU


class wxGUI(wx.Frame):
    def __init__(self):
        super().__init__(None, style=_style)
        self.SetTitle("AutoPauseMC")
        self.SetSize(300, 110)
        self.SetPosition((300, 300))
        self._button = wx.Button(self, label="Toggle", pos=(7, 7), size=(80, 30))
        self._checkBox = wx.CheckBox(self, label="AutoDetect", pos=(7, 44), size=(80, 30))
        self._status = wx.StaticText(self, pos=(110, 14), size=(240, 10))
        self._msg = wx.StaticText(self, pos=(110, 44), size=(240, 10))
        self._controller = Controller(GUI_msg=self.msg, GUI_set_status=self.set_status)
        self.init()
        self.Show()

    def msg(self, msg):
        self._msg.SetLabelText(msg)

    def set_status(self, status):
        self._status.SetLabelText(status)

    def init(self):
        self._button.Bind(wx.EVT_BUTTON, self.on_click)
        self._checkBox.Bind(wx.EVT_CHECKBOX, self.on_cb_toggle)
        self.set_status("Unknown status.")
        self.msg("Waiting...")

    def on_click(self, evt):
        if globalVar.get_value("debug", False):
            print("[DEBUG]wxGUI=>on_click: Button clicked: " + str(evt))
        self._controller.on_click()

    def on_cb_toggle(self, evt):
        if globalVar.get_value("debug", False):
            print("[DEBUG]wxGUI=>on_cb_toggle: CB Toggled: %s,%s" % (str(self._checkBox.IsChecked()), str(evt)))
        self._controller.on_cb_toggled(self._checkBox.IsChecked())

    def stop_controller(self):
        self._controller.stop_threads()


class wxApp(wx.App):
    thread_killer = None

    def set_thread_killer(self, thread_killer):
        self.thread_killer = thread_killer

    def OnExit(self):
        super().OnExit()
        if globalVar.get_value("debug", False):
            print("[DEBUG]wxApp=>OnExit: OnExit called!")
        self.thread_killer()
        return 0
