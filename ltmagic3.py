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
 
 


import pandas as pd
#df = pd.read_csv('ordered.csv')
df = pd.read_csv('orderednew.csv')
l1 =  [tuple(x) for x in df.values]
l2 =  [(x[1],x[0],x[2]) for x in df.values]

ord = False

for ordered in ([x for x in sorted(l1,reverse=False)],[x for x in sorted(l1,reverse=True)],[x for x in sorted(l2,reverse=False)],[x for x in sorted(l2,reverse=True)]):

 pixels.fill((0, 0, 0))
 p =(-1,-1,-1) 

 

 imin,imax = min([x[0] for x in ordered]),max([x[0] for x in ordered])
 rangevalues = range(int(imin),int(imax),int((int(imax)-int(imin))/40))
 if ord == True: 
    rangevalues = range(int(imax),int(imin),-int((int(imax)-int(imin))/40))
    ord = False
 else:
    ord = True
    
 for i in rangevalues:
   print(0)
   vmax = ((int(imax)-int(imin))/40) * 0.55
   #print(imin,imax,i) 
   lit = []
   #pixels.fill((0, 0, 0))
   #pixels.show() 
   for j in range(len(ordered)):  
       if abs(ordered[j][0] - i) < vmax: 
           lit.append(j)
           v = int(ordered[j][2])
           pixels[v] = (255,255,255)
       else:
           v = int(ordered[j][2])
           pixels[v] = (0,0,0)
   print(lit)
   print(1)
   pixels.show() 
   print(2)
   #time.sleep(.5)


