# Simple test for NeoPixels on Raspberry Pi 
import time 
import board 
import neopixel 
 
 
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 
# NeoPixels must be connected to D10, D12, D18 or D21 to work. 
pixel_pin = board.D21 
 
 
# The number of NeoPixels 
#num_pixels = 30 
num_pixels = 100 
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed! 
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW. 
ORDER = neopixel.GRB 
 
pixels = neopixel.NeoPixel( 
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER 
) 
 
 

from picamera import PiCamera
camera = PiCamera()

ordered = [99,
  98,
  90,
  89,
  95,
  97,
  92,
  96,
  88,
  91,
  87,
  86,
  85,
  82,
  84,
  83,
  81,
  78,
  67,
  77,
  69,
  66,
  68,
  75,
  76,
  65,
  73,
  70,
  64,
  72,
  71,
  63,
  62,
  54,
  55,
  56,
  57,
  0,
  59,
  58,
  53,
  1,
  2,
  52,
  51,
  47,
  3,
  45,
  48,
  50,
  46,
  4,
  44,
  49,
  5,
  43,
  36,
  39,
  38,
  40,
  37,
  35,
  7,
  26,
  27,
  34,
  31,
  24,
  29,
  25,
  8,
  28,
  33,
  9,
  10,
  22,
  11,
  21,
  17,
  14,
  15,
  12,
  18,
  19,
  13,
  16]

pixels.fill((0, 0, 0))
p =(-1,-1,-1) 
for j in range(len(ordered)):

  #  for i in range(0,num_pixels-2-j,3):
        i = ordered[j]
        i1 = -1
        i2 = -1
        if j > 1: i1 = ordered[j-1] 
        if j > 2: i2 = ordered[j-2] 
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
            if i1 != -1: pixels[i1] = (g,b,r)
            if i2 != -2: pixels[i2] = (b,r,g)
            

        pixels.show()
        time.sleep(.1)
        #camera.capture('/home/pi/image'+str(j)+'.jpg')
       # time.sleep(.5)
