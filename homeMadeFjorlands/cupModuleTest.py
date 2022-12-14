import time
#from LineModule import LineModule
#from motorControl import MotorControl
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
#motorControl = MotorControl(const)
#lineModule = LineModule(True, None , const)
cupModule = CupModule(False, const)
cupDistBuffer = 10

    
def startVideoCapture():
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format=("bgr"), use_video_port=True):
        time.sleep(0.0001)

        image = frame.array
        frame.truncate(0)
        
        test2(image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def test1(image):
    print("Executing subtask 2")
    cupPos, cupInImage, cupIsClose = cupModule.analyzeImage(image)
    if not cupInImage:
        motorControl.turnLeft(35)
    else:
        motorControl.turnToPos(cupPos)
    if cupPos in range(-cupDistBuffer, cupDistBuffer):
        motorControl.stop()
        print("Subtask 2 complete")

def test2(image):
    print(cupModule.analyzeImage(image))


startVideoCapture()