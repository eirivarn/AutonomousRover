import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from getkey import getkey



class CaptureImage:

    def __init__(self, const):
        self.const = const
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.image = None

    
    def startVideoCapture(self, robot):
        time.sleep(0.1)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.001)

            self.image = frame.array
            frame.truncate(0)
            
            robot.update(self.image)

  
            if cv2.waitKey(1) & 0xff == ord('q'):
                robot.motor.stop()
                cv2.destroyAllWindows()
                break
            '''if self.const.isHeadless:
                key = getkey()
                if key == 'q':
                    robot.motor.stop()
                    break'''