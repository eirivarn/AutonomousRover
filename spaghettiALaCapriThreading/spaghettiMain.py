from spaghettiLineModule import *
from spaghettiRover import motorControl

if __name__ == "__main__":
    print("\n\nStarting!\n")
    motor = motorControl()
    lineDetector = LineDetector(motor)
    lineDetector.analyzeStrip()

    while input('>') != 'q':
        pass

    lineDetector.quit()
    motor.quit()
