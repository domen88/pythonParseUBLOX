#!/usr/bin/python

"""
Authors:
    Domenico Scotece
    Michele Solimando

Description:
    From NAV-HPPOSECEF & NAV-HPPOSLLH messages creates a file with rows like this:
        ROW --->    Time    X   Y   Z   Pacc    LAT     LON     HEIGHT      Hacc    Vacc
        UNIT --->   X-Y-Z-xAcc-Height=m; Lat-Lon=deg
"""

import sys
import signal
import ubx
import datetime
import os.path
import logging
from decimal import *
from logging.handlers import TimedRotatingFileHandler


# Handler Ctrl-C
def signal_handler(signal, frame):
    #out_file.close()
    print('\nOutput File Closed')
    print('You pressed Ctrl+C!')
    # TODO: close serial
    # parser.serial.close()
    sys.exit(0)


def callback(logger, ty, *args):
    # these variables have to survive to callback
    global ecef_string, llh_string, ecef_itow, llh_itow, old_time
    # set precision of Decimal
    getcontext().prec = 12

    ##############################################################
    # ECEF coordinates    ########################################
    ##############################################################
    if ty == "NAV-HPPOSECEF":
        ecef_string = ""
        my_list = repr(args).split()    # string split using space (default) delimiter
        param_counter = 0
        ecef_x = ecef_y = ecef_z = hecef_x = hecef_y = hecef_z = pacc = ecef_itow = None
        real_ecef_x = real_ecef_y = real_ecef_z = 0
        for element in my_list:
            if element == "([{'Pacc':":
                pacc = float(my_list[param_counter + 1][:-1])/1000000
            elif element == "'ITOW':":
                # old_time = ecef_itow
                ecef_itow = int(my_list[param_counter + 1][:-1])/1000

            elif element == "'ECEF_X':":
                # [:-1] -> delete comma from the string
                ecef_x = float(my_list[param_counter + 1][:-1])
                if hecef_x is not None:
                    real_ecef_x = (ecef_x+(hecef_x/100))/100
            elif element == "'hECEF_X':":
                hecef_x = float(my_list[param_counter + 1][:-1])
                if ecef_x is not None:
                    real_ecef_x = (ecef_x+(hecef_x/100))/100

            if element == "'ECEF_Y':":
                ecef_y = float(my_list[param_counter + 1][:-1])
                if hecef_y is not None:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100
            elif element == "'hECEF_Y':":
                hecef_y = float(my_list[param_counter + 1][:-1])
                if ecef_y is not None:
                    real_ecef_y = (ecef_y+(hecef_y/100))/100

            if element == "'ECEF_Z':":
                ecef_z = float(my_list[param_counter + 1][:-1])
                if hecef_z is not None:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100
            elif element == "'hECEF_Z':":
                hecef_z = float(my_list[param_counter + 1][:-4])
                if ecef_z is not None:
                    real_ecef_z = (ecef_z+(hecef_z/100))/100

            param_counter += 1

        if real_ecef_x != 0 or real_ecef_y != 0 or real_ecef_z != 0 or pacc != 0:
            ecef_string = "%d %.4f %.4f %.4f %.4f" % (ecef_itow, real_ecef_x, real_ecef_y, real_ecef_z, pacc)
            # print "DEBUG::: ecefStr %s" % ecef_string

    ##############################################################
    # LLH coordinates    #########################################
    ##############################################################
    elif ty == "NAV-HPPOSLLH":
        llh_string = ""
        my_list = repr(args).split()
        param_counter = 0

        # TODO --> not different form 0 but from 'None'
        llh_lat = llh_lon = hllh_lat = hllh_lon = llh_height = hllh_height = hacc = vacc = llh_itow = None
        real_llh_lat = real_llh_lon = real_llh_height = 0

        for element in my_list:
            if element == "'ITOW':":
                # old_time = llh_itow
                llh_itow = int(my_list[param_counter + 1][:-1])/1000
            elif element == "'Hacc':":
                hacc = float(my_list[param_counter + 1][:-4])/1000000
            elif element == "'Vacc':":
                vacc = float(my_list[param_counter + 1][:-1])/1000000

            elif element == "'LAT':":
                llh_lat = float(my_list[param_counter + 1][:-1])
                if hllh_lat is not None:
                    real_llh_lat = Decimal(llh_lat + (hllh_lat / 100)) / Decimal(10000000)
            elif element == "'hLAT':":
                hllh_lat = float(my_list[param_counter + 1][:-1])
                if llh_lat is not None:
                    real_llh_lat = Decimal(llh_lat + (hllh_lat / 100)) / Decimal(10000000)

            elif element == "'LON':":
                llh_lon = float(my_list[param_counter + 1][:-1])
                if hllh_lon is not None:
                    real_llh_lon = Decimal(llh_lon+(hllh_lon/100)) / Decimal(10000000)
            elif element == "'hLON':":
                hllh_lon = float(my_list[param_counter + 1][:-1])
                if llh_lon is not None:
                    real_llh_lon = Decimal(llh_lon+(hllh_lon/100)) / Decimal(10000000)

            elif element == "'HEIGHT':":
                llh_height = float(my_list[param_counter + 1][:-1])
                if hllh_height is not None:
                    real_llh_height = (llh_height+(hllh_height/10))/1000
            elif element == "'hHEIGHT':":
                hllh_height = float(my_list[param_counter + 1][:-1])
                if llh_height is not None:
                    real_llh_height = (llh_height+(hllh_height/10))/1000

            param_counter += 1

        if real_llh_lat != 0 or real_llh_lon != 0:
            llh_string = "%.10f %.10f %.4f %.4f %.4f" % (real_llh_lat, real_llh_lon, real_llh_height, hacc, vacc)
            # print "DEBUG::: llhStr %s" % llh_itow + " " + llh_string

    # write on file
    if llh_itow == ecef_itow:
        # if it is the first time OR it is a new timestamp
        if old_time == 0 or old_time != llh_itow:
            old_time = llh_itow
            write_line_on_file(ecef_string, llh_string, logger)


