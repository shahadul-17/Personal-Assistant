import string
import socket
import threading

from ResponseGenerator import ResponseGenerator

_socket = None         # socket object...
responseGenerator = ResponseGenerator()     # creating response generator object...

serverSocket = socket.socket()      # creating socket object...
serverSocket.bind((socket.gethostname(), 60225))    # binding socket to address (host-name, port)...
serverSocket.listen(5)

def backgroundWorker():     # this method will run on a different thread...
    global _socket

    print('background worker running...')

    while True:
        if _socket is not None:
            text = _socket.recv(1024).decode('ascii')    # receiving text from client...
            
            if text != "":
                print('client said: ' + str.strip(text))     # printing the text received from client (for debugging purpose)...
                _socket.send((responseGenerator.getResponse(text) + '\r\n').encode('ascii'))    # generating appropriate response and sending to client...

threading.Thread(target = backgroundWorker).start()       # starting background thread...

while True:         # this infinite loop accepts new clients and running on main thread...
    print('Waiting for client...')

    _socket, address = serverSocket.accept()

    print('Client connected...')