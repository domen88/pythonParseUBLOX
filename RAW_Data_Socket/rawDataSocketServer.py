#!/usr/bin/python

import sys
import socket
import serial
import threading

def printit():
  threading.Timer(20.0, printit).start()
  print "Sending Data..."

def main(argv):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 2101))
    server_socket.listen(2)

    while True:
        # accept connections
        print 'Wait for connection'
        (socketClient, address) = server_socket.accept()
        try:
            print 'Client ADDRESS: ', address
            print 'Start sending data to client'

            #TODO Send Data
            try:
                ser = serial.Serial('/dev/ttyUSB0') # open serial port
                # print(ser.name) # check which port was really used
                ser.baudrate = 115200
            except serial.SerialException as e:
                print 'IOError ', e.strerror

            printit()

            while True:
                # STREAM
                line = self.serial.read(512)
                socketClient.send(line)

            #TODO Error case
            #print >> sys.stderr, 'Protocol Error!! Exit'
            socketClient.close()
            sys.exit(0)

        except (KeyboardInterrupt, SystemExit):
            print >> sys.stderr, 'KeyboardInterrupt or SystemExit Received. Exit.'
            socketClient.close()

        finally:
            # close connection
            print 'Client ', address, 'Disconnected.'
            socketClient.close()

if __name__ == "__main__":
    main(sys.argv[1:])
