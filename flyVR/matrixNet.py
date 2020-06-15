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



import numpy
import threading
import time
import socket
import struct
import numpy as np
import uuid
import matrixIP


broadcastPort = 5005
measurePort = 5006
statusPort = 5007
modifPort = 5008
measurementPort = 5009


fishVRPort = 5010
malkoPort = 5011


multiTrackerPort = 5012

requestStatusCode = 1001
sendStatusCode = 1002
isStarted =[1003,1004]
idCode = [2101,2102,2103,2104]
measurementCode = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]
modifCode = [3001,3002,3003,3004,3005,3006,3007,3008]
expCode = [4001,4002,4003,4004,4005,4006,4007,4008]
fishVRCode = [5001,5002,5003,5004]
startTrackingCode = [6001,6002,6003,6004,6005,6006,6007,6008,6009,6010,6011,6012,6013,6014]
startDisplayCode = [7001,7002,7003,7004,7005,7006,7007,7008,7009,7010,7011,7012,7013,7014]


startMatrixCode = [8001,8002,8003,8004]

startAnalCode = [9001,9002]

stimuliCode =[10001,10002,10003,10004,10005,10006,10007,10008,10009,10010]
newStimuliCode = [11001,11002,11003,11004]
newBackGroundCode =[12001,12002]

multiTrackCode = [34001,34002,34003,34004]

killCode = 99999

running = True


max_int64 = 0xFFFFFFFFFFFFFFFF


def broadcastSize(fishVR,size):
    global running
    socketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketSend.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketSend.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print('>> Apoc wants everybody to know the size of the fish : ')


    data = struct.pack('id', fishVR,size)

    #print('Send : ' + str(struct.unpack('dddi', data)))
    try:
        socketSend.sendto(data, (matrixIP.apocWifi , measurementPort + 20))
        time.sleep(1)
    except:
        print('sometthing went with wrong  broadcasting')

    socketSend.close()
    print('Sender Disconnected')

def giveStatus(ip):
    backlog = 1  # how many connections to accept
    maxsize = 28
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    binded = False
    while not binded:
        try:
            server.bind((ip,statusPort))
            binded = True
        except:
            print('- Give Status -- binding failed')
            binded = False
            time.sleep(20)
    server.listen(1)
    while running:
        print('--- waiting for a connection')
        try:
            connection, client_address = server.accept()
            print('------ Connection coming from ' + str(client_address))



            code = struct.unpack('i',connection.recv(4))[0]
            print('------ code : '+ str(code))
            if code == requestStatusCode:
                data = struct.pack('i', sendStatusCode)
                try:
                    connection.sendall(data)
                except:
                    print('sending did not work :/ but better not break everything')
        except:
            pass


def requestStatus(ip):
    status = False
    socketClient = socket.socket()
    socketClient.settimeout(10)
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    fishN=0
    print('--- Connection to ' + str(ip))

    try:
        socketClient.connect((ip, statusPort))
        print('--- Connected to ' + str(ip))
        try:
            data = struct.pack('i', requestStatusCode)
            socketClient.sendall(data)
            code = struct.unpack('i',socketClient.recv(4))[0]
            if code == sendStatusCode:
                status = True      
        finally:
            socketClient.shutdown(socket.SHUT_RDWR)
            socketClient.close()

    except:
        pass
        #print('--- connection failed')  
    return status



def checkVRStatus():
    fishVRStatus = np.zeros(5)
    for k in range(0,5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        try:
            s.connect((matrixIP.fishVRIP[k], 8081))
            print("Port 8081 reachable")
            fishVRStatus[k] = 1

        except socket.error as e:
            print ("Error on connect: %s" % e)
        s.close()
    return fishVRStatus



def sendMalko(code=startAnalCode[0],dataSend=[]):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    
    print('--- MalkoFish Connection  ')

    
    while connect == 0:
        try:
            socketClient.connect((matrixIP.malkoFishIP, malkoPort))
            connect = 1
        except:
            connect = 0
    print('--- MalkoFish connected')
    if code == startAnalCode[0]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))

    print(dataRec)
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    print('MalkoFish Disconnected')
    return dataRec




def sendModif(code,dataSend = []):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    
    print('--- architect Connection  ')

    
    while connect == 0:
        try:
            socketClient.connect((matrixIP.architectIP, modifPort))
            connect = 1
        except:
            connect = 0
    print('--- Architect connected')
    if code == idCode[0]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec=[]
        dataRec.append(struct.unpack('i',socketClient.recv(4))[0])
        a,b = struct.unpack('>QQ',socketClient.recv(16))
        unpacked = (a << 64) | b

        dataRec.append(uuid.UUID(int=unpacked))
    if code == idCode[2]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))[0]
        if dataRec == idCode[3]:
            u=dataSend
            data = struct.pack('>QQ', (u.int >> 64) & max_int64, u.int & max_int64)
            socketClient.sendall(data)

        


    if code in expCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('ii',socketClient.recv(8))
    if code in fishVRCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('iiiiii',socketClient.recv(24))
    if code in modifCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        data = struct.pack('i', dataSend[0])
        socketClient.sendall(data)
        dataRec = struct.unpack('ii',socketClient.recv(8))
    if code in startDisplayCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code in startTrackingCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code in startMatrixCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code == killCode:  
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code == isStarted[0]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('ii',socketClient.recv(8))
    if code == measurementCode[8]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        data = struct.pack('ddddd',dataSend[0],dataSend[1],dataSend[2],dataSend[3],dataSend[4])
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))


    print(dataRec)
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    print('Architect Disconnected')
    return dataRec




