#!/usr/bin/python

"""
Authors:
    Domenico Scotece
    Michele Solimando

Description:

"""

import sys
import socket
import serial
import signal
from MessageProtocol import MessageProtocol


# Handler Ctrl-C
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # TODO: gestione dell'handler
    sys.exit(0)


def main(argv):

    # Retrieve serial port
    if len(sys.argv) <= 1:
        print >> sys.stderr, 'Usage python '+sys.argv[0]+ ' [port]'
        # Exit with error code
        sys.exit(1)

    port=argv[0]

    # Register handler Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    # Open socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Option to immediately reuse the socket if it is in TIME_WAIT status, due to a previous execution.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8282))
    server_socket.listen(1)

    while True:
        # accept connections
        print 'Wait for connection'
        (socketClient, address) = server_socket.accept()
        try:
            print 'Client ADDRESS: ', address
            # receive start message
            data = socketClient.recv(MessageProtocol.MSG_START.__len__())

            # DEBUG
            print data

            if data == MessageProtocol.MSG_START:
                print 'Start sending data to client'
                # send ack connection
                socketClient.sendall(MessageProtocol.MSG_OK)

                # Open Serial Port
                try:
                    ser = serial.Serial('/dev/'+port)
                    ser.baudrate = 115200
                except serial.SerialException as e:
                    print 'IOError ', e.strerror

                while True:
                    # STREAM
                    line = ser.readline()
                    if len(line) == 0:
                        socketClient.close()
                        break
                    # Dimensione della linea
                    dim=str(len(line))
                    # Invio lunghezza linea
                    socketClient.sendall(dim)
                    # Invio linea
                    socketClient.sendall(line)

            else:
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
