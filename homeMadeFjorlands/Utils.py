import numpy as np
import cv2
import time
from Image import *

def SlicePart(img, images, slices):
    height, width = img.shape[:2]
    sl = int(height/slices)
    
    for i in range(slices):
        part = sl*i
        crop_img = img[part:part+sl, 0:width]
        images[i].setImage(crop_img)
        images[i].Process()
    
def RepackImages(images):
    img = images[0].getImage()
    for i in range(len(images)):
        if i == 0:
            img = np.concatenate((img, images[1].getImage()), axis=0)
        if i > 1:
            img = np.concatenate((img, images[i].getImage()), axis=0)
            
    return img

def Center(moments):
    if moments["m00"] == 0:
        return 0
        
    x = int(moments["m10"]/moments["m00"])
    y = int(moments["m01"]/moments["m00"])

    return x, y
    
def RemoveBackground(image, b):
    up = 100
    # create NumPy arrays from the boundaries
    lower = np.array([0, 0, 0], dtype = "uint8")
    upper = np.array([up, up, up], dtype = "uint8")
    #----------------COLOR SELECTION-------------- (Remove any area that is whiter than 'upper')
    if b == True:
        mask = cv2.inRange(image, lower, upper)
        image = cv2.bitwise_and(image, image, mask = mask)
        image = cv2.bitwise_not(image, image, mask = mask)
        image = (255-image)
        return image
    else:
        return image
    #////////////////COLOR SELECTION/////////////


#/////////////////prettyPrint///////////////
def printInfo(images):
    i = 0
    mainString ={}
    for image in images:
        area, w, offset = image.getMainContourInfo()
        dir = image.getDir()
        crossFound = ''
        if image.crossFound():
            crossFound = 'CROSS!'
        mainString[i] = [dir, area, w, offset, crossFound]
        i += 1

    print ("\n{:<8} {:<15} {:<15} {:<15} {:<15} {:<15}".format('i','Dir','Area','Width', 'Distance', 'Corss'))
    for k, v in mainString.items():
        dir, area, w, offset, crossFound = v
        print ("{:<8} {:<15} {:<15} {:<15} {:<15} {:<15}".format(k, dir, area, w, offset, crossFound))    
    

def crossFound(images):
    crossLocation = [0,0,0,0]
    for i in range(3):
        if images[i].crossFound():
            crossLocation[i] = 1 

    return  crossLocation
