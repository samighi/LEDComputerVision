# Simple test for NeoPixels on Raspberry Pi 
import time 
import board 
import neopixel 
 
 
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 
# NeoPixels must be connected to D10, D12, D18 or D21 to work. 
pixel_pin = board.D21 
 
 
# The number of NeoPixels 
#num_pixels = 30 
num_pixels = 150 
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed! 
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW. 
ORDER = neopixel.GRB 
 
pixels = neopixel.NeoPixel( 
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER 
) 
 
 
import csv

import pandas as pd
#df = pd.read_csv('ordered.csv')
df = pd.read_csv('orderednew.csv')
l1 =  [tuple(x) for x in df.values]
l2 =  [(x[1],x[0],x[2]) for x in df.values]
for ordered in ([x[2] for x in sorted(l1)],[x[2] for x in sorted(l1,reverse=True)],[x[2] for x in sorted(l2,reverse=False)],[x[2] for x in sorted(l2,reverse=True)]):

 pixels.fill((0, 0, 0))
 p =(-1,-1,-1) 
 for j in range(len(ordered)):

  #  for i in range(0,num_pixels-2-j,3):
        i = int(ordered[j])
        i1 = -1
        i2 = -1
        if j > 1: i1 = int(ordered[j-1] )
        if j > 2: i2 = int(ordered[j-2]) 
        #pixels.fill((0, 0, 0))
        for v in p: 
            if p != -1: 
                pixels[v] = (0,0,0)
        r,g,b= 255,0,0
        p = (i,i1,i2)
#        if i == 0: 
#       else: 
        if True:
            #pixels[i-1] = (0,0,0)
            #pixels.fill((0, 0a, 0))
            pixels[i] = (r,g,b)
            pixels[i] = (255,255,255)
            #if i1 != -1: pixels[i1] = (g,b,r)
            #if i2 != -2: pixels[i2] = (b,r,g)
            

        pixels.show()
        #time.sleep(.1)
        #camera.capture('/home/pi/image'+str(j)+'.jpg')
 time.sleep(.5)



from random import random

df = pd.DataFrame(l1)
from time import sleep

newList = [tuple(x) for x in df.values]

X = [x[1] for x in newList]
Y = [x[0] for x in newList]
xmin,xmax = min(X),max(X)
ymin,ymax = min(Y),max(Y)

xstep = (xmax-xmin)/10
ystep = (ymax-ymin)/10

newOrder = sorted(newList,reverse=True)

print(newOrder)
prevCol = -1
balls = []
for j in range(50): # drop 30 colors
    column = int(random()*10)
    if prevCol == column:
        column = column + 1 % 10
    preCol = column
    # add the new color to the list
    balls.append((ymax,xmin+xstep*column,j))
    balls.append((ymax,xmin+xstep*column,j))


print(balls)

for j in range(200):
    #print(j)
    pixels.fill((0, 0, 0))
    for i,ball in enumerate(balls):
        step = j-i
        #if i < j: continue
        if step < 0 or step > 40 :  continue
        for pixel,xy in enumerate(newOrder):

            bx = ball[0]  - (xstep * step)
            by = ball[1]# - (ystep * step)
            x = xy[0]
            y = xy[1]
            dist = ((bx-x)**2+(by-y)**2)**.5
            if pixel == 0:  print((ball[0],ball[1]),step,(bx,x),(by,y),dist)
            #print(dist)
            #if dist < (xstep**2+ystep**2)**.5:
            if dist < 40:
                #print(pixel,xy,color)
               pixel = int(xy[2])
               colors = [(255,0,0),(255,0,255),(255,102,0),(255,255,255),(0,255,0),(0,0,255)]
               pixels[pixel] = colors[i % len(colors)]
    pixels.show()
    time.sleep(.2)
    #scatter_plot(newOrder,c)

    #sleep(.1)
    #clear_output(wait=True)

##  abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / np.sqrt(np.square(x2-x1) + np.square(y2-y1))
##  from numpy.linalg import norm 
## d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)

