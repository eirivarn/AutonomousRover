from Task import Task


class Task2(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const):
        super().__init__(motorContorl, lineModule, cupModule, const)
        self.speed = self.const.need4speed 
        
        self.subTask = 1

    def update(self, image):

        if self.subTask == 1:
            line, crossFound = self.lineModule.analyzeImage(image)
            self.motorControl.followLine(line, self.speed)
            if crossFound:
                self.motorControl.goToCross(self.speed)
                self.subtask = 2

        if self.subTask == 2:    #task 2 complete
            super.setActiveTask(3)

        else:
            print('Error in task2. subTaskCount out of bounce')