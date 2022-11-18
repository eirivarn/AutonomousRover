from gpiozero import Servo, AngularServo
 
class servo:
       
    def __init__(self, port, angOrCont):
        self.port = port
        self.open_val = 0.6
        self.close_val = 0.15
        self.up = 45
        self.flat = 20
        self.cameraFront = 0
        self.cameraLeft = 1
        self.cameraRight = 2      
        
        if angOrCont == 'ang':
            self.servo = AngularServo(self.port, min_pulse_width = 0.0006, max_pulse_width=0.0023)
        else:
            self.servo = Servo(self.port)

 
   
    def openGripper(self):
        self.servo.value = self.open_val
 
    def closeGripper(self):
        self.servo.value = self.close_val

    def lift(self):
        self.servo.value = self.up
 
    def lower(self):
        self.servo.value = self.flat
 
        
        

