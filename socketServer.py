#!/usr/bin/python
import sys

import socket

def main(argv):
    #crea server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', 8282))
    serverSocket.listen(1)

    while True:
        #accetta connessioni
        print 'Wait for connection'
        (SocketClient, address) = serverSocket.accept()
        try:
            print 'ADDRESS: ', address
            #receive data
            while True:
                data = SocketClient.recv(16)
                print >> sys.stderr, 'received "%s"' % data
                if data:
                    print >> sys.stderr, 'sending data back to the client'
                    SocketClient.sendall(data)
                else:
                    print >> sys.stderr, 'no more data from', address
                    break
        finally:
            #close connection
            SocketClient.close()


if __name__ == "__main__":
    main(sys.argv[1:])