"""
OpenCV module for Color-based object detection for shenzhen images

Date: Nov 2020
Author: Yuanda Dong, Yiran Jing
Group: CP32-17b1 (COMP3988 group 1)
"""


import cv2
import numpy as np
import platform
import os
import matplotlib.pyplot as plt
import tempfile
import time
import sys
import shutil
import glob

import config as cfg

## FILTERS

# red filter for stop sign
lower_red_stop = np.array([160, 75, 50])   #red filter (same as cian's)
upper_red_stop = np.array([180, 255, 255])   #red filter (same as cian's)

lower_red2_stop = np.array([0, 150, 100])   #red filter (same as cian's)
upper_red2_stop = np.array([10, 255, 255])   #red filter (same as cian's)


# blue filter for turn arrow
lower_blue_sign = np.array([90, 70, 40])    # relaxed blue filter good (cian's))
upper_blue_sign = np.array([140, 255, 255])   #blue filter good

lower_blue_sign2 = np.array([110,30,110])     #blue filter good
upper_blue_sign2 = np.array([160, 255, 255])   #blue filter good

lower_blue_sign_bgr =  np.array([50,0,0])
upper_blue_sign_bgr =  np.array([255,15,15])

lower_white_sign = np.array([0, 0, 150])     #hsv filter good
upper_white_sign = np.array([255, 55, 255])   #hsv filter good


# green filter for park sign
lower_green_park = np.array([60, 55, 55])   #green filter
upper_green_park = np.array([90, 130, 150])   #green filter


c= np.array([179, 55, 153])

canny_low = 50#100
canny_upper = 150#200


# set kernel for operations
kernel = np.ones((cfg.KERNEL_SIZE,cfg.KERNEL_SIZE), np.uint8) # cfg.KERNEL_SIZE = 3
stop_kernel = np.ones((cfg.STOP_KERNEL_SIZE,cfg.STOP_KERNEL_SIZE), np.uint8)

def is_squarish(height, width):
    # calculate ratio of sides - anything not square is not worth checking
    a = height / width
    b = width / height

    if (0.5 < a < 2.0) and (0.5 < b < 2.0):
        return True
    else:
        return False


def collect_contours_area(contours, frame):

    rect = None
    sub_rois = []
    for cnt in contours:
  
        x,y,w,h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        #if area > cfg.AREA_SIZE_TURN or area > cfg.AREA_SIZE_STOP:
        if area>100 and area < 2000: # the upper bound and lower bound of interested area
            rect = cv2.boundingRect(cnt)
            x,y,w,h = rect
            roi = frame[y:y+h, x:x+w]
            sub_rois.append([roi, area])
            
    return sub_rois




