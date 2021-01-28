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
ORDER = neopixel.RGB
 
pixels = neopixel.NeoPixel( 
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
) 
 
 
import csv

import pandas as pd
#df = pd.read_csv('ordered.csv')
df = pd.read_csv('orderednew.csv')
l1 =  [tuple(x) for x in df.values]
l2 =  [(x[1],x[0],x[2]) for x in df.values]

lit = [z[2] for z in l1]
unlit = [x for x in range(num_pixels) if x not in lit]


pixels.fill((0, 0, 0))

for j in unlit: 
  pixels[j] = (255,0,0)

pixels.show()