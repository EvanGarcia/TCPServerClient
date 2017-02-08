#Evan Garcia
#Professor Tindall
#CSC 4800
#February, 8, 2017
#Once a connection is made with the client module, this program executes commands depending on what it receives from the client.

from time import ctime, sleep
from socket import *
import os

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection...\n')
    tcpCliSock, addr = tcpSerSock.accept()

    #If tcpCliSock != -1, the server has connected to the client
    if(tcpCliSock != -1):
        print('connected...')

    while True:
        #Recieve information from the client
        data = tcpCliSock.recv(BUFSIZ)
            
        if not data:
            break
        
        #Place commands and parameters in a dataList
        dataList = [1]
        dataString = data.decode('utf-8')
        if dataString.count(' ') == 1:
            dataList = dataString.split()
        else:
            dataList[0] = dataString

        #EXITSERVER: Closes all sockets, and terminates server and client
        if  dataList[0].lower() == 'exitserver' and len(dataList) == 1 :
                tcpCliSock.close()
                tcpSerSock.close()
                exit()
        #DATE: Sends current date/timestamp to client
        elif dataList[0].lower() == 'date' and len(dataList) == 1 :
            tcpCliSock.send(bytes('Date: %s' % (ctime()), 'utf-8'))
        #OS: Sends operating system info to client
        elif dataList[0].lower() == 'os' and len(dataList) == 1 :
            tcpCliSock.send(bytes('OS: %s' % (os.name), 'utf-8'))
        #LS: Sends directory information (Directory and File Listings) to client
        elif dataList[0].lower() == 'ls' and len(dataList) <= 2 :
            if len(dataList) == 1:
                DirectoryInfo = os.listdir()
                tcpCliSock.send(bytes('LS: %s' % (DirectoryInfo), 'utf-8'))
            elif len(dataList) == 2:
                if os.path.exists(dataList[1]):
                    DirectoryInfo = os.listdir(dataList[1])
                    tcpCliSock.send(bytes('LS \"%s\": %s' % (dataList[1], DirectoryInfo), 'utf-8'))
                else:
                    tcpCliSock.send(bytes('Invalid Parameter for LS function', 'utf-8'))
        #SLEEP: Server sleeps for 5 secs if no other time is specified, and sends sleep time to client
        elif dataList[0].lower() == 'sleep'and len(dataList) <= 2 :
            if len(dataList) == 1:
                sleep(5)
                tcpCliSock.send(bytes('Slept for %i seconds' % (5), 'utf-8'))
            elif len(dataList) == 2 and dataList[1].isdigit():
                sleepTime = int(dataList[1])
                sleep(sleepTime)
                tcpCliSock.send(bytes('Slept for %i seconds' % (sleepTime), 'utf-8'))
            else:
                sleep(5)
                tcpCliSock.send(bytes('Slept for %i seconds' % (5), 'utf-8'))
        #If not one of the commands listed above, echo message to client
        else:
            if len(dataList) == 2:
                dataList[0] = dataList[0] + ' ' + dataList[1]
                tcpCliSock.send(bytes('[%s] %s' % (ctime(), dataList[0]), 'utf-8'))
            else:
                tcpCliSock.send(bytes('[%s] %s' % (ctime(), dataList[0]), 'utf-8'))

    tcpCliSock.close()
tcpSerSock.close()