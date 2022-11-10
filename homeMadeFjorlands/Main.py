from motorControl import motorControl
from LesGetSomeLines import LesGetSomeLines

if __name__ == "__main__":
    print("\n\nStarting!\n")
    motor = motorControl()
    lineDetector = LesGetSomeLines(False)
    lineDetector.startVideoCapture()

    lineDetector.quit()
    motor.quit()
