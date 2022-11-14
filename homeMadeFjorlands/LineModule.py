from Utils import *
import cv2
from Image import Image

import numpy as np
from sklearn.linear_model import LinearRegression

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
        
        
        pi@mypi:~/CODE/grpc $ ldd /usr/local/lib/python3.9/dist-packages/grpc/_cython/cygrpc.cpython-39-arm-linux-gnueabihf.so
        linux-vdso.so.1 (0xbeef7000)
        /usr/lib/arm-linux-gnueabihf/libarmmem-${PLATFORM}.so => /usr/lib/arm-linux-gnueabihf/libarmmem-v7l.so (0xb698b000)
        libpthread.so.0 => /lib/arm-linux-gnueabihf/libpthread.so.0 (0xb695f000)
        libatomic.so.1 => /lib/arm-linux-gnueabihf/libatomic.so.1 (0xb6946000)
        libstdc++.so.6 => /lib/arm-linux-gnueabihf/libstdc++.so.6 (0xb67be000)
        libm.so.6 => /lib/arm-linux-gnueabihf/libm.so.6 (0xb674f000)
        libc.so.6 => /lib/arm-linux-gnueabihf/libc.so.6 (0xb65fb000)
        /lib/ld-linux-armhf.so.3 (0xb6fcc000)
        libgcc_s.so.1 => /lib/arm-linux-gnueabihf/libgcc_s.so.1 (0xb65ce000)


        #angle, lateralOffset= ekstraBox(repackedImg)
        #printInfo(self.images)
        

        if not self.isHeadless:
            cv2.imshow('Image', repackedImg)
        
        atCross = self.robot.crossConfirmed()

        return line, atCross, angle, offset

    def quit(self):
        cv2.destroyAllWindows()