import globalVar

from wxGUI import wxGUI, wxApp

if __name__ == '__main__':
    app = wxApp()
    globalVar.init()
    globalVar.set_value("debug", False)
    gui = wxGUI()
    app.set_thread_killer(gui.stop_controller)
    app.MainLoop()
