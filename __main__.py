import globalVar
import sys
from PyQt5.QtWidgets import QApplication
from GUI import GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    globalVar.init()
    globalVar.set_value("debug", True)
    gui = GUI()
    sys.exit(app.exec_())
