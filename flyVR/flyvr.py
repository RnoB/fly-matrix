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
import sys
import datetime
import time
import random
import math
import select
import struct
import uuid
import sqlite3
import numpy as np
from shutil import copyfile
from tetheredvr.proxy import JSONStimulusOSGController
from tetheredvr.observers import SimulatedObserver, CarModelSocketObserver
import emailer

replication = 4

project = 'DecisionGeometry'
experimenter = 'VHS'

projectDB = '/home/flyvr/flyvr/fly-matrix/dbGen/flyProjects.db'
expDB = '/home/flyvr/flyvr/fly-matrix/dbGen/flyExperiments.db'
pathData = '/home/flyvr/flyvr/data/'

running = 1
numberPost = 10


def pathDefine(path,ids, params=[]):
    path = path + str(ids)
    if not os.path.exists(path):
        os.makedirs(path)
    for param in params:
        path = path + '/' + str(param)
        if not os.path.exists(path):
            os.makedirs(path)
    return path




def distance(pos0, pos1, post):
    if post == True:
        dx = pos0['x'] - pos1[0]
        dy = pos0['y'] - pos1[1]
    else:
        dx = pos0['x'] - pos1['x']
        dy = pos0['y'] - pos1['y']

    return math.sqrt(dx**2 + dy**2)


