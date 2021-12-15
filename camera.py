#!/usr/bin/env python

from picamera import PiCamera
from time import sleep

camera = PiCamera()
#camera.rotation = 90
if False:
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
#camera.start_preview()
#sleep(5)
camera.capture('/tmp/picture.jpg')
#camera.stop_preview()
