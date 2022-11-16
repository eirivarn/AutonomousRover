import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2


class CaptureImage:

    def __init__(self, const):
        
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.image = None

    
    def startVideoCapture(self, robot):
        time.sleep(0.1)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            self.image = frame.array
            frame.truncate(0)
            
            robot.update(self.image)

  
            if cv2.waitKey(1) & 0xff == ord('q'):
                robot.motor.stop()
                break