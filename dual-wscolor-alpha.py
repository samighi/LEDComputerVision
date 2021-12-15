from rpi_ws281x import * 
import argparse

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


LED_COUNTS      = [150,150]    # Number of LED pixels.
#LED_COUNTS      = [50,50]    # Number of LED pixels.
#LED_PINS       = [12,21]     # GPIO pin connected to the pixels (18 uses PWM!).
LED_PINS       = [21,12]     # GPIO pin connected to the pixels (18 uses PWM!).


import sys
import traceback
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

import cv2
from scipy.ndimage import rotate
import pandas as pd

        
# Simple test for NeoPixels on Raspberry Pi 
import time 
#import board 
#import neopixel

import os.path
from os import path
import cProfile
from picamera import PiCamera

ALL =[ ['00000000','00111100','01100110','01100110','01111110','01100110','01100110','01100110']
,['01111000','01001000','01001000','01110000','01001000','01000100','01000100','01111100']
,['00000000','00011110','00100000','01000000','01000000','01000000','00100000','00011110']
,['00000000','00111000','00100100','00100010','00100010','00100100','00111000','00000000']
,['00000000','00111100','00100000','00111000','00100000','00100000','00111100','00000000']
,['00000000','00111100','00100000','00111000','00100000','00100000','00100000','00000000']
,['00000000','00111110','00100000','00100000','00101110','00100010','00111110','00000000']
,['00000000','00100100','00100100','00111100','00100100','00100100','00100100','00000000']
,['00000000','00111000','00010000','00010000','00010000','00010000','00111000','00000000']
,['00000000','00011100','00001000','00001000','00001000','00101000','00111000','00000000']
,['00000000','00100100','00101000','00110000','00101000','00100100','00100100','00000000']
,['00000000','00100000','00100000','00100000','00100000','00100000','00111100','00000000']
,['00000000','00000000','01000100','10101010','10010010','10000010','10000010','00000000']
,['00000000','00100010','00110010','00101010','00100110','00100010','00000000','00000000']
,['00000000','00111100','01000010','01000010','01000010','01000010','00111100','00000000']
,['00000000','00111000','00100100','00100100','00111000','00100000','00100000','00000000']
,['00000000','00111100','01000010','01000010','01000010','01000110','00111110','00000001']
,['00000000','00111000','00100100','00100100','00111000','00100100','00100100','00000000']
,['00000000','00111100','00100000','00111100','00000100','00000100','00111100','00000000']
,['00000000','01111100','00010000','00010000','00010000','00010000','00010000','00000000']
,['00000000','01000010','01000010','01000010','01000010','00100100','00011000','00000000']
,['00000000','00100010','00100010','00100010','00010100','00010100','00001000','00000000']
,['00000000','10000010','10010010','01010100','01010100','00101000','00000000','00000000']
,['00000000','01000010','00100100','00011000','00011000','00100100','01000010','00000000']
,['00000000','01000100','00101000','00010000','00010000','00010000','00010000','00000000']
,['00000000','00111100','00000100','00001000','00010000','00100000','00111100','00000000']]

ALLLETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def readImage(name):
    try: 
    #if True:
        file = name
        img = cv2.imread(file)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        blurred = cv2.GaussianBlur(gray, (11,11), 0)

        thresh = cv2.threshold(blurred, 195, 255, cv2.THRESH_BINARY)[1]

        #Detecting multiple bright spots in an image with Python and OpenCV
        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        #thresh = cv2.erode(thresh, None, iterations=2) ## removed this (Saman) since it seemed to misidentify the LEDs 
        thresh = cv2.dilate(thresh, None, iterations=4)

        #Detecting multiple bright spots in an image with Python and OpenCV
        # perform a connected component analysis on the thresholded
        # image, then initialize a mask to store only the "large"
        # components
        labels = measure.label(thresh, connectivity = 2 , background=0) #,neighbors=4 ## deprecated
        mask = np.zeros(thresh.shape, dtype="uint8")
        # loop over the unique components
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue
            # otherwise, construct the label mask and count the
            # number of pixels 
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
            # if the number of pixels in the component is sufficiently
            # large, then add it to our mask of "large blobs"
            if numPixels > 300:
                mask = cv2.add(mask, labelMask)


        image = img 
        #Detecting multiple bright spots in an image with Python and OpenCV
        # find the contours in the mask, then sort them from left to
        # right
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = contours.sort_contours(cnts)[0]
        # loop over the contours
        for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            #print(cX,cY)
           
            cv2.circle(image, (int(cX), int(cY)), int(radius),
                (0, 0, 255), 3)
            cv2.putText(image, "{}".format(i + 1), (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        
        # show the output image
        #cv2.imshow("Image", image)
        #l.append((cX,cY))
        return (cX,cY)
    except:
    #else:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        cX,cY = -1,-1
        print(cX,cY)
        return (cX,cY)

 
def takePicture(pixelnumber,name,strand,num_pixels):
    j = pixelnumber
    global camera
    #pixels.fill((0, 0, 0))
    for item in range(num_pixels):
        strip[strand].setPixelColor(item,0)
    i = j 

    r,g,b= (255,255,255)
    strip[strand].setPixelColor(i,Color(r,g,b))
    strip[strand].show()
   
    camera.capture(name)
   # time.sleep(.5)
    r,g,b= (0,0,0)
    strip[strand].setPixelColor(i,Color(r,g,b))
    strip[strand].show()
       
       
def alignPixels(datafilename,strand,num_pixels):

    
    
    
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 
    # NeoPixels must be connected to D10, D12, D18 or D21 to work. 

 
    l = []
    
    if not path.exists(datafilename):
     if True:
        for j in range(num_pixels):
            print(j," ",end="")
            filename = "../image"+str(strand)+"-"+str(j)+".jpg"
     
            if not path.exists(filename):
                  takePicture(j,filename,strand,num_pixels)
            l.append(readImage(filename))
            if l[-1][0] == -1: print(filename)
            #print(l)
            sys.stdout.flush()
    
        l1 = [(xy[0],xy[1],i,strand) for i,xy in enumerate(l) if xy[0] != -1]
        l2 =  [(xy[1],xy[0],i,strand) for i,xy in  enumerate(l) if xy[0] != -1]    
        pd.DataFrame(l1).to_csv(datafilename+str(strand),index=False)
        print("Wrote "+str(len(l1))+" Records.")

def walkStrands():
  global strip
  
  for i in range(LED_COUNTS[0]):
    print(i)
    if i < 50:
        strip[0].setPixelColor(i,Color(255,255,255) )
        strip[1].setPixelColor(i,Color(255,255,255) )
        strip[1].show()
        strip[0].show()
    else: 
        strip[0].setPixelColor(i,Color(255,255,255) )
        strip[1].setPixelColor(i,Color(255,255,255) )
        strip[1].show()
        strip[0].show()
        
    time.sleep(.01)

def wsshowLines(datafilename):
    global num_pixels,strip
     
    XFACTOR = 20
    df = pd.read_csv(datafilename+"0")
    df2 = pd.read_csv(datafilename+"1")
    df = pd.concat([df,df2])
    df = df[df["1"] < 600] ### HACK

    print(df)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2],x[3]) for x in df.values]

    ord = False
    strands = len(LED_COUNTS)

    for times in range(5):
        print("HERE")
        for ordered in ([x for x in sorted(l1,reverse=False)],[x for x in sorted(l1,reverse=True)],[x for x in sorted(l2,reverse=False)],[x for x in sorted(l2,reverse=True)]):

         #pixels.fill((0, 0, 0))
         for strand in range(strands):
          for item in range(LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,0)
 

         imin,imax = min([x[0] for x in ordered]),max([x[0] for x in ordered])
         rangevalues = range(int(imin),int(imax),int((int(imax)-int(imin))/XFACTOR))
         if ord == True: 
            rangevalues = range(int(imax),int(imin),-int((int(imax)-int(imin))/XFACTOR))
            ord = False
         else:
            ord = True
         lit = []
         for i in rangevalues:
           #print(0)
           vmax = ((int(imax)-int(imin))/XFACTOR) * 0.55
           vmax = ((int(imax)-int(imin))/XFACTOR) * 0.30
           #print(imin,imax,i) 
           for item in lit:
              #print(item)
              v = int(ordered[item][2])
              strand = ordered[item][3]
              #pixels[int(] = (0,0,0)
              strip[strand].setPixelColor(v,Color(0,0,0))
           lit = []

              
           #pixels.fill((0, 0, 0))
           #pixels.show() 
           for j in range(len(ordered)):  
               if abs(ordered[j][0] - i) < vmax: 
                   lit.append(j)
                   v = int(ordered[j][2])
                   strand = ordered[j][3]
                   #pixels[v] = (255,255,255)
                   if strand == 0: 
                       strip[strand].setPixelColor(v,Color(255,255,255))
                   else:
                       strip[strand].setPixelColor(v,Color(255,255,255))
               #else:
                  #  v = int(ordered[j][2])
