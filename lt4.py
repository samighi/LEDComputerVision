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
 
 

from picamera import PiCamera
camera = PiCamera()

RGB = [[(255,0,0),(255,0,0),(255,0,0)],[(0,0,255),(0,255,0),(255,0,0)], [(255,0,0),(0,0,255),(0,255,0)], [(0,255,0),(255,0,0),(0,0,255)]]
pixels.fill((0, 0, 0))
for j in range(len(RGB)):

    for i in range(0,num_pixels-2-j,3):
        r,g,b = 255,0,0
#        if i == 0: 
#       else: 
        if True:
            #pixels[i-1] = (0,0,0)
            #pixels.fill((0, 0, 0))
            pixels[i+j] = RGB[0][0]
            pixels[i+1+j] = (0,0,0)# RGB[j][1]
            pixels[i+2+j] = (0,0,0)# RGB[j][2]

            pixels.show()
    time.sleep(.5)
    camera.capture('/home/pi/image'+str(j)+'.jpg')
    time.sleep(.5)
