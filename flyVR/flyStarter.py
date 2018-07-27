import os
import threading
import time
import subprocess

running = True
runDisplay = "flyvr-run-display-server"

runStimuli = "/home/flyvr/flyvr/fly-matrix/flyVR/flyvr.py"

runTracker = "python /home/flyvr/flyvr/scripts/flyvr-tethered-orientation-tracker.py --config-raw \"{capture: {configuration: {ExposureTime: 9000, ExposureAuto: 'Off'}}}\" pylon:"


def displayServer():
    print('starting display')
    p=subprocess.Popen(['xterm','-e',runDisplay])
    while running:
        time.sleep(1)
    p.terminate()


def tracker():
    print('starting tracker')
    time.sleep(3)
    p=subprocess.Popen(['xterm','-e',runTracker])
    while running:
        time.sleep(1)
    p.terminate()



 
 
 
 
 
def startFly():
    global running
    print('fly VR is starting')
    displayThread = threading.Thread(target=displayServer)
    displayThread.start()
    trackerThread = threading.Thread(target=tracker)
    trackerThread.start()
    print('starting stimuli')
     
    subprocess.call(['python',runStimuli])
     
    running = False
    print('fly VR is done')
    displayThread.join()
    trackerThread.join()
 
def main():
    startFly()



if __name__ == '__main__':
    main()