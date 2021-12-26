from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import matplotlib.pyplot as plt


def windowTracker():
    process_time = {}
    timestamp = {}
    x = 0
    while True:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(
            ".exe", "")
        timestamp[current_app] = int(time.time())
        time.sleep(1)
        if current_app not in process_time.keys():
            process_time[current_app] = 0
        process_time[current_app] = process_time[current_app] + int(time.time()) - timestamp[current_app]
        print(process_time)
        x += 1
        if (x == 10):  # TODO: change this to a button or a keyboard signal that stops the timer and returns your converted graph or even the timer ending at the end of the day (for now it's set at 10 seconds for testing purposes)
            return process_time


def plotTestData(x):
    labels, sizes = zip(*x.items())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title("Your App Usage")
    plt.show()


x = windowTracker()
plotTestData(x)
