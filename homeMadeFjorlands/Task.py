from servo import Servo
class Task:
    def __init__(self, motorContorl, lineModule, cupModule, const, robot):
        self.robot = robot
        self.const = const
        self.motorControl = motorContorl
        self.lineModule = lineModule
        self.cupModule = cupModule
        self.cameraServo = Servo(12)
        self.gripperServo = Servo(13)
        self.image = None
        self.subTask = 1 
        self.completed = False
        

    def update(self, image, motionError):
        pass

        
    def completed(self):
        return self.completed