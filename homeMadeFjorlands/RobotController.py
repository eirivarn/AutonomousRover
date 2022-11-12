from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule
from CaptureImage import CaptureImage
from Victory import Victory, Fail

from Task1 import Task1
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4

class Robot():

    def __init__(self):
        self.motor = MotorControl()
        self.lineModule = LineModule(False)
        self.cupModule = CupModule(False)
        self.camera = CaptureImage()
        
        self.activeTask = 1


    def update(self, image):
        if self.activeTask == 1:
            task = Task1(self.motor, self.lineModule, self.cupModule)
        elif self.activeTask == 2:
            task = Task2(self.motor, self.lineModule, self.cupModule)
        elif self.activeTask == 3:
            task = Task3(self.motor, self.lineModule, self.cupModule)
        elif self.activeTask == 4:
            task = Task4(self.motor, self.lineModule, self.cupModule)
        elif self.activeTask == 5:
            Victory(self.motor, self.lineModule)
            return

        task.update(image)   

    def setActiveTask(self, task):
        self.activeTask = task


