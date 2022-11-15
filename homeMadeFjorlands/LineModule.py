from Utils import *
import cv2
from Image import Image
import numpy as np
import math 


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
            y.append(self.const.resolution[1]/8 + self.const.resolution[1]/4*i)

        x = np.array(list)
        y = np.array(y)

        A = np.vstack([x, np.ones(len(x))]).T

        self.m, self.c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        y0 = self.const.resolution[1]*7/8
        x0 = self.predict(self.const.resolution[1]*7/8)

        y3 = self.const.resolution[1]*1/8
        x3 = self.predict(self.const.resolution[1]*1/8)


        angle = math.degrees(np.arctan(self.m))
        offset = self.predict(self.const.resolution[1]/2)

        ##////////Printing linReg line
        image = repackedImg
        line_thickness = 2
        cv2.line(image, (int(x3), 340 - int(y3)), (int(x0), 340 - int(y0)), (255, 32, 0), thickness=line_thickness)

        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()


        ##///////////Printing information
        print ("\n{:<8} {:<15} {:<15} ".format('Angle','Offset', 'Cross'))
        print ("{:<8} {:<15} {:<15} ".format("{0:.3f}".format(angle), "{0:.3f}".format(offset), atCross))   

        return list, atCross, angle, offset

    def predict(self, y):
        f_y = (y - self.c)/self.m
        return f_y

    def quit(self):
        cv2.destroyAllWindows()