from rpi_ws281x import * 
import argparse

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN2 = 12 ## Second strand
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53





import sys
import traceback
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import time

import cv2
from scipy.ndimage import rotate
import pandas as pd

LED_COUNT2 = 100

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

strip2 = Adafruit_NeoPixel(LED_COUNT2, LED_PIN2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip2.begin()

# for i in range(LED_COUNT):
#     print(i)
#     strip.setPixelColor(i,Color(0,128,0) )
#     strip.show()
#     time.sleep(.005)
# 
# for i in range(LED_COUNT2):
#     print(i)
#     if i < 50:
#         strip2.setPixelColor(i,Color(128,0,0) )
#     else: 
#             strip2.setPixelColor(i,Color(9,0,128) )
# 
#     strip2.show()
#     time.sleep(.005)

for i in range(LED_COUNT2):
    print(i)
    if i < 50:
        strip2.setPixelColor(i,Color(128,0,0) )
        strip.setPixelColor(i,Color(0,128,0) )
        strip.show()
        strip2.show()
    else: 
        strip2.setPixelColor(i,Color(0,0,128) )
        strip.setPixelColor(i,Color(128,128,0) )
        strip.show()
        strip2.show()
        
    time.sleep(.1)
