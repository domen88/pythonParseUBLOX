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
import time
import datetime
import os.path


# Create directory if not exists and open file
timestamp = time.time()
out_file_name = "coordinates_" + \
                datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d') + ".txt"
out_path = "generated/"
if not os.path.exists(out_path):
    os.makedirs(out_path)
if not os.path.exists(out_path + out_file_name):
    out_file = open(out_path + out_file_name, "w")
else:
    out_file = open(out_path + out_file_name, "a")


# Handler Ctrl-C
def signal_handler(signal, frame):
    out_file.close()
    print('\nOutput File Closed')
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
                    # print ("DEBUG::: ECEF_X = %f && hECEF_X = %f" % (ecef_x, hecef_x/100))
            elif element == "'hECEF_X':":
                hecef_x = float(my_list[param_counter + 1][:-1])
                if ecef_x != 0:
                    real_ecef_x = (ecef_x+(hecef_x/100))/100
                    # print ("DEBUG::: ECEF_X = %f && hECEF_X = %f" % (ecef_x, hecef_x / 100))

            if element == "'ECEF_Y':":
                ecef_y = float(my_list[param_counter + 1][:-1])
                if hecef_y != 0:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100
                    # print ("DEBUG::: ECEF_Y = %f && hECEF_Y = %f" % (ecef_y, hecef_y/100))
            elif element == "'hECEF_Y':":
                hecef_y = float(my_list[param_counter + 1][:-1])
                if ecef_y != 0:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100
                    # print ("DEBUG::: ECEF_Y = %f && hECEF_Y = %f" % (ecef_y, hecef_y / 100))

            if element == "'ECEF_Z':":
                ecef_z = float(my_list[param_counter + 1][:-1])
                if hecef_z != 0:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100
                    # print ("DEBUG::: ECEF_Z = %f && hECEF_Z = %f" % (ecef_z, hecef_z/100))
            elif element == "'hECEF_Z':":
                # [:-1] -> delete symbols at the end of the string
                hecef_z = float(my_list[param_counter + 1][:-4])
                if ecef_z != 0:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100
                    # print ("DEBUG::: ECEF_Z = %f && hECEF_Z = %f" % (ecef_z, hecef_z / 100))
            param_counter += 1

        # Write a line of coordinates also if we have only one...
        if real_ecef_x != 0 or real_ecef_y != 0 or real_ecef_z != 0:
            ecef_string = "[%s] ECEF Coordinates x = %f m, y = %f m, z = %f m" % \
                (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                 real_ecef_x, real_ecef_y, real_ecef_z)
            out_file.write(ecef_string + "\n")
            print ecef_string

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
                    # print ("DEBUG::: lat = %f && hlat = %f" % (llh_lat, hllh_lat/100))
            elif element == "'hLAT':":
                hllh_lat = float(my_list[param_counter + 1][:-1])
                if llh_lat != 0:
                    real_llh_lat = llh_lat+(hllh_lat/100)
                    # print ("DEBUG::: lat = %f && hlat = %f" % (llh_lat, hllh_lat/100))

            elif element == "'LON':":
                llh_lon = float(my_list[param_counter + 1][:-1])
                if hllh_lon != 0:
                    real_llh_lon = llh_lon+(hllh_lon/100)
                    # print ("DEBUG::: lon = %f && hlon = %f" % (llh_lon, hllh_lon/100))
            elif element == "'hLON':":
                hllh_lon = float(my_list[param_counter + 1][:-1])
                if llh_lon != 0:
                    real_llh_lon = llh_lon+(hllh_lon/100)
                    # print ("DEBUG::: lon = %f && hlon = %f" % (llh_lon, hllh_lon/100))
            param_counter += 1

        # Write a line of coordinates also if we have only one...
        if real_llh_lat != 0 or real_llh_lon != 0:
            llh_string = "[%s] LLH Coordinates lat = %f deg, lon = %f deg" %\
                (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    real_llh_lat, real_llh_lon)
            out_file.write(llh_string + "\n")
            print llh_string


def main(argv):
    # Usage
    if len(sys.argv) <= 1:
        print >> sys.stderr, 'Usage python ' + sys.argv[0] + ' [port]'
        # Exit with error code
        sys.exit(1)

    port = argv[0]

    # Register handler Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    # Start the parser
    t = ubx.Parser(callback, '/dev/' + port)
    t.parsedevice()

if __name__ == "__main__":
    main(sys.argv[1:])
