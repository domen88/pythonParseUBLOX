#!/usr/bin/python

import sys
import socket
import serial
import threading
import os
import time

def printit():
  threading.Timer(20.0, printit).start()
  print "Sending Data..."

def main(argv):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 2101))
    server_socket.listen(2)

    while True:
        # accept connections
        print 'Wait for connection'
        (socketClient, address) = server_socket.accept()
        try:
            #Reset SERIAL
            print 'Client ADDRESS: ', address
            print 'Resetting serial port...'
            os.system("modprobe -r pl2303")
            os.system("modprobe -r usbserial")
            time.sleep(5)
            os.system("modprobe pl2303")
            time.sleep(5)
            print 'Serial Port OK!'
            print 'Start sending data to client'

            #Open SERIAL
            try:
                ser = serial.Serial('/dev/ttyUSB0')
                ser.baudrate = 115200
            except serial.SerialException as e:
                print 'IOError ', e.strerror

            printit()

            while True:
                # Read Serial and Stream TCP
                line = ser.read(256)
                socketClient.send(line)

            socketClient.close()
            sys.exit(0)

        except (KeyboardInterrupt, SystemExit):
            print >> sys.stderr, 'KeyboardInterrupt or SystemExit Received. Exit.'
            socketClient.close()
            #sys.exit(1)
            os._exit(0)

        finally:
            print 'Client ', address, 'Disconnected.'
            socketClient.close()

if __name__ == "__main__":
    main(sys.argv[1:])
