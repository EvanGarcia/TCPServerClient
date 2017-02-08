#Evan Garcia
#Professor Tindall
#CSC 4800
#February, 8, 2017
#Once a connection is made with the server module, this program sends commands to the server for execution.

from socket import *

HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
#Connect to server
tcpCliSock.connect(ADDR)

while True:
    #User enters command or message
    data = input('> ')
    if not data:
        break
    #Send command/message to server
    tcpCliSock.send(bytes(data, 'utf-8'))
    #Recieve server's reply
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    #Print server's reply
    print(data.decode('utf-8'))

tcpCliSock.close()
