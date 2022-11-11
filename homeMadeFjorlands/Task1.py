from motorControl import motorControl
from LineModule import LineModule

class Task1:
    def __init__(self, motorContorl, lineModule):
        self.motorControl = motorContorl
        self.lineModule = lineModule
        self.completed = False
        

    def execute(self):
        #TODO
        pass


    def completed(self):
        return self.completed