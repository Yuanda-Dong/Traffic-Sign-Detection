'''
OpenCV module for Color-based object detection for unity map

Date: Nov 2020
Author: Yuanda Dong, Yiran Jing
Group: CP32-17b1 (COMP3988 group 1)

'''

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
import tensorflow as tf
import config as cfg


## FILTERS
# red filter for stop sign
lower_red_stop = np.array([160, 75, 50])   #red filter
upper_red_stop = np.array([180, 255, 255])   #red filter

lower_red2_stop = np.array([6, 150, 100])   #red filter
upper_red2_stop = np.array([10, 255, 255])   #red filter

# green filter for park sign
lower_green_park = np.array([43, 180, 130])   #green filter
upper_green_park = np.array([46, 255, 255])   #green filter

# yello filter for park sign
lower_yello_park = np.array([25, 190, 165])   #yellow filter
upper_yello_park = np.array([29, 255, 255])   #yellow filter

# blue filter for turn arrow
lower_blue_sign = np.array([90,190,150])     #blue filter good
upper_blue_sign = np.array([120, 255, 255])   #blue filter good

lower_black_sign = np.array([95,6,40])
upper_black_sign = np.array([115,55,90])

lower_white_sign = np.array([0, 0, 150])     #hsv filter good
upper_white_sign = np.array([255, 55, 255])   #hsv filter good
lower_white_sign2 = np.array([91, 10, 126])
upper_white_sign2 = np.array([133, 67, 161])

lower_blue_sign_bgr =  np.array([50,0,0])
upper_blue_sign_bgr =  np.array([255,15,15])

lower_orange_cone = np.array([0,60,60])
upper_orange_cone = np.array([10,180,120])
lower_orange2_cone = np.array([170,60,60])
upper_orange2_cone = np.array([180,180,120])

my_hsv_lower = np.array([100, 100, 30]) #for regular turn
my_hsv_upper = np.array([125, 255, 160]) #for regular turn

pent_turn_lower  = np.array([20, 0, 121]) #for penta turn
pent_turn_upper = np.array([179, 55, 153])

canny_low = 50#100
canny_upper = 150#200


# set kernel for operations
kernel = np.ones((cfg.KERNEL_SIZE,cfg.KERNEL_SIZE), np.uint8)
stop_kernel = np.ones((cfg.STOP_KERNEL_SIZE,cfg.STOP_KERNEL_SIZE), np.uint8)


def is_squarish(height, width):
    # calculate ratio of sides - anything not square is not worth checking
    a = height / width
    b = width / height

    if (0.5 < a < 2.0) and (0.5 < b < 2.0):
        return True
    else:
        return False

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

    # find the largest contour first that fits all our conditions.
    largest_area = -1
    rect = None
    largest_cnt = None
    for cnt in contours:
        
        # calculate the area of current cnt
        area = cv2.contourArea(cnt)
        
        # determine the size allowed
        if area > largest_area and area > cfg.AREA_SIZE_STOP and area < cfg.MAX_AREA_SIZE:
            largest_area = area
            largest_cnt = cnt
            rect = cv2.boundingRect(cnt)
    
    # found at least one rect that fits the conditions
    if largest_area > 0:
        # capture a ROI image and store for later
        x,y,w,h = rect
        roi = frame[y:y+h, x:x+w] 
        return roi, largest_area, True,rect
    
    return frame, 0, False,None # fail to find any


##TURN DETECTION
def detect_blue(frame, hsv):
  
    mask = cv2.inRange(hsv, lower_blue_sign, upper_blue_sign)

    mask = cv2.GaussianBlur(mask, (5,5), 0)
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

    # find the largest contour first that fits all our conditions.
    largest_area = -1
    rect = None


    for cnt in contours:
        
        
        x,y,w,h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        if area > largest_area and area > cfg.AREA_SIZE_TURN and area < cfg.MAX_AREA_SIZE:
            largest_area = area
            rect = cv2.boundingRect(cnt)

    # if we found an region of interest that fits the conditions
    if largest_area > 0:

        x,y,w,h = rect
        roi = frame[y:y+h, x:x+w]
        return roi, largest_area, True, rect
    
    return frame, 0, False, None


