from pyupbit import WebSocketManager
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import time


class Worker(QThread):
    recv = pyqtSignal(str)
    def run(self):
        # create websocket for Bithumb
        wm = WebSocketManager("ticker", ["KRW-BTC"])
        while True:
            data = wm.get()
            self.recv.emit(data['content']['closePrice'])


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel("BTC", self)
        label.move(20, 20)

        self.price = QLabel("-", self)
        self.price.move(80, 20)
        self.price.resize(60, 20)

        button = QPushButton("Run", self)
        button.move(20, 50)
        button.clicked.connect(self.click_btn)

        self.th = Worker()
        self.th.recv.connect(self.receive_msg)

    @pyqtSlot(str)
    def receive_msg(self, msg):
        print(msg)
        self.price.setText(msg)

    def click_btn(self):
       self.th.start()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   app.exec_()