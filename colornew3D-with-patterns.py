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
    
# 15A5E1
# FFE500
# 00A40A
# 900048
# 390080
# FF9050
# 282828
# FF1D00


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
                r = int(c / 256 / 256)
                g = int((c - r * 256 * 256) /256)
                b = int(c % 256)
                c = Color(g,r,b)
                strip[strand].setPixelColor(item,c)
                lastcolor = c
                lastpos = d[i]
                Colors[i] = c 
                #print(i,strand,item,d[i])

    strip[0].show()
    strip[1].show()

    dfCSV.reset_index().groupby(pd.cut(dfCSV['y'],30)).agg({'led' : list})
    time.sleep(1)

    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
     # Up and down   horizontally
    for loop in range(10):
        df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['y'],30)).agg({'led' : list}).reset_index()[['led']]
        l = df1.values
        iMax = len(l)
        sign = -1
        for w in range(3):
         for r in [range(len(l)),range(len(l)-1,0,-1)]:
          sign = sign * -1
          for i in r:
            i1,i2 = (i-(sign*1)+iMax) % iMax ,(i-(sign*2)+iMax) % iMax
           #  print(i,i1,i2)
    #         print(l[i][0])
            for led in l[i][0]: 
                item = int(led % 250) #1
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(128,128,128))
            for led in l[i1][0]: 
                item = int(led % 250) #2
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(64,64,64))
            for led in l[i2][0]: 
                item = int(led % 250) #3
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(0,0,0))
            strip[0].show()
            strip[1].show()  
            time.sleep(.02)
         
        # around Theta / Angle vertically  
        dfCSV['t'] = dfCSV[['x','z']].apply(lambda x: getThetafromXZ(x[0],x[1]),axis=1)
        #dfCSV['t'] =  (dfCSV['t']+max( dfCSV['t']))*abs(dfCSV['x'])/dfCSV['x']
        
        df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['t'],40)).agg({'led' : list}).reset_index()[['led']]
        l = df1.values 
        # l = [led for led in l if not (i<15 or (i>245 and i<265) or (i>480)) ]
        iMax = len(l)
        print(l)
        sign = 1
        for w in range(3):
         for r in [range(len(l))]:#,range(len(l)-1,0,-1)]:
          #sign = sign * -1
          for i in r:
            i1,i2 = (i-(sign*1)+iMax) % iMax ,(i-(sign*2)+iMax) % iMax
           #  print(i,i1,i2)
    #         print(l[i][0])
            if True:
                if l[i][0] == None: l[i][0] = []
                for led in l[i][0]: 
                    print(led,dfCSV.loc[led][['x','z','t']].values)
                    item = int(led % 250) #1
                    strand = int(led/250)
                    #print(led,item,type(item),strand)
                    strip[strand].setPixelColor(item,Color(0,128,0))
                for led in l[i1][0]: 
                    item = int(led % 250) #2
                    strand = int(led/250)
                    #print(led,item,type(item),strand)
                    strip[strand].setPixelColor(item,Color(128,0,0))
                for led in l[i2][0]: 
                    item = int(led % 250) #3
                    strand = int(led/250)
                    #print(led,item,type(item),strand)
                    strip[strand].setPixelColor(item,Color(0,0,0))

            strip[0].show()
            strip[1].show()
            time.sleep(.04)
         print("")
         print("")
         

         for led in l[i][0]: 
            item = int(led % 250) #1
            strand = int(led/250)
            #print(led,item,type(item),strand)
            strip[strand].setPixelColor(item,Color(0,0,0))
         for led in l[i1][0]: 
            item = int(led % 250) #2
            strand = int(led/250)
            #print(led,item,type(item),strand)
            strip[strand].setPixelColor(item,Color(0,0,0))
       
        df1 = dfCSV.reset_index().sort_values('t').groupby(pd.cut(dfCSV['y'],40)).agg({'led' : list}).reset_index()[['led']]#.fillna([0])
        l1 = df1.values
        df1 = dfCSV.reset_index().sort_values('y').groupby(pd.cut(dfCSV['t'],40)).agg({'led' : list}).reset_index()[['led']]#.fillna([0])
        l2 = df1.values
        print( l1,l2 )   
        l1 = [x for x in l1 if x[0] is not None]
        l2 = [x for x in l2 if x[0] is not None]    
        dL1 = { y : i for i,x in enumerate(l1) for y in x[0] if y is not  None}
        dL2 = { y : i for i,x in enumerate(l2) for y in x[0] if y is not  None  }
        lLEDs = []
        for led in range(500):
            try:
             x,y = dL1[led],dL2[led]
             #print(led,x,y)
             lLEDs.append([x,y,led])
            except:
              #print("Bad LED",led)
              pass
        l = pd.DataFrame(lLEDs).groupby([0,1]).agg({2: list}).values
        iMax = len(l)
        sign = -1
        for w in range(0):
          lNew = [y for x in l for y in x[0]]
          iMax = len(lNew)
          N = 5
          for i in range(1,iMax):
            #print(i)
            snake = lNew[i:i+N]
            #print(snake)
            blist = [(snake[0],Color(0,255,0))]+[(led,Color(255-b*6,255-b*6,255-b*30)) for b,led in enumerate(snake[1:])]
           
            for led,b in blist: 
              #  print(b,led,item,strand)
                item = int(led % 250) 
                strand = int(led/250)
                c = b
               # print(b,led,item,strand)

                strip[strand].setPixelColor(item,c)

            led = lNew[i-1]
            item = int(led % 250) 
            strand = int(led/250)
            c = Color(0,0,0)
            strip[strand].setPixelColor(item,c)
            strip[0].show()
            strip[1].show() 
            
            time.sleep(.02)
            
            
    #### f

    dfCSV.reset_index().groupby(pd.cut(dfCSV['x'],30)).agg({'led' : list})
    time.sleep(1)

    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
     # Up and down   horizontally
    for loop in range(10):
        df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['x'],30)).agg({'led' : list}).reset_index()[['led']]
        l = df1.values
        iMax = len(l)
        sign = -1
        for w in range(3):
         for r in [range(len(l)),range(len(l)-1,0,-1)]:
          sign = sign * -1
          for i in r:
            i1,i2 = (i-(sign*1)+iMax) % iMax ,(i-(sign*2)+iMax) % iMax
           #  print(i,i1,i2)
    #         print(l[i][0])
            for led in l[i][0]: 
                item = int(led % 250) #1
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(128,128,128))
            for led in l[i1][0]: 
                item = int(led % 250) #2
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(64,64,64))
            for led in l[i2][0]: 
                item = int(led % 250) #3
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(0,0,0))
            strip[0].show()
            strip[1].show()  
            time.sleep(.02)
         
        # around Theta / Angle vertically  
        dfCSV['t'] = dfCSV[['x','z']].apply(lambda x: getThetafromXZ(x[0],x[1]),axis=1)
        #dfCSV['t'] =  (dfCSV['t']+max( dfCSV['t']))*abs(dfCSV['x'])/dfCSV['x']
 
    #### f

    dfCSV.reset_index().groupby(pd.cut(dfCSV['z'],30)).agg({'led' : list})
    time.sleep(1)

    for strand in range(strands):
        for item in range( LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))
        strip[strand].show()
     # Up and down   horizontally
    for loop in range(10):
        df1 = dfCSV.reset_index().groupby(pd.cut(dfCSV['z'],30)).agg({'led' : list}).reset_index()[['led']]
        l = df1.values
        iMax = len(l)
        sign = -1
        for w in range(3):
         for r in [range(len(l)),range(len(l)-1,0,-1)]:
          sign = sign * -1
          for i in r:
            i1,i2 = (i-(sign*1)+iMax) % iMax ,(i-(sign*2)+iMax) % iMax
           #  print(i,i1,i2)
    #         print(l[i][0])
            for led in l[i][0]: 
                item = int(led % 250) #1
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(128,128,128))
            for led in l[i1][0]: 
                item = int(led % 250) #2
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(64,64,64))
            for led in l[i2][0]: 
                item = int(led % 250) #3
                strand = int(led/250)
                #print(led,item,type(item),strand)
                strip[strand].setPixelColor(item,Color(0,0,0))
            strip[0].show()
            strip[1].show()  
            time.sleep(.02)
         
        # around Theta / Angle vertically  
        dfCSV['t'] = dfCSV[['x','z']].apply(lambda x: getThetafromXZ(x[0],x[1]),axis=1)
        #dfCSV['t'] =  (dfCSV['t']+max( dfCSV['t']))*abs(dfCSV['x'])/dfCSV['x']
 
 
        