def write_line_on_file(string_ecef, string_llh, logger):
    # Write a line on file --> TIME X Y Z pAcc Lat Lon Height hAcc vAcc
    if string_ecef != "" and string_llh != "":
        logger.debug(ecef_string+" "+llh_string)
        # out_file.write(ecef_string+" "+llh_string+"\n")
        # print "DEBUG ::: ECEF " + string_ecef + " LLH " + str(time_llh) + " " + string_llh


def main(argv):
    # Usage
    if len(sys.argv) <= 1:
        print >> sys.stderr, 'Usage python ' + sys.argv[0] + ' [port]'
        # Exit with error code
        sys.exit(1)

    port = argv[0]

    #Create logging file and logger
    out_path = "generated/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # get the root logger
    logger = logging.getLogger()
    # set overall level to debug, default is warning for root logger
    logger.setLevel(logging.DEBUG)

    log_file = "generated/coordinates"

    # setup logging to file, rotating at midnight
    filelog = logging.handlers.TimedRotatingFileHandler(log_file,
                                                        when='midnight', interval=1, backupCount=0, utc=True)
    filelog.setLevel(logging.DEBUG)
    logger.addHandler(filelog)

    # setup logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


    '''logger = logging.getLogger("Coordinates Log")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(log_file, when="m",interval=1,backupCount=0, utc=True)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)'''



    # Create directory if not exists and open file
    # TODO send CTRL-C to this script at midnight and create a new file (from bash)
    '''global out_file
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
        out_file.write("\n")
    print "Script started...\nFile Opened...\nStarting parser...."
    '''

    # Assignment at the start
    global ecef_string, llh_string, ecef_itow, llh_itow, old_time
    ecef_string = llh_string = ""
    ecef_itow = llh_itow = old_time = 0

    # Register handler Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    # Start the parser
    t = ubx.Parser(callback, '/dev/' + port, logger=logger)
    print "Parser Started...\n"
    t.parsedevice()


if __name__ == "__main__":
    main(sys.argv[1:])