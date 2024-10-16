import platform
import subprocess
import os
import threading

# Make changes here as needed depending on if your machine is being annoying
frontStart = ['npm', 'run', 'dev']
backendStart = ['flask', 'run', '--debug']
# Might need to change this to python3 for you windows people
backendStartWindows = ['python','flask', 'run', '--debug']

def start_front():
    os.chdir('INFILTR8/')
    subprocess.run(frontStart)

def start_back():
    os.chdir('backend/')
    if platform.system() == 'Windows':
        subprocess.run(backendStartWindows)
    else:
        subprocess.run(backendStart)

frontThread = threading.Thread(target=start_front)
backThraed = threading.Thread(target=start_back)

frontThread.start()
backThraed.start()