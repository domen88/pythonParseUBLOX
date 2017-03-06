#!/usr/bin/python
import sys

import socket

def main(argv):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8282))
    try:
        #send data
        message = 'This is the message.  It will be repeated.'
        print >> sys.stderr, 'sending "%s"' % message
        s.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = s.recv(16)
            amount_received += len(data)
            print >> sys.stderr, 'received "%s"' % data

    finally:
        print >> sys.stderr, 'closing socket'
        s.close()

if __name__ == "__main__":
    main(sys.argv[1:])