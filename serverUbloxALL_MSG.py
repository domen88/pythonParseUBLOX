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
    logger.debug(ty + " " + str(args))


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

    log_file = "generated/coordinatesALL"

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
