#!/usr/bin/python

import sys
import socket

def main(argv):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Option to immediately reuse the socket if it is in TIME_WAIT status, due to a previous execution.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8282))
    server_socket.listen(1)

    while True:
        # accept connections
        print 'Wait for connection'
        (socketClient, address) = server_socket.accept()
        try:
            print 'Client ADDRESS: ', address
            print 'Start sending data to client'

            # TODO Send Data

            #TODO Error case
            print >> sys.stderr, 'Protocol Error!! Exit'
            socketClient.close()
            # Exit with error code
            sys.exit(1)

        except (KeyboardInterrupt, SystemExit):
            print >> sys.stderr, 'KeyboardInterrupt or SystemExit Received. Exit.'
            socketClient.close()

        finally:
            # close connection
            print 'Client ', address, 'Disconnected.'
            socketClient.close()

if __name__ == "__main__":
    main(sys.argv[1:])
