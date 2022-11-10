from LineModule import *
from motorControl import motorControl

if __name__ == "__main__":
    print("\n\nStarting!\n")
    motor = motorControl()
    lineDetector = LineDetector(motor)
    lineDetector.startVideoCapture()

    lineDetector.quit()
    motor.quit()
