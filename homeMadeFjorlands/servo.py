from gpiozero import AngularServo
from gpiozero.pins.native import NativeFactory
from const import Const
import RPi.GPIO as GPIO
 
class servo:
       
    def __init__(self, port):
        GPIO.setwarnings(False)
        self.servo = AngularServo(port)
        self.const = Const()


    def openGripper(self):
        self.servo.value = self.const.open_val
 
    def closeGripper(self):
        self.servo.value = self.const.close_val

    def lift(self):
        self.servo.value = self.const.cameraUp
 
    def lower(self):
        self.servo.value = self.const.cameraLower 
 
        
        

