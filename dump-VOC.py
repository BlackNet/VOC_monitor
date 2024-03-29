#!/usr/bin/python3

###########################################
#
# VOC monitor
# we are using a SGP40 gas sensor
# This is fed from a SHT31D sensor
# 
###########################################

###########################################
# ::Python modules needed
#	pillow
#	smbus
#	gpiod
#	Adafruit-Blinka
#	Adafruit-SSD1306
#	adafruit-circuitpython-bme280
#	adafruit-io




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

# gather data from sensors
sht30=Sensirion_SHT30()
sht30.sht30_read()
#set IICbus elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
sgp40=Sensirion_SGP40(bus = 1, relative_humidity = sht30.humidity, temperature_c = sht30.temperature)
sgp40.set_envparams(sht30.humidity, sht30.temperature)

#set Warm-up time
#print('Please wait 5 seconds...')
sgp40.begin(5)

# process it
voc_index = int(sgp40.get_voc_index())
voc_raw = int(sgp40.measure_raw())
temp = float(sht30.temperature)
humidity = float(sht30.humidity)    
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

entry = now+" T:%2.2fC, H:%2.2f, I:%3.0d, R:%5.0d" % (temp, humidity, voc_index, voc_raw)
print (entry)
    
# write to the log file
#file = open(LOG_FILE, "a")
#file.write (entry+"\n")
#file.close ()

# send it to the AIO feed
#aio.send_data(aio.feeds('enviro-humidity').key, humidity)
#aio.send_data(aio.feeds('enviro-temp').key, temp)
#aio.send_data(aio.feeds('voc-index').key, voc_index)
#aio.send_data(aio.feeds('voc-raw').key, voc_raw)
    


##### display section
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display settings
WIDTH = 128
HEIGHT = 64  
BORDER = 0

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Load font for the display
font = ImageFont.truetype(FONT_FILE, 40)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# set the voc index to the display, dont care about temp/humidity.
text = "VOC: " + str(voc_index)
(font_width) = oled.width #font.getlength(text)
(font_height)= oled.height - 30 #font.getlength(text)

draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - (font_height + font_height//2) // 2),
    text,
    font=font,
    fill=255,
)

# Display image
oled.image(image)
oled.show()

 
    