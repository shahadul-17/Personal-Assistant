import string
import socket
import threading

from Utility import Utility
from ResponseGenerator import ResponseGenerator

class Main:

    port = None
    _socket = None         # socket object...
    responseGenerator = ResponseGenerator()     # creating response generator object...

    def __init__(self):
        self.port = Utility.getValueFromConfigurationFile('port')

        serverSocket = socket.socket()      # creating socket object...
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(('', int(self.port)))    # binding socket to address (host-name, port)...
        serverSocket.listen(5)

        print('server running...\n\nip-address = ' + socket.gethostbyname(socket.gethostname()) + '\nport = ' + self.port)

        threading.Thread(target = self.backgroundWorker).start()       # starting background thread...

        while True:         # this infinite loop accepts new clients and running on main thread...
            print('waiting for client...')
            
            self._socket, address = serverSocket.accept()
            
            print('client connected...')
    
    def toUTF(self, text):        # this method will change character encoding from ASCII to UTF-8...
        encoded = text.encode('utf-8')
        length = len(encoded)
        x, y = divmod(length, 256)

        _bytearray = bytearray()
        _bytearray.append(x)
        _bytearray.append(y)

        for _byte in encoded:
            _bytearray.append(_byte)
        
        return _bytearray

    def backgroundWorker(self):     # this method will run on a different thread...
        print('background worker running...')

        while True:
            if self._socket is not None:
                text = self._socket.recv(1024).decode('utf-8')    # receiving text from client...
                
                if len(text) != 0:
                    text = str.strip(text[2:])

                    print('client said: ' + text)     # printing the text received from client (for debugging purpose)...
                    self._socket.send(self.toUTF(self.responseGenerator.getResponse(text)))    # generating appropriate response and sending to client...

if __name__ == '__main__':      # main method... execution of this program starts from here...
    Main()