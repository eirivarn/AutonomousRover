from gpiozero import Servo, AngularServo
 
class servo:
       
    def __init__(self, port, angOrCont):
        self.port = port
        self.open = 70
        self.close = 120
        self.up = 45
        self.flat = 0
        self.cameraFront = 0
        self.cameraLeft = 1
        self.cameraRight = 2      
        
        if angOrCont == 'ang':
            self.servo = AngularServo(self.port, min_pulse_width = 0.0006, max_pulse_width=0.0023)
        else:
            self.servo = Servo(self.port)

 
   
    def open(self):
        self.servo.value = self.open
 
    def close(self):
        self.servo.value = self.close
 
    def lift(self):
        self.servo.angle = self.up
 
    def lower(self):
        self.servo.angle = self.flat
 
    def panRight(self):
        self.servo.value = self.cameraRight
   
    def panLeft(self):
        self.servo.value = self.cameraRight
   
    def panFront(self):
        self.servo.value = self.cameraRight
        
        
        

