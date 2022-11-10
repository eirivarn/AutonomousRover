import time
from Utils import *
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from Image import Image


class LesGetSomeLines:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 368)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        time.sleep(0.1)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.Images=[]
        self.N_SLICES = 4
        self.direction = 0


    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            image = frame.array
            removedBgImg = RemoveBackground(image, False)
            
            for _ in range(self.N_SLICES):
                img = Image()
                self.Images.append(img)
            
            if img is not None:
                SlicePart(removedBgImg, self.Images, self.N_SLICES)
                for i in range(self.N_SLICES):
                    self.direction += self.Images[i].getDir()
                
                repackedImg = RepackImages(self.Images)
            
            cv2.imshow('Image', repackedImg)
            self.rawCapture.truncate(0)
           
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    def quit(self):
        cv2.destroyAllWindows()