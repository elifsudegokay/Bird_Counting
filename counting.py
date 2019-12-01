# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:58:06 2019

@author: elifs
"""

from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage

import cv2
import numpy as np


def preprocess(image_path):
    image = image_path
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
    image = cv2.GaussianBlur(image,(5,5),0)
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresholding = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    return thresholding

def counting(pp_image, minDistance):
    
    D = ndimage.distance_transform_edt(pp_image)
    localMax = peak_local_max(D, indices = False, min_distance = minDistance,labels = pp_image)
    markers = ndimage.label(localMax, structure = np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask = pp_image)
    count = len(np.unique(labels)) - 1
    return count

def count_birds(image_path, min_distance):
    
    threshoulding = preprocess (image_path)
    count = counting(threshoulding, min_distance)
    
    return count

