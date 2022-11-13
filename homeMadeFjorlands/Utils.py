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

def improveLine(pic):
        kernel = np.ones((3,3),np.uint8)
        pic = cv2.erode(pic, kernel, iterations=4)
        pic = cv2.dilate(pic, kernel, iterations=4)
        return pic
    
def preProcessAngle(ang, w, h):
    if ang > 45 and w>h:
        ang = -(90-ang)
    elif ang <= 45 and h<w:
        ang = -(90-ang)
    return ang



def ekstraBox(image):
    #differentiate black black areas
        blackAreas = cv2.inRange(image, (0,0,0), (50,50,50))
        blackAreas = improveLine(blackAreas)
        blackContours, hierarchy = cv2.findContours(blackAreas.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(blackContours) > 0:
            c = max(blackContours, key=cv2.contourArea) #biggest black contour area
            xb, yb, wb, hb = cv2.boundingRect(c) #bounding box rectangle
            contourbox = cv2.minAreaRect(c) #contour tape rectangle
            (xc, yc), (wc,hc), angle = contourbox
            #determine angle and lateral offset
            angle = preProcessAngle(angle,wc,hc)
            lateralOffset = int(320-xb-wb/2)
            
            #Write boxes and lines to image
            cv2.rectangle(image,(xb,yb),(xb+wb,yb+hb),(0,255,0),2) #Bounding box
            cv2.line(image, (int(xb+wb/2), yb), (int(xb+wb/2), yb+hb),(0,255,0), 2) #bounding box centerline
            cv2.line(image,(int(xb+wb/2), int(yb+hb/2)), (320, int(yb+hb/2)),(0,0,255), 1)# distance line
            cv2.line(image, (320, 10), (320, 350),(0,0,255), 1)#center line
            cv2.drawContours(image, [np.int0(cv2.boxPoints(contourbox))],0,(255,0,0), 2)#draw contourBox
            cv2.putText(image, f"{str(int(angle))}deg", (360,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#text>
            cv2.putText(image, str(lateralOffset)+"dist", (360,330),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#te>
            cv2.drawContours(image, blackContours,-1,(0,0,255),1)
            return angle, lateralOffset
            
    


##/////////////////prettyPrint///////////////
#def printInfo(images):
#    i = 0
#    mainString ={}
#    for image in images:
#        area, w, offset = image.getMainContourInfo()
#        dir = image.getDir()
#        crossFound = ''
#        if image.crossFound():
#            crossFound = 'CROSS!'
#        mainString[i] = [dir, area, w, offset, crossFound]
#        i += 1
#
#    print ("\n{:<8} {:<15} {:<15} {:<15} {:<15} {:<15}".format('i','Dir','Area','Width', 'Distance', 'Corss'))
#    for k, v in mainString.items():
#        dir, area, w, offset, crossFound = v
#        print ("{:<8} {:<15} {:<15} {:<15} {:<15} {:<15}".format(k, angle, area, w, lateralOffset, crossFound))    
#    
#
def crossFound(images):
    crossLocation = [0,0,0,0]
    for i in range(3):
        if images[i].crossFound():
            crossLocation[i] = 1 

    return  crossLocation
