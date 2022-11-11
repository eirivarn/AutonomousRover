import time
from Utils import *
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from Image import Image


class LineModule:
    def __init__(self, isHeadless, camera):
        self.isHeadless = isHeadless
        self.camera = camera
        
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        time.sleep(0.1)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = 4
        self.images = []
        self.breakLoop = False
        for _ in range(self.N_SLICES):
            self.images.append(Image())
        


    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            image = frame.array
            removedBgImg = RemoveBackground(image, True)
            direction = 0
            
            if removedBgImg is not None:
                SlicePart(removedBgImg, self.images, self.N_SLICES)
                for i in range(self.N_SLICES):
                    direction += self.images[i].getDir()
                
                repackedImg = RepackImages(self.images)
            
            printInfo(self.images)

            if not self.isHeadless:
                cv2.imshow('Image', repackedImg)
            self.rawCapture.truncate(0)
           
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            
            if self.breakLoop:
                self.breakLoop = False
                break

    def quit(self):
        self.breakLoop = True
        cv2.destroyAllWindows()