from Utils import *
import cv2
from Image import Image

import numpy as np
#from sklearn.linear_model import LinearRegression

class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.const = const

        for _ in range(self.N_SLICES):
            self.images.append(Image())        


    def analyzeImage(self, image):
        removedBgImg = RemoveBackground(image, True)
        direction = 0
        atCross = False
        line = []
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
                line.append(self.images[i].getDir()) ##TODO usikker på om getDir eller getOffset er riktig
                if self.images[i].crossFound():
                    self.robot.updateCrossConf(i)
            repackedImg = RepackImages(self.images)
        
        ##/////////linReg line
        y = np.array(line).reshape(-1,1)
        x = []
        pixelsBetweenReadings = self.const.resolution / self.N_SLICES
        for i in range(self.N_SLICES):
            y.append(pixelsBetweenReadings/2 + pixelsBetweenReadings*i)
        #model = LinearRegression().fit(x,y)
        #angle = np.degreesarctan(model.predict(100) - model.predict(0)/100)
        #offset = model.predict(240) - 320


        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        
        angle = 0
        offset = 0

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()

        return line, atCross, angle, offset

    def quit(self):
        cv2.destroyAllWindows()