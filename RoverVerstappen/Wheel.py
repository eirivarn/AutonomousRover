import RPi.GPIO as GPIO
from collections import namedtuple
from time import time
from Utils import clamp, sign


# This is so that wheel logs have identical time scales
global startTime
startTime  = time()
getRunTime = lambda: time() - startTime

#Setting PIN mode
GPIO.setmode(GPIO.BOARD)

class TimedHardwareLoop:
    """
    This will help classes that are in some main loop that need an "update" function of some sort that depends on time.
    They can check if it's time to run or not.
    """

    def __init__(self, delay):
        self.delay = delay
        self.lastTime = 0

        # Keep track of how long the delay ACTUALLY is
        self.lastDelay = delay

    def isUpdate(self):
        """
        Check if it's time to update
        :return: True if ready, False if wait
        """
        now     = getRunTime()
        willRun = now > self.lastTime + self.delay

        if willRun:
            self.lastDelay = now - self.lastTime
            self.lastTime  = now

        return willRun

    def update(self):
        # In case the child doesn't have this function
        pass


class Wheel(TimedHardwareLoop):

    def __init__(self, speedPin, directionPin):
        super().__init__(delay=0.05)

        # Set up Wheel Controls
        self.speed = 0

        GPIO.setup(speedPin, GPIO.OUT)
        GPIO.setup(directionPin, GPIO.OUT)
    
        self.speed_pwm = GPIO.PWM(speedPin, 20)
        self.speed_pwm.start(0)