## END OF NOTEBOOK 

#        for r in [range(len(l)),range(len(l)-1,0,-1)]:
#           snake = []
#           sign = sign * -1
#           for i in r:
#            #  print(i,i1,i2)
#     #         print(l[i][0])
#             for led in l[i][0]: 
#                 item = int(led % 250) #1
#                 strand = int(led/250)
#                 #print(led,item,type(item),strand)
#                 strip[strand].setPixelColor(item,Color(255,255,255))
#                 snake.append(led)
#                 for j,ledx in enumerate(reversed(snake)):
#                     item = int(ledx % 250) #1
#                     strand = int(ledx/250)
#                     #print(i,led,item,strand)
#                     c = strip[strand].getPixelColor(item)
#                     #print(c)
#                     N = 10
#                     r = int(int(c / 256 / 256 )) 
#                     #print("R = ",r,c)
#                     g = int(int((c - (r  * 256 * 256)) /256 )-N)
#                     r = int(r -N) 
#                     #print("G = ",g,r,c)
#                     b = int(int((c % 256 ))-N)
#                     #print("B = ",b,g,r,c)
#                     c = Color(g,r,b)
#                     #print(item,g,r,b, c)
#                     if j > 10:
#                       c = Color(0,0,0)
#                     strip[strand].setPixelColor(item,c)
#                 ## turn off others 
#                 
#                 snake = snake[-10:]
#                 strip[0].show()
#                 strip[1].show()  
#             #time.sleep(.01)
#                 
#            #  for led in l[i1][0]: 
# #                 item = int(led % 250) #2
# #                 strand = int(led/250)
# #                 #print(led,item,type(item),strand)
# #                 strip[strand].setPixelColor(item,Color(64,64,64))
# #             for led in l[i2][0]: 
# #                 item = int(led % 250) #3
# #                 strand = int(led/250)
# #                 #print(led,item,type(item),strand)
# #                 strip[strand].setPixelColor(item,Color(0,0,0))
#             strip[0].show()
#             strip[1].show()  
#             #time.sleep(.01)
          
