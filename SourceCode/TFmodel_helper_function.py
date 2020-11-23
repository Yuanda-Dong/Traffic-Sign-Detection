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


import config as cfg
from Object_Detection_Unity import *



folder = "data" # dataset name
labels = [ "stop", "right", "left", "park", "speed_50_white"] # define the labels of model


# define the path
abs_path = "data/" # change to relative path, according to the bitbucket structure
train_path = abs_path + "train/" # the path of original training images
test_path = abs_path + "test/" # the path of original test images
roi_train_path = abs_path + "trainCNN_roi/" # the path of the training rois after openCV processing
roi_test_path = abs_path + "testCNN_roi/" # the path of the test rois after openCV processing
roi_test_misclass_path = abs_path + "test_roi/" 


# the folder of mannully cleaned dataset, which will be used to train model.
trainCNN_roi = "/trainfilterCNN_roi" # the roi image folder including iamges had been manually filltered
testCNN_roi = "/testfilterCNN_roi" # the folder name of testing roi images images 


# Predefined CNN model Hyper-parameter 
learning_rate = 0.001
batch_size = 64
img_height = 100
img_width = 100
epochs = 8

# folder used in openCV processing
class_names = ["stop/stop_simulator/", "stop/stop_realWorld/", 
                 "right/right_blue/", "right/right_realWorldImage/", "right/right_black/",
                 "left/left_blue/", "left/left_real_worldImage/", "left/left_black/","left/left_blue_f1/",
                "park/park_green/", "park/park_yellow/", #"park/park_white/",
                 "speed_50_white/speed_50_white_simulator/", "speed_50_white/speed_50_realworldImage/"
                ]

#labels = ["stop/stop_simulator", "right/right_blue", "right/right_black", "left/left_blue",
#"left/left_black", "park/park_yellow", "park/park_green",     "speed_50_white/speed_50_white_simulator"
#]

labels = ['left', 'park', 'right', 'speed_50_white', 'stop'] # class for model training 

def load_training_data(folder, train_path):
    """
    load the training data folder, and print the number of images in each class
    
    parameter:
        folder: (string) the name of dataset
        train_path: (string) the folder name of training dataset
    
    output:
        data_dir: the path of training dataset
    """
    print("Train data: ")
    data_dir = pathlib.Path(folder + train_path)
    image_count = len(list(data_dir.glob('*/*/*'))) # there are some png, also some jpg
    #image_count = len(list(data_dir.glob('*/*')))
    print("The total number of turning images are {}. \n".format(image_count))

    for class_name in labels:
        path = folder+ train_path + "/" + class_name 
        #path2 = pathlib.Path(path)
        image_count = len(list(pathlib.Path(path).glob('*/*')))
        print("{}: {} images.".format(class_name, image_count))
        
    return data_dir



def load_testing_data(folder, test_path):
    """
    load the testingdata folder, and print the number of images in each class
    
    parameter:
        folder: (string) the name of dataset
        test_path: (string) the folder name of test dataset
    
    output:
        test_data_dir: the path of testing dataset
    """
    print("Test data:")
    test_data_dir = pathlib.Path(folder + test_path)
    image_count = len(list(test_data_dir.glob('*/*/*'))) # there are some png, also some jpg
    #image_count = len(list(test_data_dir.glob('*/*')))
    print("The total number of test images are {}. \n".format(image_count))

    for class_name in labels:
        path = folder + test_path + '/' + class_name 
        image_count = len(list(pathlib.Path(path).glob('*/*')))
        print("{}: {} images.".format(class_name, image_count))
        
    return test_data_dir
    

    
    
