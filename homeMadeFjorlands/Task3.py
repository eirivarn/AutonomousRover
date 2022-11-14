from time import sleep
from Task import Task


class Task3(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const):
        super().__init__(motorContorl, lineModule, cupModule, const)
        self.speed = self.const.speed  #sett en safe og trygg speed gjennom hinderløpa
        self.subTask = 1

    def update(self, image):
        if self.subTask == 1: # turn left
            self.subTask1()
        
        if self.subTask == 2:   #keep tunring left til main line
            self.subTask2(image)

        if self.subTask == 3:   #follow line to next cross
            self.subTask3(image)

        if self.subTask == 4:    #task 2 complete
            super.setActiveTask(4)

        else:
            print('Error in task3. subTaskCount out of bounce')


    def subTask1(self):
        self.motorControl.turnLeft()
        sleep(1)
        self.subTask = 2

    def subTask2(self,image):
        line, crossFound = self.lineModule.analyzeImage(image)
        if line == []:
            self.motorControl.turnLeft()
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.lineDistBuffer, self.lineDistBuffer):
                self.subTask = 3

    def subTask3(self, image):
        line, crossFound = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, self.speed)
        if crossFound:
            self.motorControl.goToCross(self.speed)
            self.subtask = 4