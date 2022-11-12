import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule
import Main



class CaptureImage:

    def __init__(self, motor, lineModule, cupModule):
        
        self.camera = PiCamera()
        self.camera.resolution = (640, 368)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        self.image = None
        self.motor = motor
        self.lineModule = lineModule
        self.cupModule = cupModule

    
    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            self.image = frame.array
            
            Main.update(self.image)
  
            if cv2.waitKey(1) & 0xff == ord('q'):
                break