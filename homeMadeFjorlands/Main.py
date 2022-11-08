from LineModule import *
from motorControl import motorControl

if __name__ == "__main__":
    print("\n\nStarting!\n")
    motor = motorControl()
    lineDetector = LineDetector()
    lineDetector.analyzeStrip()

    while input('>') != 'q':
        pass

    lineDetector.quit()
    motor.quit()
    