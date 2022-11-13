from Utils import *
import cv2
from Image import Image


class LineModule:
    def __init__(self, isHeadless):
        self.isHeadless = isHeadless
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.crossTracker = [[],[],[],[]]
        
        for _ in range(self.N_SLICES):
            self.images.append(Image())        


    def analyzeImage(self, image):
        removedBgImg = RemoveBackground(image, True)
        direction = 0
        atCross = False
        line = []
        self.crossTracker.pop(0)
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
                line.append(self.images[i].getDir()) ##TODO usikker på om getDir eller getOffset er riktig
            repackedImg = RepackImages(self.images)

        ekstraBox(self, repackedImg)
        printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        crossLocation = crossFound(self.images)
        self.crossTracker.append(crossLocation)

        if self.crossTracker == [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]:
            atCross = True
        return line, atCross 

    def quit(self):
        cv2.destroyAllWindows()