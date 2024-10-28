import platform
import subprocess
import os
import threading
import shutil

python_path = shutil.which('python3') or shutil.which('python')
npm_path = shutil.which('npm')

# Make changes here as needed depending on if your machine is being annoying
frontStart = [npm_path, 'run', 'dev']
backendStart = [python_path, '-m', 'flask', 'run', '--debug']
print(frontStart)
print(backendStart)
# Might need to change this to python3 for you windows people
backendStartWindows = [python_path, '-m', 'flask', 'run', '--debug']

def start_front():
    os.chdir('INFILTR8/')
    subprocess.run(frontStart)
    # proc1 = subprocess.Popen(
        
    # )

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