def image_proprecessing_openCV(class_folders, train_path, roi_train_path):
    """
    OpenCV pre-processing 
    
    parameters: 
        class_folders: list, the folder name of raw images need to be processed by openCV
        train_path: the path of train dataset
        roi_train_path: the path that roi output images will be written to.
    
    """

    for folder_name in class_folders:
    
        # process training images
        class_train_path = train_path + folder_name
        roi_dst_dir = roi_train_path + folder_name
        fail_image_collection, success_rate = test_images(class_train_path, roi_dst_dir, 0)
        print("The success rate on {} training images is : {:.3f}".format(folder_name, success_rate))
    
        # process testing images
        if "world" or "f1" in folder_name.lower():
            continue # the testing dataset has no realworld images currently
        class_test_path = test_path + folder_name
        roi_dst_dir = roi_test_path + folder_name
        fail_image_collection, success_rate = test_images(class_test_path, roi_dst_dir, 0)
        print("The success rate on {} test images is : {:.3f}".format(folder_name, success_rate))
 


def separate_train_val_test_data(data_dir, test_data_dir):
    """
    separate train, validation, and test data, and resize the image
    we split 20% data from train as the validation set

    
    parameters:
        data_dir: relative path of train dataset
        test_data_dir: relative path of test dataset
    
    return:
        train_ds: keras preprocessing image_dataset
        val_ds: keras preprocessing image_dataset
        test_ds: keras preprocessing image_dataset
    """

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2, # 20% as validation data
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_data_dir,
        image_size=(img_height, img_width),
        seed=123,
        batch_size=batch_size)
        
    return train_ds, val_ds, test_ds


