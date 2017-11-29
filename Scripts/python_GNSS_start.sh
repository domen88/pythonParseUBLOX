#!/usr/bin/env bash

echo "sleep 120 seconds"
sleep 120
cd /home/pi/serverUBLOX/
echo "start serverUblox"
sudo python serverUblox.py ttyACM0
