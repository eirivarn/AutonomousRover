from servo import Servo
class Task:
    def __init__(self, motorContorl, lineModule, cupModule, const):
        self.const = const
        self.motorControl = motorContorl
        self.lineModule = lineModule
        self.cupModule = cupModule
        #self.cameraServo = servo()
        self.image = None
        self.subTask = 1 
        self.completed = False
        

    def update(self, image):
        pass

        
    def completed(self):
        return self.completed