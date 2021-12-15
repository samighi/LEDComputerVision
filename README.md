# LEDComputerVision<br>

This is to be used with a Raspi 4 4 GB model - SD size 16 GB - RaspberryPi OS (at the time of this writing) 

pyenv local 3.8.3<br>
pip install board<br>
pip install rpi_ws281x adafruit-circuitpython-neopixel<br>
python -m pip install --force-reinstall adafruit-blinka<br>
pip install imutils<br> 
pip install numpy <br>
pip install opencv-contrib-python==4.5.3.56<br>
pip install scikit-image<br>
pip install pandas <br>

Finally and only with Python 3.8.3 (and about 10 hours of compiling) 

### running the code

There are a lot of connections and setup that has to be done, maily using rpi_ws281x module 

the code below finally runs the LEDs on the tree with patterns however it has to be pre-proceesed first 

Step <last>: python colornew3D-with-patterns.py

Step 1: python dual-wscolor.py 
Step 1a: This creates the first view of the tree. it should work fine with moving the LEDs up and down and to the sides. 

More instruction to do for each 0 90 180 270 view of the tree
And then process each view to a X Y Z from a Y X view of the camera 
  
 
