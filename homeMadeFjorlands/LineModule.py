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
        #differentiate black black areas
        blackAreas = cv2.inRange(image, (0,0,0), (50,50,50))
        blackAreas = self.improveLine(blackAreas)
        blackContours, hierarchy = cv2.findContours(blackAreas.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(blackContours) > 0:
            c = max(blackContours, key=cv2.contourArea) #biggest black contour area
            xb, yb, wb, hb = cv2.boundingRect(c) #bounding box rectangle
            contourbox = cv2.minAreaRect(c) #contour tape rectangle
            (xc, yc), (wc,hc), angle = contourbox
            #determine angle and lateral offset
            angle = self.preProcessAngle(angle,wc,hc)
            lateralOffset = int(320-xb-wb/2)
            
            self.controller.setAngLDist(int(angle), int(lateralOffset))
            
            #Write boxes and lines to image
            cv2.rectangle(image,(xb,yb),(xb+wb,yb+hb),(0,255,0),2) #Bounding box
            cv2.line(image, (int(xb+wb/2), yb), (int(xb+wb/2), yb+hb),(0,255,0), 2) #bounding box centerline
            cv2.line(image,(int(xb+wb/2), int(yb+hb/2)), (320, int(yb+hb/2)),(0,0,255), 1)# distance line
            cv2.line(image, (320, 10), (320, 350),(0,0,255), 1)#center line
            cv2.drawContours(image, [np.int0(cv2.boxPoints(contourbox))],0,(255,0,0), 2)#draw contourBox
            cv2.putText(image, f"{str(int(angle))}deg", (360,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#text>
            cv2.putText(image, str(lateralOffset)+"dist", (360,330),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#te>
            cv2.drawContours(image, blackContours,-1,(0,0,255),1)
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