'''
# Config
'''

import cv2
import numpy as np
import platform

import time
import sys

##
## Open CV Variables
##
# show the debug output for the open cv
DEMO_MODE = True

# Collect data and save to new image folder

# set some variables for testing output
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Min and Max Area Sizes
AREA_SIZE_STOP = 50
AREA_SIZE_TURN = 50
AREA_SIZE_PARK = 50
AREA_SIZE_TRAFFIC = 25
AREA_SIZE_CONE = 100
MAX_AREA_SIZE = 1200

# kernels
KERNEL_SIZE = 3
TRAFFIC_KERNEL_SIZE = 3
STOP_KERNEL_SIZE = 9

# traffic signal threshold counters
COUNTER_THRESHOLD_GREEN = 20
COUNTER_THRESHOLD_RED = 25
COUNTER_THRESHOLD_AMBER = 15

HORIZON = 0
ROOF = 0
ROOF_R = 0 #1/4
HORIZON_R = 1 # get top half only

# Define what colour space we are working with.
#  For some reason Jetson Nano (gstreamer) needs RGB instead of BGR
os = platform.system()
if os == 'Linux':  # Jetson
    COLOUR_CONVERT = cv2.COLOR_RGB2HSV
elif os == 'Windows': # Testing
    COLOUR_CONVERT = cv2.COLOR_BGR2HSV
elif os == 'Darwin':
    COLOUR_CONVERT = cv2.COLOR_BGR2HSV

## Error checking (valid_range) function
# show the detection area in the output image
DRAW_RANGE = True

# set the range for detection (horizontal).  Fractions of total (5 = 1/5, 2 = 1/2, 1 = whole frame)
VR_TOP = 5	# 1/5 - close to the top but no the roof
VR_BOTTOM = 2 	# 1/2 - halfway



##
## Donkey Car Variables
##
# Threshold: How many values in set before running code.  (set 0 to always run)
# Size:  How many values to keep track of, more values opens potential for higher error rate (min 3, default 10)
DK_COUNTER_THRESHOLD = 4   # will take (+1) of value
DK_COUNTER_SIZE = 10       # 1 = ~0.05 secs, 20 = 1 sec

# Delay: wait this many cycles before executing the command (set to 0 for no delay)
# Runtime:  wait this many cycles until AutoPilot can run again
DK_ACTION_DELAY = 5      # 10 = 0.5s, 20 = 1 sec
DK_ACTION_RUNTIME = 60        # 60 = 3.0s, 20 = 1 sec
DK_STOP_RUNTIME = 6
DK_STOP_TOTALTIME = 100

# show the debug output for the donkey car part.
DK_SHOW_TEXT_DEBUG = True
