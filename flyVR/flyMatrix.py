import flyStarter
import socket
import matrixIP
import matrixNet
import threading
import time
import struct
running = True
expTime = 90

expThread = []


def killExperiment():

    print('need to define something')



def masterControl():
    global expThread
    state = 'waiting'
    backlog = 1  
    maxsize = 28
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    binded = False
    t0 = 0
    while not binded:
        try:
            server.bind((matrixIP.flyVRIP,matrixNet.multiTrackerPort))
            binded = True
        except:
            print('- Give Status -- binding failed')
            binded = False
    server.listen(1)
    print('Waiting for instructions')
    while running:
        time.sleep(.1)
        #print('--- waiting for a connection')
        connection, client_address = server.accept()
        print('------ Connection coming from ' + str(client_address))



        code = struct.unpack('i',connection.recv(4))[0]
        print('------ code : '+ str(code))
        if code == matrixNet.multiTrackCode[0]:
            data = struct.pack('i', code+1)
            t0 = time.time()
            try:
                if len(expThread) > 0:
                    print('already running')
                else:
                    expThread.append(threading.Thread(target = flyStarter.startFly))
                    expThread[-1].daemon = True
                    expThread[-1].start()
                    print('here')
                connection.sendall(data)

            except:
                print('sending did not work :/ but better not break everything')
        if code == matrixNet.multiTrackCode[2]:
            dt=int(expTime-(time.time()-t0)/60)

            if dt>0:
                state = 2
            elif dt<0:
                state = 0
                dt = 0
            print("The state is : " + str(state));
            print("the time left is : "+str(dt))
            data = struct.pack('iii', code+1,state,dt)
            try:
                

                connection.sendall(data)

            except:
                print('sending did not work :/ but better not break everything')

        if code == matrixNet.killCode:
            killExperiment()
        






def main():
    
    global expThread

    statusThread = threading.Thread(target = matrixNet.giveStatus, args=(matrixIP.flyVRIP,))
    statusThread.daemon = True
    statusThread.start()

    masterThread = threading.Thread(target = masterControl)
    masterThread.daemon = True
    masterThread.start()

    t0 = time.time()
    while running:
        t = time.time()-t0
        time.sleep(60)
        if len(expThread)>0:
            expThread[-1].join()
            expThread = []
            try:
                emailer.twitStatus('',status = 3)
            except:
                pass
        if int(t/60) % 60 == 0:

            print(">>>>>>>>>>>> the FlyMatrix is in service since " + str(int(t/3600)) +" hours")




    



if __name__ == '__main__':
    main()