#                    pixels[v] = (0,0,0)
           #print(lit)
          # print(1)
           #pixels.show() 
           for strand in range(strands):
            strip[strand].show()
           #print(2)
           time.sleep(.1)


def lineDistance(x0,y0,x1,y1,x2,y2):
   rc = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / np.sqrt(np.square(x2-x1) + np.square(y2-y1))
   return rc
       
def wsshowWaveLines(datafilename):
    global num_pixels
     
    XFACTOR = 20

    df = pd.read_csv(datafilename+"0")
    df2 = pd.read_csv(datafilename+"1")
    df = pd.concat([df,df2])
    df = df[df["1"] < 600] ### HACK
    print(df)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2],x[3]) for x in df.values]

    ord = False
    for ordered in [l1,l2]:
     for times in range(10):
        #for ordered in ([x for x in sorted(l1,reverse=False)],[x for x in sorted(l1,reverse=True)],[x for x in sorted(l2,reverse=False)],[x for x in sorted(l2,reverse=True)]):
       
        # pixels.fill((0, 0, 0))
         for strand in range(strands):

          for item in range(LED_COUNTS[strand]):
            strip[strand].setPixelColor(item,Color(0,0,0))


         imin,imax = min([x[0] for x in ordered]),max([x[0] for x in ordered])
         jmin,jmax = min([x[1] for x in ordered]),max([x[1] for x in ordered])

         x,y = {},{}
         ## Fixed point
         #print(ordered)
         print(imin,imax,jmin,jmax)
        
         rangevalues = range(int(imin),int(imax),int((int(imax)-int(imin))/XFACTOR))
         if ord == True: 
            rangevalues = range(int(imax),int(imin),-int((int(imax)-int(imin))/XFACTOR))
            ord = False
         else:
            ord = True
         lit = []
         for i in rangevalues:
           x[1] = int(abs((imax+imin)/2))
           y[1] = jmin
           # other side -- then i is the moving x[1]
           x[2] = i
           y[2] = jmax
           
           
           vmax = ((int(imax)-int(imin))/XFACTOR) * 0.55
           
           #print(imin,imax,i) 
           for item in lit:
              #print(item)
              #pixels[int(ordered[item][2])] = (0,0,0)
              strand = ordered[item][3]
              strip[strand].setPixelColor(int(ordered[item][2]),Color(0,0,0))
           lit = []

              
           #pixels.fill((0, 0, 0))
           #pixels.show() 
           for j in range(len(ordered)):  
               x[0] = ordered[j][0] ## X POINT of the pixel
               y[0] = ordered[j][1] ## Y POINT of the pixel
              
               distance = lineDistance(x[0],y[0],x[1],y[1],x[2],y[2])

               if abs(distance) < vmax: 
                   lit.append(j)
                   v = int(ordered[j][2])
                   strand = ordered[j][3]
                   strip[strand].setPixelColor(v,Color(255,255,255))

           for strand in range(strands):
            strip[0].show()
           #print(2)
           #time.sleep(.02)
           
def wsShowLetters(datafilename):
    for i,letter in enumerate(ALLLETTERS):
      print(letter,ALL[i])
      
    global num_pixels,strip
     
    XFACTOR = 20
    df = pd.read_csv(datafilename+"0")
    df2 = pd.read_csv(datafilename+"1")
    df = pd.concat([df,df2])
    df = df[df["1"] < 600] ### HACK

    print(df)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2],x[3]) for x in df.values]
           
           
def clearStrand():
    global strip
    for strand in range(strands):
      for item in range(LED_COUNTS[strand]):
        strip[strand].setPixelColor(item,0)
      strip[strand].show()
            

        
def main():
    global  num_pixels,pixels
    
 
    datafilename = "dualorderednew.csv"
    strands = len(LED_COUNTS)
    
#    walkStrands()
    clearStrand()

#     for strand in range(strands):
#       
#       alignPixels(datafilename,strand,LED_COUNTS[strand])
    clearStrand()

        
    #wsshowLines(datafilename)
    wsShowLetters(datafilename)
    clearStrand()

#     wsshowWaveLines(datafilename)
#     clearStrand()

    



if __name__ == '__main__':

    strip = {}
    strands = len(LED_COUNTS)
    camera = PiCamera()
    for strand in range(strands):
        strip[strand] = Adafruit_NeoPixel(LED_COUNTS[strand], LED_PINS[strand], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        strip[strand].begin()
        for item in range( LED_PINS[strand]):
            strip[strand].setPixelColor(item,0)
        strip[strand].show()

    cProfile.run('main()')

    
    