##PARK DETECTION
def detect_green_yellow(frame, hsv):
    # convert to HSV image
    #this code just doesnt work because of version issues apparently, commenting it out of part.py until we can test it in isolatio
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_green = cv2.inRange(hsv, lower_green_park, upper_green_park)
    mask_yellow = cv2.inRange(hsv, lower_yello_park, upper_yello_park)

    mask = mask_green + mask_yellow
    # mask = mask_yellow

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations=1)


    #img = cv2.bitwise_and(frame,frame,mask = mask)
    # cv2.imshow("mask", img)
    # cv2.waitKey(1)
    # find shapes
    # contours detection
    height, width = mask.shape[:2]
    cfg.ROOF = int(height*cfg.ROOF_R)
    cfg.HORIZON = int(height*cfg.HORIZON_R)

    contours, _ = cv2.findContours(mask[0:cfg.HORIZON, 0:width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    # cv2.drawContours(frame, contours, -1, (255,0,0), 1)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        #if cfg.AREA_SIZE_PARK < area < cfg.MAX_AREA_SIZE:
        if cfg.AREA_SIZE_PARK < area and area < cfg.MAX_AREA_SIZE:
            rect = cv2.boundingRect(cnt)
            x,y,w,h = rect
            # calculate ratio of sides - anything not square is not worth checking
            sr = is_squarish(h, w)
            if not sr:
                continue
            
            roi = frame[y:y+h, x:x+w]
            
            return roi, area, True, rect 

    return frame, 0, False, None

def detect_black(frame, hsv):
    """
     Expects: HSV image of any shape + current frame
     Returns: the ROI with the biggest area
    """
    mask = cv2.inRange(hsv, lower_black_sign, upper_black_sign)
   
    mask = cv2.GaussianBlur(mask, (3,3), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # find shapes
    # contours detection
    height, width = mask.shape[:2]
    cfg.ROOF = int(height*cfg.ROOF_R)
    cfg.HORIZON = int(height*cfg.HORIZON_R)
    contours, _ = cv2.findContours(mask[:cfg.HORIZON, :width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # find the largest contour first that fits all our conditions.
    largest_area = -1
    rect = None
    largest_cnt = None
    for cnt in contours:
        
        # calculate the area of current cnt
        area = cv2.contourArea(cnt)
        
        # determine the size allowed
        if area > largest_area and area > cfg.AREA_SIZE_STOP and area < cfg.MAX_AREA_SIZE:
            largest_area = area
            largest_cnt = cnt
            rect = cv2.boundingRect(cnt)
    
    # found at least one rect that fits the conditions
    if largest_area > 0:
        # capture a ROI image and store for later
        x,y,w,h = rect
        roi = frame[y:y+h, x:x+w] 
        return roi, largest_area, True, rect
    
    return frame, 0, False, None # fail to find any


def detect_white(frame, hsv):
    # convert to HSV image
    """
    这个function好像可以删掉
    """

    mask = cv2.inRange(hsv, lower_white_sign2, upper_white_sign2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations=1)

    #img = cv2.bitwise_and(frame,frame,mask = mask)
    # contours detection
    height, width = mask.shape[:2]
    cfg.ROOF = int(height*cfg.ROOF_R)
    cfg.HORIZON = int(height*cfg.HORIZON_R)

    contours, _ = cv2.findContours(mask[0:cfg.HORIZON, 0:width], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        #if cfg.AREA_SIZE_PARK < area < cfg.MAX_AREA_SIZE:
        if cfg.AREA_SIZE_PARK < area:
            rect = cv2.boundingRect(cnt)
            x,y,w,h = rect 
            # calculate ratio of sides - anything not square is not worth checking
            sr = is_squarish(h, w)
            if not sr:
                continue
                
            roi = frame[y:y+h, x:x+w]
            return roi, area, True,rect

    return frame, 0, False, None


def detect_interested_area(frame):
    """
    Expect to detect the interest area
    Then run it using TF model 
    
    Parameter: 
        image: the path of the image
        
    Return:
        roi: the extract interesed area
        result: true or false
    """
    
    # convert image to hsv
    try: # skip errors
        hsv = cv2.cvtColor(frame, cfg.COLOUR_CONVERT) 
    except:
        return frame, False,None
    
    rois = []; # collect all rois
    ## test on multiple maks
    roi, area, result, rect = detect_red(frame, hsv)
    if result:
        rois.append([roi, area, rect])
    
    roi, area, result, rect = detect_blue(frame, hsv)
    if result:
        rois.append([roi, area, rect])

    roi, area, result, rect = detect_black(frame, hsv)
    if result:
        rois.append([roi, area, rect])
    
    roi, area, result, rect = detect_green_yellow(frame, hsv)
    if result:
        rois.append([roi, area, rect])
    
    # roi, area, result,rect = detect_white(frame, hsv)
    # if result:
    #     #print("detect_red return result");
    #     #return roi, True
    #     rois.append([roi, area,rect])
        
    # find the roi with the largest area. return it
    if (len(rois) > 0):
        # seek the roi with largest area
        max_roi, i = find_max_roi(rois)
        #max_roi = tf.image.resize(max_roi, [100,100])   
        rect = rois[i][2] # save rect
        
        return max_roi, True, rect 
    
    return frame, False, None


def find_max_roi(rois):
    """
    helper function for detect_interested_area
    
    find and retain the roi with the max area
    """
    # seek the roi with largest area
    i = 0
    max_roi = rois[i][0]
    max_area = rois[i][1]
    
    for i in range(1, len(rois)):
        if rois[i][1] > max_area:
            max_area = rois[i][1]
            max_roi = rois[i][0]
    
    return max_roi, i
    
    

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
        roi, result, rect = detect_interested_area(frame)
        
        ## Test result
        if not result:
            count_fail += 1
            fail_image_collection.append(image)
        
        else:
            count_success += 1
        
            # cfg.DEMO_MODE is used for debugging
            if cfg.DEMO_MODE and printfirst < num_visualize:
            
                plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)) # opencv loads in BGR format by default, we want to show it in RGB.
                plt.show()
                printfirst +=1
            
            # save the successfully detected images
            roi_path = roi_dst_dir + filename
            cv2.imwrite(roi_path, roi) 
    
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