def detect_red(frame, hsv):
    """
     Expects: HSV image of any shape + current frame
     Returns: the ROI with the biggest area
    """
    mask_red = cv2.inRange(hsv, lower_red_stop, upper_red_stop)
    mask_red2 = cv2.inRange(hsv, lower_red2_stop, upper_red2_stop)
    mask = mask_red + mask_red2
   
    mask = cv2.GaussianBlur(mask, (3,3), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # find shapes
    # contours detection
    height, width = mask.shape[:2]
    cfg.ROOF = int(height*cfg.ROOF_R)
    cfg.HORIZON = int(height*cfg.HORIZON_R)
    contours, _ = cv2.findContours(mask[:cfg.HORIZON, :width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # collect all interested areas
    sub_rois = collect_contours_area(contours, frame)
    
    if len(sub_rois) >0:
        return sub_rois, True
    
    return frame, False


def detect_blue(frame, hsv):
    """
     Reference Cian's code 
     Expects: HSV image of any shape + current frame
     Returns: TBD
    """
    maskfilter = cv2.inRange(frame, lower_blue_sign, upper_blue_sign)
    maskfilter_white = cv2.inRange(hsv, lower_white_sign, upper_white_sign)
    
    mask = maskfilter + maskfilter_white
    
    # operations
    mask = cv2.dilate(maskfilter, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    img = cv2.bitwise_and(frame,frame,mask = mask)
    
    # logic
    # contours detection
    height, width = mask.shape[:2]
    #contours, _ = cv2.findContours(mask[0:int(height/2), 0:width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(mask[0:int(height), 0:width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    sub_rois = []
    # collect all interested areas
    sub_rois = collect_contours_area(contours, frame)
    
    if len(sub_rois) >0:
        return sub_rois, True
    
    return frame, False


def detect_blue1(frame, hsv):
    """
    reference group cp31 code
    detect the blue color sign
    """
    mask = cv2.inRange(hsv, lower_blue_sign2, upper_blue_sign2)
    
    mask = cv2.GaussianBlur(mask, (5,5), 0)
    #mask = cv2.GaussianBlur(mask, (3,3), 0)
    
    maskfilter = cv2.inRange(frame, lower_blue_sign_bgr, upper_blue_sign_bgr)
    # operations
    mask = cv2.dilate(maskfilter, kernel, iterations=1)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations=1)

    # drawing boundaries for debugging
    height, width = mask.shape[:2]
    cfg.HORIZON = int(height*cfg.HORIZON_R)
    cfg.ROOF = int(height*cfg.ROOF_R)

    img_mask = cv2.bitwise_and(frame,frame,mask = mask)
    img_gray = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (5,5), 0)

    output = frame.copy()
    circle = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1.3, 120)
    if circle is not None:
        circle = np.round(circle[0, :]).astype("int")
        for (x, y, r) in circle:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    # cv2.imshow("output", np.hstack([frame, output]))

    contours, _ = cv2.findContours(mask[0:cfg.HORIZON, 0:width], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # collect all interested areas
    sub_rois = collect_contours_area(contours, frame)
    
    if len(sub_rois) >0:
        return sub_rois, True
    
    return frame, False


    


def detect_green(frame, hsv):
    """
    Green sign detection
    """
   
    mask_green = cv2.inRange(hsv, lower_green_park, upper_green_park)

    mask = mask_green

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations=1)

    # contours detection
    height, width = mask.shape[:2]
    cfg.ROOF = int(height*cfg.ROOF_R)
    cfg.HORIZON = int(height*cfg.HORIZON_R)

    contours, _ = cv2.findContours(mask[0:cfg.HORIZON, 0:width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    # cv2.drawContours(frame, contours, -1, (255,0,0), 1)
    sub_rois = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if cfg.AREA_SIZE_PARK < area < cfg.MAX_AREA_SIZE:
        #if cfg.AREA_SIZE_PARK < area 
            x,y,w,h = cv2.boundingRect(cnt)

            # calculate ratio of sides - anything not square is not worth checking
            sr = is_squarish(h, w)
            if not sr:
                continue
            
            roi = frame[y:y+h, x:x+w]
            sub_rois.append([roi, area])
     
    if(len(sub_rois) > 0):
        return sub_rois, True
    
    return frame, False



def detect_interested_area(frame):
    """
    Expect to detect the interest area
    Then run it using TF model 
    
    Parameter: 
        frame: the frame of input image
        
    Return:
        rois: the extract interesed areas
        result: true or false
    """
    
    # convert image to hsv
    try: # skip errors
        hsv = cv2.cvtColor(frame, cfg.COLOUR_CONVERT) 
    except:
        return frame, False
    
    rois = []; # collect all rois
    
    ## test on multiple masks
    sub_rois, result = detect_red(frame, hsv)
    if result:
        rois.extend(sub_rois)
        
    sub_rois, result = detect_blue(frame, hsv) # blue-turnning sign method 1
    if result:
        rois.extend(sub_rois)
        
    sub_rois, result = detect_blue1(frame, hsv) # blue-turnning sign method 2
    if result:
        rois.extend(sub_rois)
    
    sub_rois, result = detect_green(frame, hsv)
    if result:
        rois.extend(sub_rois)
    
        
    # return all rois
    if (len(rois) > 0):
        return rois, True
    
    return frame, False



def create_or_empty_dir(dir_name):
    """
    helper function for test_images
    
    create the folder if the given folder path not exits,
    clean the old foler if it already exist.
    """
    #dir_name = "test"

    if (os.path.exists(dir_name)):
        # `tempfile.mktemp` Returns an absolute pathname of a file that
        # did not exist at the time the call is made. We pass
        # dir=os.path.dirname(dir_name) here to ensure we will move
        # to the same filesystem. Otherwise, shutil.copy2 will be used
        # internally and the problem remains.
        tmp = tempfile.mktemp(dir=os.path.dirname(dir_name))
        # Rename the dir.
        #shutil.move(dir_name, tmp)
        # And delete it.
        shutil.rmtree(dir_name)


    # At this point, even if tmp is still being deleted,
    # there is no name collision.
    os.makedirs(dir_name)



def load_images_from_folder(folder):
    """
    Load all images within the given folder
    
    Return:
        the list of images path
    """
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            #images.append(img)
            images.append(os.path.join(folder,filename))
    return images


def save_roi_images(roi_dst_dir, image, image_name):
    """
    Save the roi to the dst_dir
    """
    os.chdir(directory)
    # Saving the image 
    cv2.imwrite(filename, img) 
    

def test_images(folder_path, roi_dst_dir, num_visualize = 0):
    """
    Test the success rate of detecting the interested area of the images in the given folder
    And save the roi to the dst_dir
    
    Parameter: 
        folder_path: the input image folder path
        roi_dst_dir: the desired path for roi collection
        num_visualize: the number of detected images we want to visualize to check the result
    """
    count_success = 0
    count_fail = 0
    fail_image_collection = []
    printfirst = 0
    
    # create a directory and overwrite an existing one
    create_or_empty_dir(roi_dst_dir);
    
    # load images and check one by one
    for filename in os.listdir(folder_path):
        # read image
        image = os.path.join(folder_path, filename)
        frame = cv2.imread(image)
        # test based on multiple mask
        
        rois, result = detect_interested_area(frame)
        
        ## Test result
        if not result:
            count_fail += 1
            fail_image_collection.append(image)
            continue;
        
        count = 1;
        count_success += 1
        for roi in rois:
        
            # cfg.DEMO_MODE is used for debugging
            if cfg.DEMO_MODE and printfirst < num_visualize:
            
                plt.imshow(cv2.cvtColor(roi[0], cv2.COLOR_BGR2RGB)) # opencv loads in BGR format by default, we want to show it in RGB.
                plt.show()
                printfirst +=1
            
            # save the successfully detected images
            roi_path = roi_dst_dir +str(count)+"_" + filename
            cv2.imwrite(roi_path, roi[0])
            count += 1
    
    success_rate = (count_success/(count_success + count_fail))
        
    return fail_image_collection, success_rate 





def save_fail_iamges(fail_image_collection, dst_dir):
    """
    Save the fail images to the given folder (dst_dir)

    parameters:
        fail_image_collection: the list of fail images
        dst_dir: the direct path we want to used to save the fail images
    """
    ## lets see the fail image
    for image in fail_image_collection:
        frame = cv2.imread(image)

        # collect to another folder
        jpgfile = glob.iglob(image)
        shutil.copy(image, dst_dir)