# Main Function
class MyExperiment(object):

    def __init__(self, osg_file):
        # the proxy instance allows us to talk to the display server
        self.ds_proxy = JSONStimulusOSGController()
        # create the observer
        self.observer = CarModelSocketObserver(self._observer_callback)
        # load the provided OSG file
        self.ds_proxy.set_stimulus_plugin('StimulusOSG')
        self.ds_proxy.load_osg(osg_file)

        self.expTrial = -1
        self.replicate = -1
        self.tSwitch = 0
        self.tExp = 0
        self.dateStart = ''

        # set starting position for stimuli
        self.rootPosition = np.zeros((1,2))
        self.postPosition = np.zeros((numberPost,2))
        self.postDistance = 5.0

        # set starting position of fly
        self.start_position = {'x': 0.0, 'y': 0.0, 'z': -0.07}
        self.ds_proxy.set_position(**self.start_position)

        # assign experiment a unique id
        self.expId = uuid.uuid4()
        # get experiment conditions from database
        self.getExperiment()
        # start every experiment with a no post condition
        self.updateStimuli(0)
        emailer.twitStatus(self.expId,status = 0, t=self.tExp)
        self.running = True
        # event counter (number of times fly position is reset)
        self.cntr = 0


    def _observer_callback(self, info_dict):
        #print info_dict
        self.move_fixed_observer(**info_dict)


    def move_fixed_observer(self, **kwargs):
        x = -kwargs.get('x')
        y = -kwargs.get('y')
        z = -kwargs.get('z')

        self.ds_proxy.move_node('Root',x ,y ,0)
        #for n in range(0,10):
            #self.ds_proxy.move_node('Cylinder' + str(n), x + self.postPosition[n,0], y + self.postPosition[n,1], 0)


    def getExperiment(self):
        # establish a connecttion to the project database
        conn = sqlite3.connect(projectDB)
        # connect a cursor that goes through the project database
        cursorProject = conn.cursor()
        # establish a second connecttion to the experiment database
        conn2 = sqlite3.connect(expDB)
        # connect a cursor that goes through the experiment database
        cursorExperiment = conn2.cursor()

        # pick a random experiment from specified project
        cursorProject.execute("Select exp from projects where project = ? ",(project,))
        fetched = cursorProject.fetchall()
        print('fetched : ' + str(fetched))
        
        expType = np.unique(fetched)
        print('the type of experiment i have in stock are '+str(expType))
        self.expTrial = -1
        
        # if number of replicates is not met, run experiment
        for k in range(0,len(expType)):
            expTemp = int(expType[k])
            print((project,expTemp,))
            cursorExperiment.execute("Select * from experiments where project = ? and exp = ? ",(project,expTemp,))
            fetched2 = cursorExperiment.fetchall()
            print('We already have ' + str(len(fetched2)) + ' replicates')
            if len(fetched2) < replication:
                self.expTrial = expTemp
                break

        if self.expTrial > -1:
            cursorProject.execute("Select replicate from projects where project = ? and exp = ? ",(project,self.expTrial,))
            fetched = cursorProject.fetchall()
            repType = np.unique(fetched)
            print('plenty of replicates : ' + str(repType))
            repIdx = np.random.randint(len(repType), size=1)
            print(repType)
            self.replicate = int(repType[repIdx])
            print('so lets pick ' + str(self.replicate))
            cursorProject.execute("Select tSwitch from projects where project = ? and exp = ? and replicate = ?",(project,self.expTrial,self.replicate,))
            fetched = cursorProject.fetchall()
            print('fetched : ' + str(fetched))
            self.tSwitch = np.unique(fetched)
            cursorProject.execute("Select tExp from projects where project = ? and exp = ? and replicate = ?",(project,self.expTrial,self.replicate,))
            self.tExp = np.unique(cursorProject.fetchall())  
            self.dateStart = datetime.datetime.now()      
        else:
            tExp = 0

        # close all established connections
        conn.close()
        conn2.close()


    def experiment_start(self):
        # self.recorder.start()
        self.observer.start_observer()
        self.loop()


    def loop(self):
        
        nStimuli = 0
        t0 = time.time()
        sl_t0 = time.time()
        
        lastMessage = True

        # write output file in specified directory
        path = pathDefine(pathData,self.expId)
        with open(path+'/results.csv', 'w') as output:
            while self.running:
                pos = self.observer.position
                direc = self.observer.azimuth
                t = time.time() - t0
                sl_t = time.time() - sl_t0

                if sl_t < 3:
                    self.observer.velocity = 0.0
                else:
                    self.observer.velocity = 0.20

                if t > self.tExp*60*.9 and lastMessage:

                    try:
                        emailer.twitStatus(self.expId,status = 1, t=self.tExp*.1)
                    except:
                        pass
                    lastMessage = False

                if t > self.tExp*60:
                    self.running = False
                    self.writeInDb()
                    emailer.twitStatus(self.expId,status = 2, t=self.tExp)                   
                elif t > (nStimuli+1)*self.tSwitch*60:
                    nStimuli = nStimuli+1
                    self.observer.reset_to(**self.start_position)
                    self.updateStimuli(nStimuli)
                    sl_t0 = time.time()
                    self.cntr = 0
                
                for nPost in range(0,10):
                    if distance(pos, self.postPosition[nPost,:], True) < 0.5:
                        self.observer.reset_to(**self.start_position)
                        self.cntr += 1
                        sl_t0 = time.time()
                        break
                if distance(pos, self.start_position, False) > self.postDistance:
                    self.observer.reset_to(**self.start_position)
                    self.cntr += 1
                    sl_t0 = time.time()

            #print "XYZ(%3.2f, %3.2f, %3.2f)" % (pos['x'], pos['y'], pos['z']), self.counter     
                #print(t)  
                output.write('%.8f, %.8f, %.8f, %.4f, %d, %.8f, %s\n' % (pos['x'], pos['y'], pos['z'], direc, self.cntr, t, str(nStimuli)))
                time.sleep(0.005)


    def updateStimuli(self,nStimuli):
        # establish a connecttion to the project database
        conn = sqlite3.connect(projectDB)
        # connect a cursor that goes through the project database
        cursorProject = conn.cursor()
        # pick a new stimulus from available permutations
        for nPost in range(0,10):
            print((project,self.expTrial,self.replicate,nStimuli))
            cursorProject.execute("Select post"+str(nPost)+" from projects where project = ? and exp = ? and replicate = ? and nStimuli =?",(project,self.expTrial,self.replicate,nStimuli))
            fetched = cursorProject.fetchall()

            data = fetched[0][0]
            #print(data)
            if data == 'None':
                #Should be the name of the blender file
                self.postPosition[nPost,:] = [1000,1000]
            else:
                dictData = eval(data)
                print(dictData['position'])
                self.postPosition[nPost,:] = dictData['position']
                self.postDistance = dictData['distance']
            self.ds_proxy.move_node('Cylinder' + str(nPost), self.postPosition[nPost,0],  self.postPosition[nPost,1], 0)
            #print(self.postPosition)
        
        # close connection
        conn.close()


    def writeInDb(self):
        todayDate = self.dateStart.strftime('%Y-%m-%d')
        self.startTime = self.dateStart.strftime('%H:%M')
        self.endTime = datetime.datetime.now().strftime('%H:%M')
        # establish a connection to the experiment database
        conn2 = sqlite3.connect(expDB)
        # connect a cursor that goes through the experiment database
        cursorExperiment = conn2.cursor()

        expId = 0
        values = [project,self.expTrial,self.replicate,
                      todayDate,self.startTime,self.endTime,
                      experimenter,str(self.expId)]
        cursorExperiment.execute("INSERT INTO experiments VALUES (?,?,?,?,?,?,?,?)",values)
        
        # commit and close connection
        conn2.commit()
        conn2.close()
        
            


def main():
    # OSGT files need to be in /home/flyvr/flyvr/FreemooVR/data
    ex = MyExperiment(osg_file='ten_post_stimulus.osgt')

    try:
        ex.experiment_start()

    except KeyboardInterrupt:
        sys.stderr.write('[QUIT] via user request <ctrl+c>')

#    finally:
#        ex.experiment_stop()


if __name__ == '__main__':
    main()
