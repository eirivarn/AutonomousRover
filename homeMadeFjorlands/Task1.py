from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule

class Task1:
    def __init__(self, motorContorl, lineModule, cupModule):
        self.motorControl = motorContorl
        self.lineModule = lineModule
        self.cupModule = cupModule
        self.completed = False
        

    def execute(self):
        #TODO
        self.cupModule.startVideoCapture()
        self.cupModule.quit()

        


    def completed(self):
        return self.completed