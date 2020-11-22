#!/usr/bin/env python
# coding: utf-8
"""
Color-based object detection using OpenCV

Date: Nov 2020
Author: Yuanda Dong, Yiran Jing
Group: CP32-17b1 (COMP3988 group 1)

Help function in `Object_Detection_shenzhen.py`
"""



import matplotlib.pyplot as plt
from os import listdir, rename, listdir
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib
from sklearn.metrics import classification_report, confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
import seaborn as sns

import cv2
import numpy as np
import platform
import tempfile
import time
import sys
import shutil
import glob

import config as cfg

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from Object_Detection_shenzhen import *


# ### Load dataset and visualization


folder = "shenzhen-images"
labels = ["stop_selected", "right_selected", "left_selected", "park_green_selected"] # the raw shenzhen data
abs_path = "/Users/yiranjing/Desktop/COMP3988/Sign-Detection/Yiran/shenzhen-images/"
train_path = abs_path + "raw/" # the path of original training images
roi_train_path = abs_path + "roi_outputs/"# the path of the training rois after openCV processing


if __name__ == "__main__":

    # ### Original dataset size
    
    print("Train data: ")
    data_dir = pathlib.Path(folder+"/raw")
    image_count = len(list(data_dir.glob('*/*'))) # there are some png, also some jpg
    print("The total number of turning images are {}. \n".format(image_count))
    
    for class_name in labels:
        path = folder+"/raw/" + class_name
        #print(path)
        #path2 = pathlib.Path(path)
        image_count = len(list(pathlib.Path(path).glob('*')))
        print("{}: {} images.".format(class_name, image_count))
    
    
    # # OpenCV pre-processing
    #
    # Note that if the images fail to be detected using OpenCV, then they willnot be collected by roi output folder. And thus willnot be used to train model.
    #
    # We are trying to guarantee the high detection rate using openCV for each class
    
    
    class_folders = ["stop_selected/", "right_selected/", "left_selected/", "park_green_selected/"]
    
    
    for folder_name in class_folders:
        # process training images
        class_train_path = train_path + folder_name
        #print(class_train_path)
        roi_dst_dir = roi_train_path + folder_name
        fail_image_collection, success_rate = test_images(class_train_path, roi_dst_dir, 0)
        print("The success rate on {} training images is : {:.3f}".format(folder_name, success_rate))
    
    
    
    
    
