from rpi_ws281x import * 
import argparse


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
import time
import numpy as np

def getThetafromXZ(x,z):
    #t = np.arctan(x/z)#*abs(z)/z
    angle = np.arctan2(x,z)
    
    angle = np.degrees(angle) % 360.0 
    angle = angle - angle % 5
    if angle == 0: angle = angle + .1 *abs(z)/z
    return angle
    #return t
    
# def getThetafromXZ(x,z):
#     t = np.arctan(x/z)
#     #t = t + ((z<0)*3.1415)
#     t = round(t,1)
#  
#     t = t *180/3.14
#     if z < 0: t = (((360-t) % 360)+90) %360  #=MOD(MOD(360-G24,360)+90,360)
#     t = t - t % 10 
#     return t

PPINK = 'FF1B8D'
SYELLOW = 'FFDA00'
SDISCO = '1BB3FF'
TBLUE = '5ECEF6'
TPINK = 'F8BEC8'

colorList = [SDISCO,SYELLOW,PPINK]
#colorList = ['000000',TBLUE,TPINK,'808080',TPINK,TBLUE]
colorList = ['52A96B','6EFFAF','808080','FF95BF','D8446E']

colorList = list(reversed(colorList))
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def c(strIn):
    return Color(h(strIn[2:4]),h(strIn[0:2]),h(strIn[4:6]))
    
def h(i):
 return int(int(i, 16)/2)

if __name__ == '__main__':

    strip = {}
    strands = len(LED_COUNTS)
    datafilename = "3dfile.csv"
    dfCSV = pd.read_csv(datafilename)
    dfCSV = dfCSV.sort_values('led').set_index('led')
    # color correct     
    d = dfCSV['RLFB12'].to_dict()
    dz = dfCSV['z'].to_dict()
    print(d)
    for strand in range(strands):
        strip[strand] = Adafruit_NeoPixel(LED_COUNTS[strand], LED_PINS[strand], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#         leds = new_ws2811_t()
#         channel = ws2811_channel_get(leds, strand)
#         ws2811_channel_t_strip_type_set(channel, WS2811_STRIP_RGB)
        strip[strand].begin()
#     for strand in range(strands):
#         for item in range( LED_COUNTS[strand]):
#             strip[strand].setPixelColor(item,Color(0,0,0))
#         strip[strand].show()
#     time.sleep(1)
#     for strand in range(strands):
#         for item in range( LED_COUNTS[strand]):
#              strip[strand].setPixelColor(item,c(SDISCO))
#         strip[strand].show()
#     time.sleep(1)
    
    N = len(colorList)
  
    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
     # Up and down   horizontally
    for loop in range(1):
        df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['y'],N)).agg({'led' : list}).reset_index()[['led']]
        l = df1.values
        iMax = len(l)
        sign = -1
        for w in range(100):
          for i in range(N):
            for led in l[i][0]: 
                item = int(led % 250) #1
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,c(colorList[(i+w )% N]))
            strip[0].show()
            strip[1].show() 
          time.sleep(10)  
    time.sleep(3) 
            
      
#     for strand in range(strands):
#         for item in range( LED_COUNTS[strand]):
#             strip[strand].setPixelColor(item,Color(0,0,0))
#         strip[strand].show()
#      # Up and down   horizontally
#     for loop in range(10):
#         df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['x'],N)).agg({'led' : list}).reset_index()[['led']]
#         l = df1.values
#         iMax = len(l)
#         sign = -1
#         for w in range(1):
#           for i in range(N):
#             for led in l[i][0]: 
#                 item = int(led % 250) #1
#                 strand = int(led/250)
#                 #print(led,item,type(item),strand)
#                 strip[strand].setPixelColor(item,c(colorList[i]))
#             strip[0].show()
#             strip[1].show()  
#             time.sleep(.02)  