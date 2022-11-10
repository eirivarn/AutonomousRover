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
        self.N_SLICES = 8
        


    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            image = frame.array
            removedBgImg = RemoveBackground(image, False)
            images = []
            direction = 0
            
            for _ in range(self.N_SLICES):
                img = Image()
                images.append(img)
            
            if removedBgImg is not None:
                SlicePart(removedBgImg, images, self.N_SLICES)
                for i in range(self.N_SLICES):
                    direction += images[i].getDir()
                
                repackedImg = RepackImages(images)
            
            cv2.imshow('Image', repackedImg)
            self.rawCapture.truncate(0)
           
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    def quit(self):
        cv2.destroyAllWindows()