def visualization_training_data(train_ds):
    """
    visualize some training data
    
    train_ds: keras preprocessing image_dataset
    """
    plt.figure(figsize=(16, 16))
    class_names = train_ds.class_names
    for images, labels in train_ds.take(1):
        for i in range(25):
            ax = plt.subplot(5, 5, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
            
            
def dataset_config(train_ds, val_ds, test_ds):
    """
    Configure the dataset for performance
    
    parameters:
        train_ds: keras preprocessing image_dataset
        val_ds: keras preprocessing image_dataset
        test_ds: keras preprocessing image_dataset
    
    
    return:
        train_ds: keras preprocessing image_dataset
        val_ds: keras preprocessing image_dataset
        test_ds: keras preprocessing image_dataset
    
    """

    AUTOTUNE = tf.data.experimental.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, val_ds, test_ds


def train_visualize_CNN(epochs, train_ds, val_ds):
    """
    Train CNN model:
    The model consists of three `convolution blocks` with a `max pool layer` in each of them. 
    There's a fully connected layer with 128 units on top of it that is activated by a `relu` activation function.
    
    parameters:
            epochs: (int) the number of epoch
            train_ds: keras preprocessing image_dataset
            val_ds: keras preprocessing image_dataset
            
    output:
            cnn: the CNN model object 
            cnn_history: model history
    """
            
    num_classes = len(class_names)
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=1) ## add EarlyStopping
    # This callback will stop the training when there is no improvement in
    # the validation loss for three consecutive epochs.
    cnn = Sequential([
          #data_augmentation,
          layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
          layers.Conv2D(16, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(32, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(64, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Flatten(),
          layers.Dense(128, activation='relu'), 
          layers.Dense(num_classes)
            ])

    cnn.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    cnn_history = cnn.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs, 
      callbacks=[callback] # EarlyStopping
    )
     
    return cnn, cnn_history



def plot_train_result(model_result, epoch):
    """
    Plot accuracy and loss of training data and validation data
    """
    acc = model_result.history['accuracy']
    val_acc = model_result.history['val_accuracy']

    loss=model_result.history['loss']
    val_loss=model_result.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(range(len(acc)), acc, label='Training Accuracy')
    plt.plot(range(len(acc)), val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(range(len(acc)), loss, label='Training Loss')
    plt.plot(range(len(acc)), val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()
    
def plot_normalized_confusion_matrix(y_true, y_pred, title, class_names):
    """
    helper function of draw_missclassification_images
    draw confusion matrix based on the raw matrix, adding label
    
    parameters:
        class_names: list of string
        title: string
        y_true: panda series
        y_pred: panda series
    """
    cm = confusion_matrix(y_true, y_pred)
    # normalized 
    cmn = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    target_names = class_names
    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle(title,fontsize=20)
    ax.set_xlabel("Preidicted_Label")
    ax.set_ylabel('True_Label')
    
    sns.heatmap(cmn, annot=True, fmt='.2f', xticklabels=target_names, 
            yticklabels=target_names, linewidths=.8,)
    plt.show()  

    
def draw_confusion_matrix(model, val_ds, class_names):
    """
    Plot confusion matrix and classification report
    
    parameters:
        class_names: list of string
        val_ds: keras preprocessing image_dataset
    """
    Y_pred = model.predict(val_ds)
    y_pred = np.argmax(Y_pred, axis=1)
    print('Confusion Matrix, x label is Predicted_Label, y is True_Label')
    y_true = np.concatenate([y for x, y in val_ds], axis=0)
    plot_normalized_confusion_matrix(y_true, y_pred, "Normalized Confusion Matrix", class_names) # self-defined function
    
    print('Classification Report bazed on test data')
    #target_names = train_ds.class_names
    target_names = class_names
    print(classification_report(y_true, y_pred, target_names=target_names))


    
def test_missclassification_images(class_name, model, roi_dst_dir, class_names, CI_level,
                                   display_misclassification_images = False):
    """
    test the misclassification ratio for given class
    
    parameters:
            class_name: string, the target class (right label)
            model: CNN model object
            roi_dst_dir: string, the path of the target folder want to do the test
            CI_level: integer, the confident level we want to use for classification deicision  
            display_misclassification_images: boolean, the default value is false
    """

    # read test dataset 
    directory = os.listdir(roi_dst_dir)
    image_list = list(directory)
    image_count = len(image_list) 
 
    ## start to test images
    mis_count = 0
    right_count = 0
    for image in directory:
        image = roi_dst_dir + image 
        picture = Image.open(image)
        img = keras.preprocessing.image.load_img(
            image, target_size=(img_height, img_width)
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        
        # creat a directory to collect the misclassification result
        result_dir = {}
        
        if 100*max(score) < CI_level:
            if class_name == "other":
                right_count +=1
                
            elif "other" not in result_dir:
                result_dir["other"] = 1
                mis_count +=1 # this fail can be prevent
                # display the misclassified images
                #if display_misclassification_images:
                    #draw_misclassification_images(image, class_name, class_names[np.argmax(score)],picture, image)
            else:
                result_dir["other"] +=1
                mis_count +=1 # this fail can be prevent
                # display the misclassified images
                #if display_misclassification_images:
                    #draw_misclassification_images(image, class_name, class_names[np.argmax(score)],picture, image)
        
        if 100*max(score) >= CI_level:
            
            if class_names[np.argmax(score)] == class_name: # correct label
                right_count +=1
            
            elif class_names[np.argmax(score)] != class_name: # miss classification
                if class_names[np.argmax(score)] not in result_dir:
                    result_dir[class_names[np.argmax(score)]] = 0
                result_dir[class_names[np.argmax(score)]] +=1
                mis_count +=1
                
                # display the misclassified images
                if display_misclassification_images:
                    #print(score)
                    #print(100*max(score))
                    draw_misclassification_images(image, class_name, class_names[np.argmax(score)], picture, image)
                
    # display test result
    print("Test {} images on class {}, misclassification ratio is {}".format(image_count, class_name, round(mis_count/image_count, 2)));
    
                
def draw_misclassification_images(image, class_name, predicted_class, picture, image_path):
    """
    draw the misclassification images produced by the test function  
    """
    
    print("Image:", str(image).split('/')[-1])
    print("True class: ", class_name)
    print("Predicted class:", predicted_class)
            
    draw = ImageDraw.Draw(picture)

    # display image
    pil_im = Image.open(image_path, 'r')
    display(pil_im)

    print("\n\n")
