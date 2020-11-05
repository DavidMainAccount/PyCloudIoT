#!/bin/bash

#Upload files
echo -ne 'Puting Files : #                                       (0%)\r'
ampy --port /dev/ttyUSB0 put ../../src/Libraries
echo -ne 'Puting Files : ##################                     (50%)\r'
ampy --port /dev/ttyUSB0 put ../../src/main.py
echo -ne 'Puting Files : ##############################         (80%)\r'
ampy --port /dev/ttyUSB0 put ../../src/Results
echo -ne 'Puting Files : ##################################     (90%)\r'
ampy --port /dev/ttyUSB0 put ../../src/Scripts
echo -ne 'Puting Files : ######################################(100%)\r'
echo -ne '\n'

ampy --port /dev/ttyUSB0 reset
