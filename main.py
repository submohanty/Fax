from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from win32gui import GetForegroundWindow
import win32process
import psutil
import time
import matplotlib.pyplot as plt
from qt_material import apply_stylesheet
import sys


def windowTracker():
    process_time = {}
    timestamp = {}
    x = 0
    while True: # TODO: add blacklist of apps that shouldn't be tracked, like Explorer, Search, etc.
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(
            ".exe", "")
        timestamp[current_app] = int(time.time())
        time.sleep(1)
        if current_app not in process_time.keys():
            process_time[current_app] = 0
        process_time[current_app] = process_time[current_app] + int(time.time()) - timestamp[current_app]
        print(process_time)
        x += 1
        if (x == 5):
            labels, sizes = zip(*process_time.items())
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')
            plt.title("Your App Usage")
            plt.show()
            return


def plotTestData(x):
    labels, sizes = zip(*x.items())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title("Your App Usage")
    plt.show()


def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape:
        self.close()
    if e.key() == QtCore.Qt.Key_F11:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()



def gui():
    extra = {
        'font_family': 'Roboto',
        'font_size': 22,
        'density_scale': '-1'
    }

    app = QApplication(sys.argv)
    win = QMainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml', extra=extra)
    win.setWindowTitle("Fax")

    #
    label = QLabel(win)
    label.setText("Press this button in order to start the screen time tracking")
    # label.setFont(QFont("Consolas", 48)) # this doesn't work with qt material
    label.move(700, 200)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)
    label.adjustSize()

    # Button
    button = QtWidgets.QPushButton(win)
    button.setText("Begin")
    button.setGeometry(0, 0, 100, 100)
    button.move(885, 400)
    button.clicked.connect(windowTracker)
    #
    button1 = QtWidgets.QPushButton(win)
    button1.setText("End")
    button1.setGeometry(0, 0, 100, 100)
    button1.move(885, 600)
    button1.clicked.connect(win.close)

    # TODO: Add a way for the user to collapse the window into the tray

    win.showMaximized()
    sys.exit(app.exec_())


gui()  # TODO: wrap this all into a class

# TODO: Add a SQL database to store the images of Matplotlib over time so that the user can see their trends over time