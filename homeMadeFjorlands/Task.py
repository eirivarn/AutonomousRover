from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule
import Main


class Task:
    def __init__(self, motorContorl, lineModule, cupModule):
        self.motorControl = motorContorl
        self.lineModule = lineModule
        self.cupModule = cupModule
        self.completed = False
        

    def update(self, image):
        pass

        
    def completed(self):
        return self.completed