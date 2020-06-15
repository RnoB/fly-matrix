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



import threading
import time
import socket
import struct
import expAnal
import matrixNet
import matrixIP
import dbLoc
import sqlite3
import urllib.request as ur
import threading
import datetime as dt
import os
from shutil import copyfile
running = True

backupPath = "/home/flyvr/flyvr/dbBackup/" 
dbpath = "/home/flyvr/flyvr/dbBackup/" 
def updateDatabase():

    today = dt.datetime.now()

    path = backupPath+ today.strftime('%y-%m-%d')
    if not os.path.exists(path):
            os.mkdir(path)
    projectDB = dbPath+"/matrixProjects.db"
    expDB = dbPath+"/matrixExperiments.db"
        

    projectDBBackup = Path+"/matrixProjects.db"
    expDBBackup = Path+"/matrixExperiments.db"
    ur.urlretrieve(projectDB,projectDBBackup )
    ur.urlretrieve(expDB,expDBBackup )


def main():
    global running
    updateDatabase()
    t0 = time.time()
    tSleep = 25-dt.datetime.now().hour
    print('sleeping for '+str(tSleep)+' hours')
    while running:
        time.sleep(3600*tSleep)
        updateDatabase()
        t = time.time()-t0
        print(">>>>>>>>>>>> MalkoFish <<<<<<<<<<")
        print("Backuping your database since " + str(int(t/3600)) +" hours")
        tSleep = 24



if __name__ == '__main__':
    main()
