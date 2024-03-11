#!/usr/bin/python3

###########################################
#
# VOC monitor
# we are using a SGP40 gas sensor
# This is fed from a SHT31D sensor
# 
###########################################


import sys
import os
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from Adafruit_IO import Client, Feed
import json
import datetime

import adafruit_ssd1306  # the display 

from Sensirion_SGP40 import Sensirion_SGP40 # gas sensor
from Sensirion_SHT30 import Sensirion_SHT30 # temp/humidity sensor


######
# Variables
######

LOG_FILE  = '/home/pi/VOC_monitor/VOC_log.txt'
FONT_FILE = '/home/pi/VOC_monitor/PixelOperator.ttf'

i2c = board.I2C()  # uses board.SCL and board.SDA

## IO adafruit setup

# VOC_log.py "USERNAME" "KEY"

#USERNAME = sys.argv[1]
#KEY = sys.argv[2]
#print (sys.argv[1] + " " + sys.argv[2] )
#aio = Client(USERNAME, KEY)


# send it to the AIO feed
#io.send_data(aio.feeds('enviro-humidity').key, humidity)
#io.send_data(aio.feeds('enviro-temp').key, temp)
#io.send_data(aio.feeds('voc-index').key, voc_index)
#io.send_data(aio.feeds('voc-raw').key, voc_raw)
    


import urllib.request, json 
with urllib.request.urlopen("http://voron/server/temperature_store") as url:
    data = json.load(url)
    jsonData = data["result"]

    Bed = data["result"]["heater_bed"]["temperatures"][1199]
    Chamber = data["result"]["temperature_fan chamber"]["temperatures"][1199]
    Extruder = data["result"]["extruder"]["temperatures"][1199]

    ## heater_bed
    ## temperature_sensor Octopus
    ## temperature_sensor raspberry
    ## temperature_fan chamber
    ## extruder

    ## temperatures
    ## targets
    ## powers

## heater_bed : 21.48
## temperature_sensor Octopus : 26.29
## temperature_sensor raspberry : 31.64
## temperature_fan chamber : 21.61
## extruder : 22.12


            
            
            