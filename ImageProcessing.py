import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

IMG_PATH = os.getcwd() + os.sep + 'img'
IMG_SIZE = (2880, 1618) # 16 : 9

def loadImgs(nameList, size=IMG_SIZE, color=False):
    # params: nameList, size=(2880, 1618), color=False
    # return: list of imgs

    # may fix if change to load from clound
    imgs = list()
    for i in range(len(nameList)):
        temp = cv2.imread(nameList[i], color)
        temp = cv2.resize(temp, IMG_SIZE)
        temp = threshold(temp, 127)
        imgs.append(temp)
    return imgs

def threshold(img, min_threshold, max_threshold=255, mode=cv2.THRESH_BINARY):
    # params: img, min_threshold, max_threshold=255, mode=cv2.THRESH_BINARY
    # return: thresholded img
    # THRESH_BINARY 1/0
    # THRESH_BINARY_INV 0/1
    # THRESH_TRUNC thres/src
    # THRESH_TOZERO src/0
    # THRESH_TOZERO_INV 0/src
    ret, thresh = cv2.threshold(img, min_threshold, max_threshold, mode)
    return thresh

def bitwiseAnd(imgs):
    # params: list of imgs
    # return: bitwise_and img
    if len(imgs) == 0: raise Exception('connot operate bitwise_and for empty list')
    if len(imgs) == 1: return imgs[0]
    return cv2.bitwise_and(imgs[0], bitwiseAnd(imgs[1:]))

def countDeadChicken(imgs):
    # params: List of images
    # return: list of {center, area}

    # bitwise_and imgs
    img = bitwiseAnd(imgs)

    temp = img.copy()

    # opening: removing minor noise
    kernel = np.ones((2,2), np.uint8)
    opening = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel)
    temp = opening

    # erosion: removing major noise
    # open again to clean the image
    kernel = np.ones((2,2), np.uint8)
    erosion = cv2.erode(temp, kernel, iterations = 5)
    temp = erosion
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel)
    temp = opening

    # closing: filling hole
    # may not be neccessary
    kernel = np.ones((2,2), np.uint8)
    closing = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
    temp = closing

    # find contour
    cnts = list()
    contours, hierarchy = cv2.findContours(temp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < getThresholdArea() : continue
        
        M = cv2.moments(cnt) 
        cx = round(M["m10"] / M["m00"],3)
        cy = round(M["m01"] / M["m00"],3)

        contours, hierarchy = cv2.findContours(temp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        t = {
            'cnt': cnt,
            'area': area,
            'center': (cx, cy)
        }
        cnts.append(t)
    return cnts

def getThresholdArea():
    # return threshold area
    # minimum area accepted computed from chicken age (date - filled_date)
    return 7000
