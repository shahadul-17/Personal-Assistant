import string
import socket
import threading

from ResponseGenerator import ResponseGenerator

_socket = None         # socket object...
_responseGenerator = ResponseGenerator()     # creating response generator object...

serversocket = socket.socket()      # creating socket object...
serversocket.bind((socket.gethostname(), 60225))    # binding socket to address (host-name, port)...
serversocket.listen(5)

def backgroundWorker():     # this method will run on a different thread...
    global _socket

    print('background worker running...')

    while True:
        if _socket is not None:
            text = _socket.recv(1024).decode('ascii')    # receiving text from client...
            
            if text != "":
                print('client said: ' + str.strip(text))     # printing the text received from client (for debugging purpose)...
                _socket.send((_responseGenerator.respond(text) + '\r\n').encode('ascii'))    # generating appropriate response and sending to client...

threading.Thread(target = backgroundWorker).start()       # starting background thread...

while True:         # this infinite loop accepts new clients and running on main thread...
    print('Waiting for client...')

    _socket, addr = serversocket.accept()

    print('Client connected...')