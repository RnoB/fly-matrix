#MIT License

#Copyright (c) 2020 Renaud Bastien

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
###########


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
