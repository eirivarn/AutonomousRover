from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule
from CaptureImage import CaptureImage
from Victory import Victory, Fail
import numpy as np

from Task1 import Task1
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4
from const import Const

class Robot():

    def __init__(self):
        self.const = Const()
        self.motor = MotorControl(self.const)
        self.lineModule = LineModule(False, self)
        self.cupModule = CupModule(False)
        self.camera = CaptureImage()
        
        self.task1 = Task1(self.motor, self.lineModule, self.cupModule)
        self.task2 = Task2(self.motor, self.lineModule, self.cupModule)
        self.task3 = Task3(self.motor, self.lineModule, self.cupModule)
        self.task4 = Task4(self.motor, self.lineModule, self.cupModule)

        self.n_slices = 4
        self.crossConfidence = np.zeros(self.n_slices)
        self.completeList = np.zeros(self.n_slices,)
        for i in range(len(self.completeList)):
            self.completeList[i] = 1

        self.activeTask = 1


    def update(self, image):
        if self.activeTask == 1:
            task = self.task1
        elif self.activeTask == 2:
            task = self.task2
        elif self.activeTask == 3:
            task = self.task3
        elif self.activeTask == 4:
            task = self.task4
        elif self.activeTask == 5:
            Victory(self.motor, self.lineModule)
            return

        task.update(image)   

    def setActiveTask(self, task):
        self.activeTask = task

    
    def updateCrossConf(self, i):
        if i == 0:
            self.crossConfidence[i] = 1
        else:
            for j in range(i):
                if self.crossConfidence[j] == 0:
                    self.crossConfidence = np.zeros(self.n_slices)
                    break
            self.crossConfidence[i] = 1

    def crossConfirmed(self):
        return (self.crossConfidence == self.completeList).all()

        