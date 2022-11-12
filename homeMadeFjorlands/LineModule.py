import time
from Utils import *
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from Image import Image


class LineModule:
    def __init__(self, isHeadless):
        self.isHeadless = isHeadless
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        for _ in range(self.N_SLICES):
            self.images.append(Image())

        self.info = None   #TODO lag get info funk
        


    def analyzeImage(self, image):
        
        removedBgImg = RemoveBackground(image, True)
        direction = 0
        
        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
            
            repackedImg = RepackImages(self.images)
        
        printInfo(self.images)

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        self.rawCapture.truncate(0)

        return self.info  #TODO

    def quit(self):
        cv2.destroyAllWindows()