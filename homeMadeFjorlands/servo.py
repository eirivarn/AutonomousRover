from gpiozero import AngularServo
from const import Const
 
class servo:
    def __init__(self, port):
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
 
        
        

