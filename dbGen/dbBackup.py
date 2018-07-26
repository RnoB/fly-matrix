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
