import matplotlib
import random
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from win32gui import GetForegroundWindow
import win32process
import psutil
import time
import matplotlib.pyplot as plt
from qt_material import apply_stylesheet
import sys

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        labels, sizes = self.windowTracker()
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(labels, sizes)
        self.setCentralWidget(sc)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        if e.key() == QtCore.Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def windowTracker(self):
        process_time = {}
        timestamp = {}
        x = 0
        while True:  # TODO: add blacklist of apps that shouldn't be tracked, like Explorer, Search, etc.
            current_app = psutil.Process(
                win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(
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
                return labels, sizes


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
