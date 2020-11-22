#!/usr/bin/env python
# coding: utf-8

"""
Traffic Sign Classification using NN

Author: Yiran Jing
Date: Nov 2020
Group: CP32-17b1 (COMP3988 group 1)

# Our model can classify the input images (collected by the donkey car) into 5 main classes:
# - right-turining (including blue, black-turning sign)
# - left-turining (including blue, black-turning sign)
# - stop
# - speed_50_white
# - park (yellow and green)
# 
# 
# ## Content 
# 1. **Obstract interested area (detect based on color) using openCV**
# 1. **EDA**
# 2. **Feature Engineering**
#     1. Configure the dataset for performance (all 100 * 100)
#     2. Standardize the data
# 3. **Train model**
#     1. 20% as test data, 80% as train data
#     2. three convolution blocks
# 4. **Model evaluation**
#     1. Confusion Matrix
#     2. Classification report for each class
#          - The overall TEST accuracy is 100%. The model performances very good overall.
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
import tempfile
import cv2
import numpy as np
import platform
import time
import sys
import shutil
import glob

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from TFmodel_helper_function import *
from Object_Detection_Unity import *



folder = "data"
labels = ["stop", "right", "left", "park", "speed_50_white"]
abs_path = "data/"

train_path = abs_path + "train/" # the path of original training images
test_path = abs_path + "test/" # the path of original test images
roi_train_path = abs_path + "trainCNN_roi/" # the path of the training rois after openCV processing
roi_test_path = abs_path + "testCNN_roi/" # the path of the test rois after openCV processing
fail_openCV = abs_path + "fail_openCV/" # the path used to collect failed image
roi_test_misclass_path = abs_path + "test_roi/"

# the folder of mannully cleaned dataset, which will be used to train model.
trainCNN_roi = "/trainfilterCNN_roi" # the roi image folder including iamges had been manually  filltered
testCNN_roi = "/testfilterCNN_roi" # the folder name of testing roi images images



if __name__ == "__main__":

    # ### Original dataset size
    
    # load dataset
    data_dir = load_training_data(folder, "/train")
    print("--------------------------------------------")
    test_data_dir = load_testing_data(folder, "/test")
    
    """
    Stage 1: Data proprocessing using openCV
    """
    image_proprecessing_openCV(class_names, train_path, roi_train_path)
    
    
    """
    Stage 2: Train CNN model
    """
    ## Data processed by openCV for CNN model training
    
    # The data in the folder `trainfilterCNN_roi` and `testfilterCNN_roi` are the selected roi from     `trainCNN_roi` and `testCNN_roi`folder
    
    
    # images will be used to train and test data
    data_dir = load_training_data(folder, trainCNN_roi)
    test_data_dir = load_testing_data(folder, testCNN_roi)
    
    # split training, validation and testing dataset
    train_ds, val_ds, test_ds = separate_train_val_test_data(data_dir, test_data_dir)
    
    class_names = train_ds.class_names
    print("The class will be used to train CNN models are:")
    print(class_names)
    
    ## visualize some training data
    visualization_training_data(train_ds)
    
    # Feature Engineering
    train_ds, val_ds, test_ds = dataset_config(train_ds, val_ds, test_ds)
    
    # Train Model
    cnn, cnn_history = train_visualize_CNN(epochs, train_ds, val_ds)
    
    # Visualize CNN model results
    plot_train_result(cnn_history, epochs)
    
    # Model evaluation
    draw_confusion_matrix(cnn, test_ds, class_names)
    
    # save model
    cnn.save('../../model/sign.h5')
    
