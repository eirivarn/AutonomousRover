import time
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

    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)
            image = frame.array
            img = Image(image)
            img = img.Process()
            
            cv2.imshow('Image', img)
            self.rawCapture.truncate(0)
           
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    def quit(self):
        cv2.destroyAllWindows()