from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from const import Const
 
class servo:
    def __init__(self, port):
        factory = PiGPIOFactory()
        self.servo = AngularServo(port, pin_factory = factory)
        self.const = Const()

    def openGripper(self):
        self.servo.value = self.const.open_val
 
    def closeGripper(self):
        self.servo.value = self.const.close_val

    def lift(self):
        self.servo.value = self.const.cameraUp
 
    def lower(self):
        self.servo.value = self.const.cameraLower 
 
        
        

