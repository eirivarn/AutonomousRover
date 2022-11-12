from Utils import *
#from picamera.array import PiRGBArray
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


    def analyzeImage(self, image):
        
        removedBgImg = RemoveBackground(image, True)
        direction = 0

        line = []
        
        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
                line.append(self.images[i].getDir())    ##TODO usikker på om getDir eller getOffset er riktig
            
            repackedImg = RepackImages(self.images)
        
        printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
            self.rawCapture.truncate(0)

        return line #TODO    skal returne line - liste av avstand fra linje til senter av bildet

    def quit(self):
        cv2.destroyAllWindows()