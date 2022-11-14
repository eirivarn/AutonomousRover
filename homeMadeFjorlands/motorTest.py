import time
from LineModule import LineModule
from motorControl import MotorControl
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from CupModule import CupModule
from const import Const

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
image = None

const = Const()
motorControl = MotorControl(const)
lineModule = LineModule(True, None , const)
cupModule = CupModule(True, const)
cupDistBuffer = 2

    
def startVideoCapture():
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format=("bgr"), use_video_port=True):
        time.sleep(0.0001)

        image = frame.array
        frame.truncate(0)
        
        test1(image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def test1(image):
    print("Executing subtask 2")
    cupPos, cupInImage, cupIsClose = cupModule.analyzeImage(image)
    if not cupInImage:
        motorControl.turnLeft(50)
    else:
        motorControl.turnToPos(cupPos)
    if cupPos in range(-cupDistBuffer, cupDistBuffer):
        
        print("Subtask 2 complete")

startVideoCapture()