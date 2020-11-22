'''
# Traffic light detection
'''

import cv2
import numpy as np

import time

from rmracerlib import config as cfg
from rmracerlib.cv.func import sign_direction, direction_check, valid_range

## FILTERS
# brightness filter
#brightness_lower = np.array([0, 0, 255])
#brightness_upper = np.array([180, 255, 255])
brightness_lower = np.array([0, 30, 255])
brightness_upper = np.array([180, 150, 255])


# For changing colour counter filter values in light_detect,
#  go to the function where the counter is.

# set kernel for operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize = (cfg.TRAFFIC_KERNEL_SIZE, cfg.TRAFFIC_KERNEL_SIZE))
    

def light_signal(shape):
    """
      Expects:  HSV Region of Interest
      Returns:  Colour Detected
    """
    # Get picture shape information
    rows,cols,dims=shape.shape

    # Separate picture channel
    h, s, v = cv2.split(shape)

    # Pixel color count
    g_counter=0
    r_counter=0
    y_counter=0

    # COLOUR FILTER - THIS IS WHERE THE COLOURS GET FILTERED OUT
    for i in range(rows):
        for j in range(cols):
            if (60 <= h[i,j] <= 85) and (v[i,j] <= 248):
                g_counter += 1

            elif ((170 <= h[i,j] <= 180) or (0 <= h[i,j] <= 14)) and (v[i,j] <= 200):
                r_counter += 1

            elif (8 <= h[i,j] <= 20) and (v[i,j] <= 254):
                y_counter += 1

    if g_counter > cfg.COUNTER_THRESHOLD_GREEN:
        return "go"
        #retun g_counter
    if r_counter > cfg.COUNTER_THRESHOLD_RED:
        return "stop"
        #return r_counter
    if y_counter > cfg.COUNTER_THRESHOLD_AMBER:
        #print("yellow")
        return None
        #return "stop"
        #return y_counter
    else :
        return None

def detect_traffic(frame, hsv):
    """
     Expects: HSV image of any shape + current frame
     Returns: TBD
    """
    #hsv = cv2.cvtColor(frame, cfg.COLOUR_CONVERT) # convert to HSV CS
    
    # perform filter and operations
    mask = cv2.inRange(hsv, brightness_lower, brightness_upper)
    morph_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    final = cv2.dilate(morph_open, kernel,iterations=2)
    

    # contours detection
    contours, _ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # create a rect box around each object located
        x,y,w,h = cv2.boundingRect(cnt)

        # OPTION 1: extract Region of Interest (ROI) from original image
        #roi = frame[y-15:y+h+15, x-15:x+w+15]

        # OPTION 2: extract ROI from HSV colour space (more efficient)
        #roi = hsv[y-15:y+h+15, x-15:x+w+15]
        roi = hsv[y:y+h, x:x+w]

        # calculate area to determine if size worth looking at
        area = cv2.contourArea(cnt)

        if cfg.AREA_SIZE_TRAFFIC < area < cfg.MAX_AREA_SIZE:
            # give ROI to pixel detect functions
            result = light_signal(roi)

            # show output in Demo Mode
            if cfg.DEMO_MODE and result:
                #print(area)
                if result == "stop":
                    color = (0,0,255)
                else:
                    color = (0,255,0)
                cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                cv2.putText(frame, result, (x+w, y+h), cfg.FONT, 1, color)
            # return result
            return result
    # no colour significiant enough to be found
    return None
