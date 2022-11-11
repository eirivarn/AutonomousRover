import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2



class CaptureImage:

    def __init__(self, motor, lineModule, cupModule):
        
        camera = PiCamera()
        camera.resolution = (640, 368)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        self.image = None
        self.motor = motor
        self.lineModule = lineModule
        self.cupModule = cupModule

        return camera
    
    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            self.image = frame.array


            if cv2.waitKey(1) & 0xff == ord('q'):
                break