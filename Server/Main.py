import string
import socket
import threading

from ResponseGenerator import ResponseGenerator

_socket = None         # socket object...

def toUTF(text):        # this method will convert strings from 'ascii' to 'utf-8'...
    encoded = text.encode('utf-8')
    length = len(encoded)
    x, y = divmod(length, 256)

    _bytearray = bytearray()
    _bytearray.append(x)
    _bytearray.append(y)

    for _byte in encoded:
        _bytearray.append(_byte)
    
    return _bytearray

def backgroundWorker():     # this method will run on a different thread...
    global _socket

    print('background worker running...')

    while True:
        if _socket is not None:
            text = _socket.recv(1024).decode('utf-8')[2:]    # receiving text from client...
            
            if len(text) != 0:
                print('client said: ' + str.strip(text))     # printing the text received from client (for debugging purpose)...
                _socket.send(toUTF(responseGenerator.getResponse(text)))    # generating appropriate response and sending to client...

responseGenerator = ResponseGenerator()     # creating response generator object...

serverSocket = socket.socket()      # creating socket object...
serverSocket.bind((socket.gethostname(), 60225))    # binding socket to address (host-name, port)...
serverSocket.listen(5)

threading.Thread(target = backgroundWorker).start()       # starting background thread...

while True:         # this infinite loop accepts new clients and running on main thread...
    print('waiting for client...')
    
    _socket, address = serverSocket.accept()
    
    print('client connected...')