def sendMeasure(code,dataSend = []):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    
    print('--- apoc Connection  ')

    
    while connect == 0:
        try:
            socketClient.connect((matrixIP.apocIP, measurementPort))
            connect = 1
        except:
            connect = 0
    print('--- Apoc connected')
    if code == measurementCode[0]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        u=dataSend[0]
        data = struct.pack('>QQ', (u.int >> 64) & max_int64, u.int & max_int64)
        
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code == measurementCode [2]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        data = struct.pack('i', dataSend[0])
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
    if code == measurementCode[4]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('iid',socketClient.recv(16))
    if code == measurementCode[6]:
        data = struct.pack('i', code)
        socketClient.sendall(data)
        dataRec = struct.unpack('i',socketClient.recv(4))
        

    print(dataRec)
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    print('Apoc Disconnected')
    return dataRec



def sendModifVR(mode,dataSend = []):
    for k in range(0,5):
        socketClient = socket.socket()
        socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connect = 0
        print('--- fish VR '+str(k+1)+' Connection IP : '+matrixIP.fishVRIP[k]+' with port :'+str(fishVRPort))
        while connect == 0:
            try:
                socketClient.connect((matrixIP.fishVRIP[k], fishVRPort))
                connect = 1
            except:
                connect = 0
        print('--- fish VR '+str(k+1)+' connected')

        if mode == 0:  
            data = struct.pack('i', newStimuliCode[0])
            socketClient.sendall(data)
            data = struct.pack('i', dataSend[0])
            socketClient.sendall(data)
        if mode == -1:
            data = struct.pack('i', newStimuliCode[2])
            socketClient.sendall(data)

        
        dataRec = struct.unpack('i',socketClient.recv(4))
        print(dataRec)
        socketClient.shutdown(socket.SHUT_RDWR)
        socketClient.close()
        print('fish VR '+str(k)+' Disconnected')
       
def sendModifVRInd(k,mode,dataSend = []):
    
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    print('--- fish VR '+str(k+1)+' Connection IP : '+matrixIP.fishVRIP[k]+' with port :'+str(fishVRPort))
    while connect == 0:
        try:
            socketClient.connect((matrixIP.fishVRIP[k], fishVRPort))
            connect = 1
        except:
            connect = 0
    print('--- fish VR '+str(k+1)+' connected')

    if mode == 0:  
        data = struct.pack('i', newStimuliCode[0])
        socketClient.sendall(data)
        data = struct.pack('i', dataSend[0])
        socketClient.sendall(data)
    if mode == -1:
        data = struct.pack('i', newStimuliCode[2])
        socketClient.sendall(data)

    
    dataRec = struct.unpack('i',socketClient.recv(4))
    print(dataRec)
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    print('fish VR '+str(k)+' Disconnected')


def switchStimuli(fishVR,fish,mode,dataSend = []):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    
    print('--- fish VR '+str(fishVR+1)+' Connection IP : '+matrixIP.fishVRIP[fishVR]+' with port :'+str(fishVRPort))


    while connect == 0:
        try:
            socketClient.connect((matrixIP.fishVRIP[fishVR], fishVRPort))
            connect = 1
        except:
            connect = 0
    print('--- fish VR '+str(fishVR+1)+' connected')
    print('------ sending ' +str(mode))
    if mode<newBackGroundCode[0]:
        code = stimuliCode[fish*2]
        data = struct.pack('i', code)
        socketClient.sendall(data)
        data = struct.pack('i', int(mode))
        socketClient.sendall(data)
        if mode == 1:
            data = struct.pack('ddd', dataSend['x'],dataSend['y'],dataSend['z'])
            socketClient.sendall(data)
        if mode == 2:
            print(dataSend)
            data = struct.pack('dddi', dataSend['speed'],dataSend['z'],dataSend['r'],int(dataSend['clockwise']))
            
            socketClient.sendall(data)
        if mode == 3:
            print(dataSend)
            data = struct.pack('dddddi', dataSend['speed'],dataSend['z'],dataSend['r'],dataSend['tBeat'],dataSend['tBurst'],int(dataSend['clockwise']))
            
            socketClient.sendall(data)
        if mode == 21:
            print(dataSend)
            data = struct.pack('d', dataSend['scale'])
            print(len(data))
            socketClient.sendall(data)
        if mode == 22:
            print(dataSend)
            data = struct.pack('i', int(dataSend['mesh']))
            print(len(data))
            socketClient.sendall(data)
        if mode == 23:
            print(dataSend)
            data = struct.pack('d', dataSend['phiOffset'])
            print(len(data))
            socketClient.sendall(data)
        if mode == 24:
            print(dataSend)
            data = struct.pack('ddd', dataSend['scaleX'],dataSend['scaleY'],dataSend['scaleZ'])
            print(len(data))
            socketClient.sendall(data)
        if mode == 5:
            data = struct.pack('d', dataSend['delay'])
            socketClient.sendall(data)

    if mode == newBackGroundCode[0]:
        code = newBackGroundCode[0]
        data = struct.pack('i', code)
        socketClient.sendall(data)
        print('sending the backgound ')
        data = struct.pack('i', int(dataSend['background']))
        socketClient.sendall(data)


  
    dataRec = struct.unpack('i',socketClient.recv(4))
    print(dataRec)
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    print('fish VR '+str(fishVR+1)+' Disconnected')
    return dataRec


