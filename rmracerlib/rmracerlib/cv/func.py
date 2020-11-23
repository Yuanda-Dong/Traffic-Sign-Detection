'''
# Functions
'''

import cv2
import numpy as np
import platform

import time
import sys

from rmracerlib import config as cfg


def contours_detection(mask, frame):
    # find shapes
    # contours detection
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if area > AREA_SIZE:
            
            if len(cnt) == 8:
                cv2.drawContours(frame, [approx], 0, (0,0,0), 5)
                x = approx.ravel()[0]
                y = approx.ravel()[1]
                cv2.putText(frame, "STOP", (x,y), font, 1, (0,0,0))
                return "stop"

    # nothing
    return None

###
###
###  HELPER FUNCTIONS
###
###

def valid_range(x, y, w, h, frame):
    '''
    This function returns if an roi is in a valid or acceptable part of the image.  The reason
     for having this is due to extra parts of the frame containing reflections.
    '''
    left_buf = 10
    right_buf = 40
    top_buf = 10
    centre_buf = 25

    height, width = frame.shape[:2]

    h_top = int(height / cfg.VR_TOP)     # previously h1
    h_bot = int(height / cfg.VR_BOTTOM)  # previously horizon

    v0 = left_buf       # furthest left width
    v1 = int(width/3)   # 1/3rd width
    v2 = v1*2           # 2/3rd width
    v3 = width - right_buf   # furthest right width

    if cfg.DRAW_RANGE: 
        cv2.line(frame, (0, h_top ), (width, h_top ), (255,0,255))
        cv2.line(frame, (0, h_bot ), (width, h_bot ), (0,255,255))

    cw = True
    ch = False

    if ( (v0 < x < v1) or (v2 < x < v3) ) and ( (v0 < x+w < v1) or (v2 < x+w < v3) ):
        cw = True

    if (h_top < y < h_bot) and (h_top < y+h < h_bot): #h0 < y < h2:
        ch = True

    if ch and cw:
        return True
    else:
        return False

def is_squarish(height, width):
    # calculate ratio of sides - anything not square is not worth checking
    a = height / width
    b = width / height

    if (0.5 < a < 2.0) and (0.5 < b < 2.0):
        return True
    else:
        return False

def sign_direction(img):
    """
        Turning Sign Detection Part 1
        Reads in a ROI and outputs either: right, left or None
    """
    # sharpen the ROI so it is clearer for detection
    sharpen = cv2.GaussianBlur(img, (3,3), 3)
    sharpen = cv2.addWeighted(img, 1.5, sharpen, -0.5, 0)

    # convert image to binary
    grey = cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)
    thresh, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # get picture shape information for selecting a smaller ROI
    height, width = binary.shape[:2]

    # CHECK 1 - calculate ratio of sides - anything not square is not worth checking
    a = height / width
    b = width / height
    if (0.5 < a < 2.0) and (0.5 < b < 2.0):
        pass
    else:
        return None

    # CHECK 2 - check the mix of white and black pixels to eliminate false detections
    # calculate total number of pixels (TODO: faster way)
    total = height * width

    # calculate ratios
    n_white_pix = np.sum(binary == 255)
    w_ratio = int(n_white_pix / total * 100)
    n_black_pix = np.sum(binary == 0)
    b_ratio = int(n_black_pix / total * 100)

    # check
    if ( ( 40 <= w_ratio <= 60 ) and ( 40 <= b_ratio <= 60 ) ):
        # run the sign detection algorithm
        result = direction_check(binary)

        if result is not None:
            return result

    # if we fail any tests, return None
    return None



def direction_check(binary):
    """
        Turning Sign Dection Part 2
        Checks the sign direction based on relevant information in the image
    """
    # extract image information
    height, width = binary.shape[:2]

    # set up our regions at 25%, 50% and 75% marks
    #  we are only going to look at the center of the binary image
    h1 = int(height/4)  # was 0
    h2 = int(height/2)
    h3 = int(h1+h2)     # was height

    v1 = int(width/4)   # was 0
    v2 = int(width/2)
    v3 = int(v1+v2)     # was width

    # quadrants / regions
    q1Block = binary[h1:h2, v2:v3]
    q2Block = binary[h1:h2, v1:v2]
    q3Block = binary[h2:h3, v1:v2]
    q4Block = binary[h2:h3, v2:v3]

    # add up the number of white pixels in each quadrant.
    q1Sum = np.sum(q1Block == 255)
    q2Sum = np.sum(q2Block == 255)
    q3Sum = np.sum(q3Block == 255)
    q4Sum = np.sum(q4Block == 255)

    # information search - check which region has the most white pixels and then
    #  determine if the sign is left or right.
    if q4Sum > q3Sum: #and q1Sum < q2Sum:
        #print("guess: left")
        return "left"
    elif q4Sum < q3Sum: #and q1Sum > q2Sum:
        #print("guess: right")
        return "right"
    else:
        return None

