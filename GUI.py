from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QLabel

from Control import Controller


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self._btn = QPushButton("Toggle", self)
        self._procStateText = QLabel("Unknown Status", self)
        self._autoDetectCB = QCheckBox("Auto detect", self)
        self._msg = QLabel("msg", self)
        self._controller = Controller(self.set_proc_state, self.msg)
        self.init_gui()

    def set_proc_state(self, state):
        pst = self._procStateText
        pst.setText(state)
        pst.adjustSize()

    def msg(self, message):
        msg = self._msg
        msg.setText(message)
        msg.adjustSize()

    def init_gui(self):
        self.resize(350, 100)
        self.move(300, 300)
        self.setWindowTitle("AutoPauseMC")
        self.setFixedSize(self.size())
        self.init_base_layout()
        self.show()

    def init_base_layout(self):
        btn = self._btn
        pst = self._procStateText
        chb = self._autoDetectCB
        msg = self._msg

        pst.adjustSize()
        btn.adjustSize()
        chb.adjustSize()
        msg.adjustSize()

        pst.move(200, 20)
        msg.move(200, 60)
        btn.move(15, 15)
        chb.move(15, 60)

        btn.clicked.connect(self.on_click)
        chb.toggled.connect(self.on_toggle)

    def closeEvent(self, QCloseEvent):
        self._controller.stop_threads()

    @pyqtSlot(name="btn onClick")
    def on_click(self):
        print("button pressed")
        self._controller.on_click()

    @pyqtSlot(name="chb onToggle")
    def on_toggle(self):
        print("checkBox toggled")
        print(self._autoDetectCB.isChecked())
