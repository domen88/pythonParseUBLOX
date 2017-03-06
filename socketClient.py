#!/usr/bin/python

"""
Authors:
    Domenico Scotece
    Michele Solimando

Description:

"""

# TODO:
#   1 Intercept Server close socket (EOF or Read/Write Error)
#   2 Receive buffered data

import sys
import socket
import signal


# Intercept SIGINT
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# Class Shared Client/Server
class MessageProtocol:
    MSG_START = 'start'
    MSG_STOP = 'stop'
    MSG_OK = 'ok'


def main(argv):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8282))
    try:
        # send first protocol message
        s.sendall(MessageProtocol.MSG_START)
        print 'sending start message "%s"' % MessageProtocol.MSG_START

        # receive ack from server
        data = s.recv(MessageProtocol.MSG_OK.__len__())
        print 'Ack received from server.'

        if data == MessageProtocol.MSG_OK:
            print 'Starting to receive server data...'
            # receive data from server

        else:
            print >> sys.stderr, 'Protocol Error!! Exit'
            s.close()
            # Exit with error code
            sys.exit(1)

        """
        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = s.recv(16)
            amount_received += len(data)
            print >> sys.stderr, 'received "%s"' % data
        """

    except KeyboardInterrupt:
        print >> sys.stderr, 'Keyboard Interrupt received. Exit.'
        s.close()
    finally:
        print >> sys.stderr, 'closing socket'
        s.close()


if __name__ == "__main__":
    main(sys.argv[1:])