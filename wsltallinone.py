from rpi_ws281x import * 
import argparse

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.setPixelColor(10,Color(255,255,255))
strip.show()
strip.setPixelColor(20,Color(255,255,255))
strip.show()


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
import board 
import neopixel

import os.path
from os import path
import cProfile
from picamera import PiCamera


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

 
def takePicture(pixelnumber,name):
    j = pixelnumber
    #RGB = [[(255,0,0),(255,0,0),(255,0,0)],[(0,0,255),(0,255,0),(255,0,0)], [(255,0,0),(0,0,255),(0,255,0)], [(0,255,0),(255,0,0),(0,0,255)]]
    pixels.fill((0, 0, 0))
    #for j in range(len(RGB)):
    #for j in range(num_pixels):
    #print(j," ",end="")
#  for i in range(0,num_pixels-2-j,3):
    i = j 
    pixels.fill((0, 0, 0))
    r,g,b= (255,255,255)
#        if i == 0: 
#       else: 
    if True:
        #pixels[i-1] = (0,0,0)
        #pixels.fill((0, 0, 0))
        pixels[i] = (r,g,b) 

    pixels.show()
    #time.sleep(.2)
    camera.capture(name)
   # time.sleep(.5)
       
       
def alignPixels(datafilename):

    global num_pixels
    
    camera = PiCamera()
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 
    # NeoPixels must be connected to D10, D12, D18 or D21 to work. 

 
    l = []

    if not path.exists(datafilename):
        for j in range(num_pixels):
            print(j," ",end="")
            filename = "../image"+str(j)+".jpg"
     
            if not path.exists(filename):
                  takePicture(j,filename)
            l.append(readImage(filename))
            if l[-1][0] == -1: print(filename)
            #print(l)
            sys.stdout.flush()
    
        l1 = [(xy[0],xy[1],i) for i,xy in enumerate(l) if xy[0] != -1]
        l2 =  [(xy[1],xy[0],i) for i,xy in  enumerate(l) if xy[0] != -1]    
        pd.DataFrame(l1).to_csv(datafilename,index=False)


def showLines(datafilename):
    global num_pixels
     
    XFACTOR = 20
    df = pd.read_csv(datafilename)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2]) for x in df.values]

    ord = False

    for times in range(1):
        for ordered in ([x for x in sorted(l1,reverse=False)],[x for x in sorted(l1,reverse=True)],[x for x in sorted(l2,reverse=False)],[x for x in sorted(l2,reverse=True)]):

         pixels.fill((0, 0, 0))
         p =(-1,-1,-1) 

 

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
           #print(imin,imax,i) 
           for item in lit:
              print(item)
              pixels[int(ordered[item][2])] = (0,0,0)
           lit = []

              
           #pixels.fill((0, 0, 0))
           #pixels.show() 
           for j in range(len(ordered)):  
               if abs(ordered[j][0] - i) < vmax: 
                   lit.append(j)
                   v = int(ordered[j][2])
                   pixels[v] = (255,255,255)
               #else:
                  #  v = int(ordered[j][2])
#                    pixels[v] = (0,0,0)
           #print(lit)
          # print(1)
           pixels.show() 
           #print(2)
           #time.sleep(.1)


def lineDistance(x0,y0,x1,y1,x2,y2):
   rc = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / np.sqrt(np.square(x2-x1) + np.square(y2-y1))
   return rc
       
def showWaveLines(datafilename):
    global num_pixels
     
    XFACTOR = 20
    df = pd.read_csv(datafilename)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2]) for x in df.values]

    ord = False
    for ordered in [l1,l2]:
     for times in range(5):
        #for ordered in ([x for x in sorted(l1,reverse=False)],[x for x in sorted(l1,reverse=True)],[x for x in sorted(l2,reverse=False)],[x for x in sorted(l2,reverse=True)]):
       
         pixels.fill((0, 0, 0))
         p =(-1,-1,-1) 

 

         imin,imax = min([x[0] for x in ordered]),max([x[0] for x in ordered])
         jmin,jmax = min([x[1] for x in ordered]),max([x[1] for x in ordered])

         x,y = {},{}
         ## Fixed point
         #print(ordered)
        
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
              print(item)
              pixels[int(ordered[item][2])] = (0,0,0)
           lit = []

              
           #pixels.fill((0, 0, 0))
           #pixels.show() 
           for j in range(len(ordered)):  
               x[0] = ordered[j][0] ## X POINT of the pixel
               y[0] = ordered[j][1] ## Y POINT of the pixel
              
               distance = lineDistance(x[0],y[0],x[1],y[1],x[2],y[2])
              #  p1 = np.array([x[0],y[0]])
