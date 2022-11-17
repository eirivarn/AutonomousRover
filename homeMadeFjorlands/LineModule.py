from Utils import *
import cv2
from Image import Image
import numpy as np

class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = const.n_slices
        self.images = []
        self.const = const

        self.m = 0
        self.c = 0

        for _ in range(self.N_SLICES):
            self.images.append(Image(const),)        


    def analyzeImage(self, image):
        removedBgImg = RemoveBackground(image, True)
        atCross = False
        list = []
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                list.append(self.images[i].getOffset())
                if self.images[i].crossFound():
                    self.robot.updateCrossConf(i) 
            repackedImg = RepackImages(self.images)

        ##/// Making LinReg line ///

        for i in range(len(list)):
            if list[i] == 0:
                list[i] = np.average(list)

        x = np.array(list)
        y = []

        for i in range(self.N_SLICES):
            y.append(self.const.resolution[1]/(self.N_SLICES*2) + self.const.resolution[1]/self.N_SLICES*i)

        y = np.array(y)
        #prøver å kun bruke de 3/4 øverste punktene til lin reg. har økt til 8 punkter:
        x = x[:int(self.N_SLICES * self.const.offsetPosition)]
        y = y[:int(self.N_SLICES * self.const.offsetPosition)]

        A = np.vstack([x, np.ones(len(x))]).T

        self.m, self.c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        inversedAngle = np.rad2deg(np.arctan(self.m))
        if inversedAngle >= 0:
            angle = 90 - inversedAngle
        if inversedAngle < 0:
            angle = -90 - inversedAngle

        offset = self.predict(self.const.resolution[1]*self.const.offsetPosition)
        #offset = self.predict(self.const.resolution[1]/2)

        try:
            y1 = self.const.linRegPlotY1
            x1 = int(self.const.resolution[0]/2 + self.predict(y1))
            y2 = self.const.linRegPlotY2
            x2 = int(self.const.resolution[0]/2 + self.predict(y2))

            cv2.line(repackedImg, (x1,y1), (x2,y2), (0,0,255), 3)
        except:
            print('Could not find line')
            

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()


        ##///////////Printing information
        print ("\n{:<8} {:<15} {:<15} ".format('Angle','Offset', 'Cross'))
        print ("{:<8} {:<15} {:<15} ".format("{0:.3f}".format(angle), "{0:.3f}".format(offset), atCross))   

        return list, atCross, angle, offset

    def flipPoint(self, x):
        return int(self.const.resolution[0]/2 - x)

    def predict(self, y):
        f_y = (y - self.c)/self.m
        return f_y

    def quit(self):
        cv2.destroyAllWindows()








        ####TODO ////////Printing linReg line
##
        ## # x og y position ved øverste punkt, ivertert
        ##inverted_y0 = self.const.resolution[1]*7/8
        ##inverted_x0 = self.predict(self.const.resolution[1]*7/8)
##
        ### x og y position ved nederste punkt, invertert 
        ##inverted_y3 = self.const.resolution[1]*1/8
        ##inverted_x3 = self.predict(self.const.resolution[1]*1/8)
##
        ##y0 = self.flipPoint(inverted_y0) 
        ##x0 = self.flipPoint(inverted_x0)
##
        ##y3= self.flipPoint(inverted_y3)
        ##x3 = self.flipPoint(inverted_x3)
##
        ##cv2.line(repackedImg, (x0, y3), (x3, y0), (255, 20, 0), thickness=3)
        ###angle, lateralOffset= ekstraBox(repackedImg)
        ###printInfo(self.images)