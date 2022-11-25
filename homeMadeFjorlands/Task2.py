from Task import Task
from time import sleep


class Task2(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const, robot):
        super().__init__(motorContorl, lineModule, cupModule, const, robot)
        self.speed = self.const.need4speed 
        self.motionError = 1
        self.subTask = 1

    def update(self, image, motionError):
        self.motionError = motionError
        if self.subTask == 1:
            self.cameraServo.down()
            self.subTask = 2
        if self.subTask == 2:
            self.subTask2(image)
        elif self.subTask == 3:    #task 2 complete
            self.robot.setActiveTask(3)
        else:
            print("error in task 2, subtask out of bounce")



    def subTask2(self, image): #cross to next cross
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speed, lostLine, self.motionError)
        if atCross:
            self.subTask = 2