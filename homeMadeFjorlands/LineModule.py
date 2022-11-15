from Utils import *
import cv2
from Image import Image
from LinReg import *

class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.const = const

        for _ in range(self.N_SLICES):
            self.images.append(Image(const),)        


    def analyzeImage(self, image):
        removedBgImg = RemoveBackground(image, True)
        direction = 0
        atCross = False
        line = []
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                direction += self.images[i].getDir()
                line.append(self.images[i].getOffset()) ##TODO usikker på om getDir eller getOffset er riktig
                if self.images[i].crossFound():
                    self.robot.updateCrossConf(i)
            repackedImg = RepackImages(self.images)

        x = []
        for i in range(self.N_SLICES):
            x.append(self.const.resolution[1]*i/4 + self.const.resolution[1]/4)
        x = np.array(x.iloc[:,0])
        y = np.array(line.iloc[:,1])
        regressor = LinearRegression(x,y)
        regressor.fit(1000, 0.0001)

        offset = (regressor.predict(self.const.resolution[1]/2)) - self.const.resolution[1]/2
        print(offset)
        angle = np.arctan((regressor.predict(10)-regressor.predict(0))/10)
        print(angle)


        
        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()

        return line, atCross, angle, offset

    def quit(self):
        cv2.destroyAllWindows()