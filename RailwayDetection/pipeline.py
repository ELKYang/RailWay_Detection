import os
import cv2
import utils
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoFileClip
import line
from PIL import Image
import time


def roi_mask(img, vertices):
    #定义mask全为黑
    mask = np.zeros_like(img)
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    mask_color = 255
    #将区域和图片进行填充fillPoly和叠加and
    cv2.fillPoly(mask, vertices, mask_color)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img


def thresholding(img):
    img=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.Canny(img, 25, 80)
    roi_vtx = np.array([[(465,720), (590, 470), (635, 470),(720, 720)]])
    threshholded=roi_mask(img,roi_vtx)
    threshholded=cv2.morphologyEx(threshholded,cv2.MORPH_CLOSE,kernel=(5,5),iterations=3)
    return threshholded

def RotateClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip(trans_img, 1)
    return new_img

def processing(img,M,Minv,left_line,right_line):
    img = Image.fromarray(img)
    undist = img
    #get the thresholded binary image
    img = np.array(img)
    thresholded = thresholding(img)
    #perform perspective  transform
    thresholded_wraped = cv2.warpPerspective(thresholded, M, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    
    #perform detection
    left_fit, right_fit, left_lane_inds, right_lane_inds = utils.find_line(thresholded_wraped)
    left_line.update(left_fit)
    right_line.update(right_fit)

    #draw the detected laneline and the information
    undist = Image.fromarray(img)
    area_img, gre1 = utils.draw_area(undist,thresholded_wraped,Minv,left_fit, right_fit)
    area_img = np.array(area_img)
    result = utils.draw_text(area_img)
    return result,thresholded_wraped


left_line = line.Line()
right_line = line.Line()
M,Minv = utils.get_M_Minv()


#draw the processed test image
test_imgs = utils.get_images_by_dir('./video/194526AA')

undistorted = []
for img in test_imgs:
    undistorted.append(img)
result=[]
t2=[]
c=1
time_sum=0
for img in undistorted:
    prev_time = time.time()
    res,t1 = processing(img,M,Minv,left_line,right_line)
    curr_time = time.time()
    exec_time = curr_time - prev_time
    time_sum+=(exec_time*1000)
    info = "time: %.2f ms" % (1000 * exec_time)
    print(info)
    cv2.imwrite('./video/194526AA_detected/'+str(c)+'.jpg',res)
    c = c + 1
print("averge_time_perImg:{}ms".format(time_sum/c))