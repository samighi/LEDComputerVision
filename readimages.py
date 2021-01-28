import sys
import traceback
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

import cv2
from scipy.ndimage import rotate
import pandas as pd

l = []
for j in range (0,150): 
    try: 
    #if True:
        file = "../image"+str(j)+".jpg"
        img = cv2.imread(file)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        blurred = cv2.GaussianBlur(gray, (11,11), 0)

        thresh = cv2.threshold(blurred, 195, 255, cv2.THRESH_BINARY)[1]

        #Detecting multiple bright spots in an image with Python and OpenCV
        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        #thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        #Detecting multiple bright spots in an image with Python and OpenCV
        # perform a connected component analysis on the thresholded
        # image, then initialize a mask to store only the "large"
        # components
        labels = measure.label(thresh, connectivity = 2 , background=0) #,neighbors=4 ## deprecated
        mask = np.zeros(thresh.shape, dtype="uint8")
        # loop over the unique components
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue
            # otherwise, construct the label mask and count the
            # number of pixels 
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
            # if the number of pixels in the component is sufficiently
            # large, then add it to our mask of "large blobs"
            if numPixels > 300:
                mask = cv2.add(mask, labelMask)


        image = img 
        #Detecting multiple bright spots in an image with Python and OpenCV
        # find the contours in the mask, then sort them from left to
        # right
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = contours.sort_contours(cnts)[0]
        # loop over the contours
        for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            #print(cX,cY)
           
            cv2.circle(image, (int(cX), int(cY)), int(radius),
                (0, 0, 255), 3)
            cv2.putText(image, "{}".format(i + 1), (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        
        # show the output image
        #cv2.imshow("Image", image)
        l.append((cX,cY))
    except:
    #else:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        cX,cY = -1,-1
        print(cX,cY)
        l.append((cX,cY))
        print(len([x for x in l if x[0] == -1]),file)
        #l.append((-1,-1))

l1 = [(xy[0],xy[1],i) for i,xy in enumerate(l) if xy[0] != -1]
l2 =  [(xy[1],xy[0],i) for i,xy in  enumerate(l) if xy[0] != -1]    
pd.DataFrame(l1).to_csv("orderednew.csv",index=False)


