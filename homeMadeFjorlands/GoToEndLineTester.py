from time import sleep
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
cupDistBuffer = 10


def startVideoCapture():
    sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format=("bgr"), use_video_port=True):
        sleep(0.0001)

        image = frame.array
        frame.truncate(0)
        
        findingEndOfLine(image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def findingEndOfLine(image):
    xPos, yPos, endOfLineInImage = lineModule.getEndOfLinePos(image)
    print ("\n{:<8} {:<15} {:<15} ".format('xPos','yPos', 'endOfLineInImage'))
    print ("{:<8} {:<15} {:<15} ".format("{0:.3f}".format(xPos), "{0:.3f}".format(yPos), endOfLineInImage)) 
    if lineModule.endOfLineIsClose(yPos):
        motorControl.goToPos(xPos, const.speed, const.motionError)



