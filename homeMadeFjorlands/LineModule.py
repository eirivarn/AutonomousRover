from Utils import *
import cv2
from Image import Image


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
        x = np.array(x)
        y = np.array(line)

        m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
        b = (np.sum(y) - m *np.sum(x)) / len(x)

        offset = m*self.const.resolution[1]/2 - b - self.const.resolution[1]/2
        print(offset)
        angle = np.arctan((m*10 - 2*b)/10)
        print(angle)


        
        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()

        return line, atCross, angle, offset

    def quit(self):
        cv2.destroyAllWindows()