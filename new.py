from rpi_ws281x import * 
import argparse

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 12      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

RATE = 5
# Simple test for NeoPixels on Raspberry Pi 
import time 
import board 
import neopixel

pixel_pin = [board.D21,board.D12]

num_pixels = 150 
ORDER = neopixel.RGB 
for strand in range(2):
        print(strand)
        pixels = neopixel.NeoPixel( 
                pixel_pin[strand], num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
            ) 
        pixels.fill((0, 0, 0))
        pixels.show()

import time
import picamera

frames = num_pixels * len(pixel_pin)

def filenames():
    global strip
    global frame
    while frame < frames:
         lclFrame = frame % num_pixels
         strand = int(frame/num_pixels)
         pixels = lpixels[strand]
         if strand == 1 and frame == num_pixels:
          lpixels[0].fill((0, 0, 0))
          lpixels[0].show()
         strFile = '../image'+str(strand)+"-"+str(lclFrame)+".jpg"
         print(strFile, strand,frame) 
         yield strFile
         if lclFrame > 0: pixels[lclFrame-1] = (0,0,0)
         r,g,b= (255,255,255)
         pixels[lclFrame] = (r,g,b) 
         pixels.show()
         frame += 1

lpixels = [0,0]
with picamera.PiCamera() as camera:
    frame = 0 
    print(strand)
    lpixels[0] = neopixel.NeoPixel( 
            pixel_pin[0], num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
        ) 
    lpixels[1] = neopixel.NeoPixel( 
            pixel_pin[1], num_pixels, brightness=1, auto_write=False, pixel_order=ORDER 
        ) 
#    camera.resolution = (2000,1500)
    camera.resolution = (1024, 768)
    camera.framerate = RATE
    #camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(filenames(), use_video_port=True)
    finish = time.time()
    print('Captured %d frames at %.2ffps' % (
        frames,
        frames / (finish - start)))
