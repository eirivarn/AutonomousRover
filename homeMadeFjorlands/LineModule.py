from Utils import *
import cv2
from Image import Image
import LinReg

class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.const = const

        for _ in range(self.N_SLICES):
            self.images.append(Image(), const)        


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

        x = np.array()    
        for i in range(self.N_SLICES):
            x.append(self.const.resolution*i + self.const.resolution/2)
        y = np.array(line)
        regressor = LinearRegression(x,y)
        regressor.fit(100, 0.001)
        yPred = regressor.predict(x)

        angle = np.arctan((yPred(10)-yPred(0))/10)
        
        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()

        return line, atCross, angle, yPred

    def quit(self):
        cv2.destroyAllWindows()