from Task import Task
from time import sleep


class Task2(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const):
        super().__init__(motorContorl, lineModule, cupModule, const)
        self.speed = self.const.need4speed 
        
        self.subTask = 1

    def update(self, image):
        self.cameraServo.down()
        self.gripperServo.openGripper()

        if self.subtasks[0] == False:
            self.subtasks[0] = True
            self.motorControl.forward(40)
            sleep(0.6)
            print("Following line to cross")
            #self.motorControl.forward(30)
            #sleep(0.005)
        line, atCross, angle, lateralOffset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, angle, lateralOffset, self.speed, lostLine, self.motionError)
        if atCross:
            self.motorControl.stop()
            print("At cross, subtask 1 complete.")
            self.subTask = 2
            self.ticker = 0

        if self.subTask == 2:    #task 2 complete
            super.setActiveTask(3)

        else:
            print('Error in task2. subTaskCount out of bounce')