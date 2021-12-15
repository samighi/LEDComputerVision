# Simple test for NeoPixels on Raspberry Pi 
import time 
import board 
import neopixel 
 
 
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 
# NeoPixels must be connected to D10, D12, D18 or D21 to work. 
pixel_pin = board.D21 
#pixel_pin = board.D12 
#pixel_pin = board.D18 
 
 
# The number of NeoPixels 
#num_pixels = 30 
num_pixels = 100 
num_pixels = 50 
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed! 
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW. 
ORDER = neopixel.GRB 
print(0) 
pixels = neopixel.NeoPixel( 
    pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER 
) 
print(1)
 


for i in range(num_pixels):
    print(i)
    r,g,b = 255,0,0
    if i == 0: 
        pixels.fill((0, 0, 0))
    else: 
        pixels[i-1] = (0,0,0)
        pixels[i] = (r, g, b)
        pixels.show()
        time.sleep(.1)

