from win32gui import GetForegroundWindow
import psutil
import time
import win32process

# to get this to work on anything post Python 3.6, do pip install pywin32 and pip install psutil

process_time = {}
timestamp = {}
while True:
    current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe",
                                                                                                                 "")
    timestamp[current_app] = int(time.time())
    time.sleep(1)
    if current_app not in process_time.keys():
        process_time[current_app] = 0
    process_time[current_app] = process_time[current_app] + int(time.time()) - timestamp[current_app]
    print(process_time)
# https://dev.to/tkkhhaarree/track-windows-app-usage-time-using-python-h9h