#                p2 = np.array([x[1],y[1]])
#                p3 = np.array([x[2],y[2]])
#                distance = np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
               ## calculate distance 
              
               if abs(distance) < 50: 
                   lit.append(j)
                   v = int(ordered[j][2])
                   pixels[v] = (128,128,128)
               #else:
                  #  v = int(ordered[j][2])
#                    pixels[v] = (0,0,0)
           #print(lit)
          # print(1)
           pixels.show() 
           #print(2)
           #time.sleep(.1)

def createFrame():
    # try to put pixels in a 20x30 frame 
    global datafilename
    df = pd.read_csv(datafilename)
    l1 =  [tuple(x) for x in df.values]
    l2 =  [(x[1],x[0],x[2]) for x in df.values]
    ordered = l1
    xmin,xmax = min([x[0] for x in ordered]),max([x[0] for x in l1])
    ymin,ymax = min([x[1] for x in ordered]),max([x[1] for x in l1])

    
    XSEGMENTS ,YSEGMENTS = 16,8
    xinc = (xmax-xmin)/XSEGMENTS
    yinc = (ymax-ymin)/YSEGMENTS
    matrix = {}
    dotmatrix = {}
    for i in range(XSEGMENTS):
      matrix[i] = {}
      dotmatrix[i] = {}
      for j in range(YSEGMENTS):
            matrix[i][j] = ((xmin+xinc*i) , (ymin+yinc*j))
            dotmatrix[i][j] = []
    
    for i in range(XSEGMENTS):
      for j in range(YSEGMENTS):
         x1,y1 = matrix[i][j]
         for pixel in l1:    
            x2,y2 = pixel[0],pixel[1]
            distance = ((x1-x2)**2+(y1-y2)**2)**0.5
            if distance < 50:
               dotmatrix[i][j].append(int(pixel[2]))
    pixels.fill((0, 0, 0))
    pixels.show()

    for i in range(XSEGMENTS):
      for j in range(YSEGMENTS):   
         for o in   ordered:
              # print(o)
               pixels[int(o[2])] = (0,0,0)
         for v in dotmatrix[i][j]:
             pixels[v] = (128,128,128)
         pixels.show()
         time.sleep(.1)
           
def drawScrollA():
    letter_a = ['00111100', '01000010', '01000010', '01111110', '01000010', '01000010', '01000010', '01000010']
    current_frame = ['10000001', '01000010', '00100100', '00011000', '00011000', '00100100', '01000010', '10000001']
    queue = ['00111100', '01000010', '01000010', '01111110', '01000010', '01000010', '01000010', '01000010']
    while len(queue[0]):
        display(current_frame)
        current_frame, queue = nextFrame(current_frame, queue)
        displayframe(current_frame)
        
def main():
    global  num_pixels,pixels

 
    
 
    datafilename = "orderednew.csv"
    
    alignPixels(datafilename)
 
        
    #showLines(datafilename)
    #showWaveLines(datafilename)
    createFrame()

if __name__ == '__main__':
    datafilename = "orderednew.csv"
    pixel_pin = board.D21 
 
 
    # The number of NeoPixels 
    #num_pixels = 30 
    num_pixels = 150 
 
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed! 
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW. 
    ORDER = neopixel.RGB 
    pixels = neopixel.NeoPixel( 
        pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
    ) 
    #cProfile.run('main()')
    main()
    
##  abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / np.sqrt(np.square(x2-x1) + np.square(y2-y1))
##  from numpy.linalg import norm 
## d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)


    
    