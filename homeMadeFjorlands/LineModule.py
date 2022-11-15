from Utils import *
import cv2
from Image import Image
import numpy as np


class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.const = const

        self.m = 0
        self.c = 0

        for _ in range(self.N_SLICES):
            self.images.append(Image(const),)        


    def analyzeImage(self, image):
        removedBgImg = RemoveBackground(image, True)
        direction = 0
        atCross = False
        list = []
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
                list.append(self.images[i].getOffset()) 
                if self.images[i].crossFound():
                    self.robot.updateCrossConf(i)
            repackedImg = RepackImages(self.images)

        ##/////////Making LinReg line
        x = []
        y = []
        for i in range(self.N_SLICES):
            y.append(self.const.resolution[1]*i/4 + self.const.resolution[1]/4)

        x = np.array(list)
        y = np.array(y)

        A = np.vstack([x, np.ones(len(x))]).T
        self.m, self.c = np.linalg.lstsq(A, y, rcond=None)[0]

        line = []
        for i in range(self.N_SLICES):
            line.append(self.predict(i))
        
        angle = np.arctan((self.predict(line[1]) - self.predict(line[0]))/120)
        offset = self.predict(self.const.resolution[1]/2)

        ##////////Printing linReg line
        x0, y0 = int(self.predict(line[0])), int(y[0])
        x1, y1 = int(self.predict(line[3])), int(y[1])

        image = repackedImg
        line_thickness = 2
        cv2.line(image, (x0, y0), (x1, y1), (255, 32, 0), thickness=line_thickness)

        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()


        ##///////////Printing information
        print ("\n{:<8} {:<15} {:<15} ".format('Angle','Offset', 'Cross'))
        print ("{:<8} {:<15} {:<15} ".format("{0:.3f}".format(angle), "{0:.3f}".format(offset), atCross))   

        return line, atCross, angle, offset

    def predict(self, x):
        return self.m*x + self.c

    def quit(self):
        cv2.destroyAllWindows()