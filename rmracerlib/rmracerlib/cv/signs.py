'''
# Sign detection
'''

import cv2
import numpy as np
import platform
import tensorflow as tf
import time
import sys
from tensorflow import keras
from rmracerlib import config as cfg
# from rmracerlib.cv.func import sign_direction, direction_check, valid_range
from rmracerlib.Object_Detection import *

# Tensorflow Detection set up 
# model = keras.models.load_model('/home/yuanda/donkey/week4-rmracerlib/rmracerlib/sign_30Oct_with_other5Classes.h5')
model = keras.models.load_model('/home/yuanda/donkey/week4-rmracerlib/rmracerlib/sign.h5')
# class_names = ['other', 'park', 'right', 'speed_50_white', 'stop']
# class_names = ['park', 'right', 'speed_50_white', 'stop']
class_names = ['left', 'park', 'right', 'speed_50_white', 'stop']
stop = ["stop"]
left = ["left", "left_blue", "left_black", "left_purple"] 
right = ["right", "right_blue", "right_black", "right_purple"] 
park = ['park', 'park_blue', "park_white"] 
speed = ["speed_50_white"] 
###
###
###  SIGN DETECTIONS
###
###




def detect(frame_original): 
    roi, result, rect = detect_interested_area(frame_original)
    if result == False:
        # print('other')
        return None,rect
    tensor_roi = tf.expand_dims(roi, 0) 
    predictions = model.predict(tensor_roi)
    score = tf.nn.softmax(predictions[0])
    if 100 * np.max(score) >= 98:
        out = class_names[np.argmax(score)] 
        # print(out)
        if out in stop:
            return "stop",rect
        elif out in left: 
            return "left",rect
        elif out in right: 
            return "right",rect
        elif out in park:
            return "park",rect
        elif out in speed:
            return "speed",rect 
    # else:
        # print('other')
    return None,rect 


    # print(class_names[np.argmax(score)])
    # if (class_names[np.argmax(score)] != None) and (100 * np.max(score) > 90): 
    #     return class_names[np.argmax(score)]
    #     else:
    #         return None
    # if 100 * np.max(score) > 95:
    #     print(class_names[np.argmax(score)])
    # return None
