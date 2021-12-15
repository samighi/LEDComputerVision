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


    
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


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
    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
    time.sleep(1)
    


    dColor = {'LF1': Color(128,0,0), 'LF2': Color(0,128,0), 'RF1': Color(0,0,128),'RF2': Color(128,128,128) ,
        'LB1': Color(128,128,0), 'LB2': Color(128,0,128) 
               ,'RB1': Color(33,33,128), 'RB2': Color(128,33,33)   
               #, 'ZF1': Color(0,255,0), 'ZF2': Color(0,255,0), 'ZB1': Color(0,255,0), 'ZB2': Color(0,255,0)   
                       }

    #for FACE in ['R','F','1']:
    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
    #if True:
     #i = 0

    Colors = {}
    lastcolor = Color(0,0,0)
    lastpos = "RF1"
    for strand in range(strands):
        #time.sleep(1)
        for item in range( LED_COUNTS[strand]):
           
            #try:
            i = item  + 250 * strand
            #if i > 160 or i < 153: continue
            if i in d:
                #if d[i] != "LF2": continue
                if d[i] in dColor: 
                 c = dColor[d[i]]
                else: 
                  c = Color(0,0,0)
                  c = lastcolor
                  d[i] = lastpos
                  print(i,"Z not exists",d[i])#,dfCSV.iloc[i])
            else: 
             # c = Color(255,255,255)
              c = lastcolor
              d[i] = lastpos
            if True:
                #if i<15 or (i>245 and i<265) or (i>480): continue 

                print(i,d[i],c)

                strip[strand].setPixelColor(item,c)
                lastcolor = c
                lastpos = d[i]
                Colors[i] = c 
                #print(i,strand,item,d[i])

        strip[strand].show()
        print(d)
        
        prev = ""
        k1,k2 = 0,0 
        for k,v in sorted(d.items()):
          print(k1,k2,k)
          if d[k] == d[k2] and d[k1] != d[k]:
            
             print("error correction", d[k],d[k2],d[k1])
             d[k1] = d[k]
          k2 = k1
          k1 = k 
    time.sleep(5)
    Colors = {}
    lastcolor = Color(0,0,0)
    lastpos = "RF1"
    for strand in range(strands):
        #time.sleep(1)
        for item in range( LED_COUNTS[strand]):
           
            #try:
            i = item  + 250 * strand
            #if i > 160 or i < 153: continue
            if i in d:
                #if d[i] != "LF2": continue
                if d[i] in dColor: 
                 c = dColor[d[i]]
                else: 
                  c = Color(0,0,0)
                  # c = lastcolor
#                   d[i] = lastpos
                  print(i,"Z not exists",d[i])#,dfCSV.iloc[i])
            else: 
              c = Color(255,255,255)
             #  c = lastcolor
#               d[i] = lastpos
            if True:
                #if i<15 or (i>245 and i<265) or (i>480): continue 

                print(i,d[i],c)

                strip[strand].setPixelColor(item,c)
                lastcolor = c
                lastpos = d[i]
                Colors[i] = c 
                #print(i,strand,item,d[i])

        strip[strand].show()
        print(d)
