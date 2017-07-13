#!/usr/bin/python

"""
Authors:
    Domenico Scotece
    Michele Solimando

Description:

"""

import sys
import signal
import ubx


# Handler Ctrl-C
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # TODO: clean environment
    sys.exit(0)


def callback(ty, *args):
    # DEBUG
    # print("callback %s %s" % (ty, repr(args)))
    # FIND LINE NAV-HPPOSECEF && NAV-HPPOSLLH
    if ty == "NAV-HPPOSECEF":
        my_list = repr(args).split()    # string split using space (default) delimiter
        param_counter = 0
        ecef_x = ecef_y = ecef_z = hecef_x = hecef_y = hecef_z = 0
        real_ecef_x = real_ecef_y = real_ecef_z = 0
        for element in my_list:
            ##############################################################
            # ECEF coordinates    ########################################
            ##############################################################
            if element == "'ECEF_X':":
                # [:-1] -> delete comma from the string
                ecef_x = float(my_list[param_counter + 1][:-1])
                if hecef_x != 0:
                    real_ecef_x = (ecef_x+(hecef_x/100))/100
                    print ("DEBUG::: ECEF_X = %f && hECEF_X = %f" % (ecef_x, hecef_x/100))
            elif element == "'hECEF_X':":
                hecef_x = float(my_list[param_counter + 1][:-1])
                if ecef_x != 0:
                    real_ecef_x = (ecef_x+(hecef_x/100))/100
                    print ("DEBUG::: ECEF_X = %f && hECEF_X = %f" % (ecef_x, hecef_x / 100))

            if element == "'ECEF_Y':":
                ecef_y = float(my_list[param_counter + 1][:-1])
                if hecef_y != 0:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100
                    print ("DEBUG::: ECEF_Y = %f && hECEF_Y = %f" % (ecef_y, hecef_y/100))
            elif element == "'hECEF_Y':":
                hecef_y = float(my_list[param_counter + 1][:-1])
                if ecef_y != 0:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100
                    print ("DEBUG::: ECEF_Y = %f && hECEF_Y = %f" % (ecef_y, hecef_y / 100))

            if element == "'ECEF_Z':":
                ecef_z = float(my_list[param_counter + 1][:-1])
                if hecef_z != 0:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100
                    print ("DEBUG::: ECEF_Z = %f && hECEF_Z = %f" % (ecef_z, hecef_z/100))
            elif element == "'hECEF_Z':":
                # [:-1] -> delete symbols at the end of the string
                hecef_z = float(my_list[param_counter + 1][:-4])
                if ecef_z != 0:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100
                    print ("DEBUG::: ECEF_Z = %f && hECEF_Z = %f" % (ecef_z, hecef_z / 100))

            param_counter += 1

        # Write a line of coordinates also if we have only one...
        if real_ecef_x != 0 or real_ecef_y != 0 or real_ecef_z != 0:
            ##############################################################
            # TODO write in file  ########################################
            ##############################################################
            print ("DEBUG::: ECEF Coordinates x = %f m, y = %f m, z = %f m" %
                   (real_ecef_x, real_ecef_y, real_ecef_z))

    elif ty == "NAV-HPPOSLLH":
        my_list = repr(args).split()
        param_counter = 0
        llh_lat = llh_lon = hllh_lat = hllh_lon = 0
        real_llh_lat = real_llh_lon = 0

        for element in my_list:
            if element == "'LAT':":
                llh_lat = float(my_list[param_counter + 1][:-1])
                if hllh_lat != 0:
                    real_llh_lat = llh_lat+(hllh_lat/100)
                    print ("DEBUG::: lat = %f && hlat = %f" % (llh_lat, hllh_lat/100))
            elif element == "'hLAT':":
                hllh_lat = float(my_list[param_counter + 1][:-1])
                if llh_lat != 0:
                    real_llh_lat = llh_lat+(hllh_lat/100)
                    print ("DEBUG::: lat = %f && hlat = %f" % (llh_lat, hllh_lat/100))

            elif element == "'LON':":
                llh_lon = float(my_list[param_counter + 1][:-1])
                if hllh_lon != 0:
                    real_llh_lon = llh_lon+(hllh_lon/100)
                    print ("DEBUG::: lon = %f && hlon = %f" % (llh_lon, hllh_lon/100))
            elif element == "'hLON':":
                hllh_lon = float(my_list[param_counter + 1][:-1])
                if llh_lon != 0:
                    real_llh_lon = llh_lon+(hllh_lon/100)
                    print ("DEBUG::: lon = %f && hlon = %f" % (llh_lon, hllh_lon/100))
            param_counter += 1

        # Write a line of coordinates also if we have only one...
        if real_llh_lat != 0 or real_llh_lon != 0:
            ##############################################################
            # TODO write in file  ########################################
            ##############################################################
            print ("DEBUG::: LLH Coordinates lat = %f deg, lon = %f deg" %
                   (real_llh_lat, real_llh_lon))


def main(argv):

    # Usage
    if len(sys.argv) <= 1:
        print >> sys.stderr, 'Usage python '+sys.argv[0]+ ' [port]'
        # Exit with error code
        sys.exit(1)

    port = argv[0]

    # Register handler Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    t = ubx.Parser(callback, '/dev/' + port)
    t.parsedevice()

    '''
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
    '''


if __name__ == "__main__":
    main(sys.argv[1:])