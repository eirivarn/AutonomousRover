from Task import Task
from time import sleep


class Task1(Task):
    def __init__(self, motorContorl, lineModule, cupModule):
        super().__init__(motorContorl, lineModule, cupModule)
        self.speed = 12
        self.cupDistBuffer = 5
        self.lineDistBuffer = 2

    def update(self, image):

        if self.subTask == 1: #follow line to cross
            self.subTask1(image)
        
        elif self.subTask == 2:  #turn left untill cup is in center
            self.subTask2(image)
            
        elif self.subTask == 3:  #turn drive forward to cup
            self.subTask3(image)
            
        elif self.subTask == 4: #pick up cup
            self.subTask4()
                       
        elif self.subTask == 5: # turn 90 deg to main line
            self.subTask5(image)
            
        elif self.subTask == 6: #turn right for 2 sek TODO adjust this variable
            self.subTask6()
            
        elif self.subTask == 7:  #keep turning to the sideline
            self.subTask7(image)
            
        elif self.subTask == 8: #drop cup
            self.subTask8()
            
        elif self.subTask == 9: #turn left for 2 sek TODO adjust this variable
            self.subTask9()
        
        elif self.subTask == 10: # keep turning to main line
            self.subTask10(image)

        elif self.subTask == 11: #task is complete
            super.setActiveTask(2)

        else:
            print('Error in task1. subTaskCount out of bounce')



    def subTask1(self,image):
        line, atCross, angle, lateralOffset = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, angle, lateralOffset, self.speed)
        if atCross:
            self.subtask = 2

    def subTask2(self,image):
        cupPos, cupInImage = self.cupModule.analyzeImage(image)
        if not cupInImage:
            self.motorControl.turnLeft()
        else:
            self.motorControl.turnToPos(cupPos)
        if cupPos in range(-self.cupDistBuffer, self.cupDistBuffer):
            self.subTask = 3
    
    def subTask3(self,image):
        cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
        if cupIsClose:
            self.motorControl.stop()
            self.subTask = 4
            return
        self.motorControl.goToCup(cupPos)

    def subTask4(self):
        self.servo.close()
        self.subTask = 5 

    def subTask5(self,image):
        line, crossFound = self.lineModule.analyzeImage(image)
        if line == []:
            self.motorControl.turnLeft()
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.lineDistBuffer, self.lineDistBuffer):
                self.subTask = 6

    def subTask6(self):
        self.motorControl.turnRight()
        sleep(2)
        self.subTask = 7

    def subTask7(self,image):
        line, crossFound = self.lineModule.analyzeImage(image)
        if line == []:
            self.motorControl.turnRight()
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.lineDistBuffer, self.lineDistBuffer):
                self.subTask = 8

    def subTask8(self):
        self.servo.open()
        self.subTask = 9


    def subTask9(self):
        self.motorControl.turnLeft()
        sleep(2)
        self.subTask = 10

    def subTask10(self,image):
        line, crossFound = self.lineModule.analyzeImage(image)
        if line == []:
            self.motorControl.turnLeft()
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.lineDistBuffer, self.lineDistBuffer):
                self.subTask = 11