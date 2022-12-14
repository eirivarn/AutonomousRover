from Task import Task
from time import sleep
from servo import Servo


class Task1(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const, robot):
        super().__init__(motorContorl, lineModule, cupModule, const ,robot)
        self.speed = self.const.speed
        self.cupDistBuffer = self.const.cupDistBuffer
        self.lineDistBuffer = self.const.lineDistBuffer
        self.cupSide = "right"
        self.turnCounter = 0
        self.ticker = 0
        self.motionError = 1

        self.subtasks = [False, False, False, False, False, False, False, False, False, False]   

    def update(self, image, motionError=1):
        self.motionError = motionError

        print("At subtask: " , self.subTask)

        if self.subTask == 1: #Følger linje til kryss
            self.subTask1(image)
        
        elif self.subTask == 2:  #Sjekker hvilke side koppen er på.
            self.subTask2(image)
            
        elif self.subTask == 3:  #turn drive forward to cup
            self.subTask3(image)
            
        elif self.subTask == 4: #pick up cup
            self.subTask4()
                       
        elif self.subTask == 5: # turn 90 deg to main line
            self.subTask5()
            
        elif self.subTask == 6: #turn right
            self.subTask6()
            
        elif self.subTask == 7:  #keep turning to the sideline
            self.subTask7()
            
        elif self.subTask == 8: #drop cup
            self.subtask8(image)
            
        elif self.subTask == 9: #turn left for 2 sek TODO adjust this variable
            self.subTask9(image)
        #
        #elif self.subTask == 10: # keep turning to main line
        #    self.subTask10(image)
#
        #elif self.subTask == 11: #task is complete
        #    super.setActiveTask(2)
#
        else:
            print('Error in task1. subTaskCount out of bounce')



    def subTask1(self,image):  # Følger linja
        self.cameraServo.down()
        self.gripperServo.openGripper()

        if self.subtasks[0] == False:
            self.subtasks[0] = True
            self.motorControl.forward(35)
            sleep(0.3)
            print("Following line to cross")

        line, atCross, angle, lateralOffset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, angle, lateralOffset, self.speed, lostLine, self.motionError)
        if atCross:
            self.motorControl.stop()
            print("At cross, subtask 1 complete.")
            self.subTask = 2
            self.ticker = 0

    def subTask2(self, image): #Finner ut hvilke side koppen er på. ¨
        print(self.turnCounter)
        if self.subtasks[1] == False:
            print("Task 2, localize cup")
            self.subtasks[1] = True
        self.cameraServo.up()
        cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
        if (1 <= self.turnCounter <= 2) and (15 < self.ticker) :
                self.motorControl.rotateRight(self.const.quartRotationSpeed)
                self.turnCounter += 1 
                sleep(self.const.quartRotationTime)
                self.motorControl.stop()
                sleep(2)
        if self.turnCounter == 0:
            if self.ticker == 0:
                self.motorControl.rotateLeft(self.const.quartRotationSpeed)
                sleep(self.const.quartRotationTime)
                self.motorControl.stop()
                sleep(0.5)
            if 15 < self.ticker: 
                self.turnCounter += 1
            if cupInImage and (10 < self.ticker):
                self.cupSide = "left"
                self.motorControl.stop()
                self.subTask = 3
                self.ticker = 0
        if (3 <= self.turnCounter) and (20 < self.ticker) :
            self.motorControl.stop()
            self.subTask = 3
            self.ticker = 0 
        self.ticker += 1 
        
        
    def subTask3(self,image): #Kjører til koppen.
        cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
        print("CupIsClose: " ,cupIsClose)
        print("cupPos: " ,cupPos)
        if cupIsClose:
            self.motorControl.stop()
            self.subTask = 4
            return
        self.motorControl.goToPos(cupPos, self.speed, self.motionError)
    

    def subTask4(self): #Plukker opp koppen
        self.gripperServo.closeGripper()
        self.subTask = 5 

    def subTask5(self): #Roterer 180 grader
        if self.cupSide == "left":
            self.motorControl.rotateRight(self.const.quartRotationSpeed)
            sleep(self.const.quartRotationTime)
            self.motorControl.rotateRight(self.const.quartRotationSpeed)
            sleep(self.const.quartRotationTime)
            self.motorControl.stop()
        if self.cupSide == "right":
            self.motorControl.rotateLeft(self.const.quartRotationSpeed)
            sleep(self.const.quartRotationTime)
            self.motorControl.rotateLeft(self.const.quartRotationSpeed)
            sleep(self.const.quartRotationTime)
            self.motorControl.stop()
        self.subTask = 6


    def subTask6(self):
        self.motorControl.forward(20)
        sleep(1.5)
        self.subTask = 7 
    

    def subTask7(self):
        self.gripperServo.openGripper()
        self.subTask = 8


    def subTask8(self, image):
        line, atCross, angle, lateralOffset, lostLine = self.lineModule.analyzeImage(image)
        if self.lineModule.isCrossAt(self.const.N_SLICES): 
            if self.cupSide == "right":
                self.motorControl.rotateLeft(self.const.quartRotationSpeed)
                sleep(self.const.quartRotationTime)
                self.subTask = 9
            if self.cupSide == "left":
                self.motorControl.rotateRight(self.const.quartRotationSpeed)
                sleep(self.const.quartRotationTime)
                self.subTask = 9
        else: self.motorControl.backward(20)


    #def subTask7(self, image):
    #    #line, atCross, angle, lateralOffset, lostLine= self.lineModule.analyzeImage(image)
    #    xPos, yPos, endOfLineInImage = self.lineModule.getEndOfLinePos(image)
    #    if self.lineModule.endOfLineIsClose(yPos):
    #        self.motorControl.forward(self.speed, self.motionError)
    #        sleep(0.5)
    #        self.motorControl.stop()
    #        self.subTask = 8
    #    self.motorControl.goToPos(xPos, self.speed, self.motionError)

    #def subTask8(self, image):
    #    self.gripperServo.openGripper()
    #    self.cameraServo.down()
    #    self.subTask = 9
    #        
    #def subTask9(self, image):
    #    line, atCross, angle, lateralOffset, lostLine= self.lineModule.analyzeImage(image)
    #    if self.lineModule.crossAtPosition(self.const.n_slices-1):
    #        self.motorControl.stop()
    #        self.subTask = 9
    #    self.motorControl.backward(self.speed ,self.motionError)
#
    #def subTask10(self, image):
    #    line, atCross, angle, lateralOffset, lostLine= self.lineModule.analyzeImage(image)
    #    if lostLine:
    #        self.motorControl.rotateLeft(self.speed, self.motionError)
    #    if lateralOffset in range(-self.const.lineDistBuffer, self.const.lineDistBuffer):
    #        self.subTask = 11 
    #    self.motorControl.rotateLeft(self.speed, self.motionError)

    