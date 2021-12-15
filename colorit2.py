from rpi_ws281x import * 
import argparse
import time

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


LED_COUNTS      = [250,250]    # Number of LED pixels.
#LED_COUNTS      = [50,50]    # Number of LED pixels.
#LED_PINS       = [12,21]     # GPIO pin connected to the pixels (18 uses PWM!).
LED_PINS       = [21,12]     # GPIO pin connected to the pixels (18 uses PWM!).

import pandas as pd 

def main():
    global  num_pixels,pixels
    
 
    datafilename = "do.csv"
    strands = len(LED_COUNTS)
    

    
import numpy as np


if __name__ == '__main__':

    strip = {}
    strands = len(LED_COUNTS)
    datafilename = "do.csv"
    dColor = {'RF': Color(0,100,0),"FR" : Color(100,0,0),"R" : Color(0,100,0) ,"RB" : Color(0,0,100) 
    , "F" : Color(100,0,0)
     ,"FL" : Color(0,0,100)
      ,"LF" : Color(0,0,100)
       ,"L" : Color(100,100,100)
       ,"BL" : Color(100,100,0)
       ,"B" : Color(0,100,100)
     }
    d = dict(pd.read_csv(datafilename).values)
    
    i = 0
    for strand in range(strands):
        strip[strand] = Adafruit_NeoPixel(LED_COUNTS[strand], LED_PINS[strand], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        strip[strand].begin()
        
    #dColor = {'xx': Color(0,0,0), 'Fx': Color(0,0,0), 'FR': Color(30,30,30), 'BR': Color(0,0,30), 'BL': Color(30,0,0), 'FL': Color(30,0,0)}
    #dColor = {'nan' : Color(0,0,0),'xx': Color(0,0,0), 'Fx': Color(0,0,0), 'RF': Color(30,30,30),'F': Color(0,100,0),'L': Color(255,0,0), 'RB': Color(0,0,100), 'BL': Color(100,0,0), 'FL': Color(100,0,0)}

    print("Starting") 
    while True:
     for s in ["L","R","F","B"]:
         print(s)
         i = 0
         for strand in range(strands):
            for item in range(LED_COUNTS[strand]):
                strip[strand].setPixelColor(item,Color(0,0,0))
                
                #try:
                if i in d and np.nan != d[i] and (s in str(d[i])):
                   try:
                    strip[strand].setPixelColor(item,dColor[d[i]])
                    #print(i,strand,item,d[i])
                   except:
                     #print(">>",i,strand,item,d[i])
                     strip[strand].setPixelColor(item,Color(0,0,0))
                #except:
                #  strip[strand].setPixelColor(item,Color(0,0,0))
    #              pass
                i = i + 1
                #strip[strand].setPixelColor(item,Color(0,0,0))
            strip[strand].show()
         time.sleep(10)
