from LineModule import *
from motorControl import motorControl
from FindLine import FindLine

if __name__ == "__main__":
    print("\n\nStarting!\n")
    motor = motorControl()
    lineDetector = FindLine()
    lineDetector.startVideoCapture()

    lineDetector.quit()
    motor.quit()