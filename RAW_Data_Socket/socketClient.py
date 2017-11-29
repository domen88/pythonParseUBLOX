#!/usr/bin/python

"""
Authors:
    Domenico Scotece
    Michele Solimando

Description:

"""

#   1 Intercept Server close socket (EOF or Read/Write Error)
#   2 Receive buffered data

import sys
import socket
import signal
from MessageProtocol import MessageProtocol


# Intercept SIGINT
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def main(argv):

    # Retrieve server ip address
    if len(sys.argv) <= 1:
        print >> sys.stderr, 'Usage python ' + sys.argv[0] + ' [ip address]'
        # Exit with error code
        sys.exit(1)

    ipserver = argv[0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipserver, 8282))

    try:
        # send first protocol message
        s.sendall(MessageProtocol.MSG_START)
        print 'sending start message "%s"' % MessageProtocol.MSG_START

        # receive ack from server
        data = s.recv(MessageProtocol.MSG_OK.__len__())
        print 'Ack received from server.'
        text_file = open("ricevuto.txt", 'w')

        if data == MessageProtocol.MSG_OK:
            print 'Starting to receive server data...'
            # receive data from server
            while True:
                # Ricevi lunghezza della linea
                dim=s.recv(12)
                # Ricevi linea
                data=s.recv(int(dim))
                if len(data) == 0:
                    text_file.write("\n")
                    text_file.close()
                    break
                else:
                    text_file.write(data)
                    text_file.flush()

        else:
            print >> sys.stderr, 'Protocol Error!! Exit'
            s.close()
            # Exit with error code
            sys.exit(1)

    except KeyboardInterrupt:
        print >> sys.stderr, 'Keyboard Interrupt received. Exit.'
        s.close()
        sys.exit(2)
    finally:
        print >> sys.stderr, 'closing socket'
        s.close()
        sys.exit(3)


if __name__ == "__main__":
    main(sys.argv[1:])