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
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
) 
 
 

from picamera import PiCamera
camera = PiCamera()

#RGB = [[(255,0,0),(255,0,0),(255,0,0)],[(0,0,255),(0,255,0),(255,0,0)], [(255,0,0),(0,0,255),(0,255,0)], [(0,255,0),(255,0,0),(0,0,255)]]
pixels.fill((0, 0, 0))
#for j in range(len(RGB)):
for j in range(num_pixels):
        print(j," ",end="")
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
        camera.capture('/home/pi/image'+str(j)+'.jpg')
       # time.sleep(.5)
