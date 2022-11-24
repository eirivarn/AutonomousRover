from time import sleep
from Task import Task


class Task3(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const):
        super().__init__(motorContorl, lineModule, cupModule, const)
        self.speedHill = self.const.speedTask3Hill  #sett en safe og trygg speed gjennom hinderløpa
        self.speedObsticals = self.const.speedObsticals
        self.turnSpeed = self.const.turnSpeed
        self.motionError = 1
        self.subTask = 1


    def update(self, image, motionError=1):
        self.motionError = motionError
        print(self.subTask)
        if self.subTask == 1: # turn left
            self.subTask1()
        
        if self.subTask == 2:   #keep tunring left til main line
            self.subTask2(image)

        if self.subTask == 3:   #follow line to next cross
            self.subTask3(image)

        if self.subTask == 4:   #follow line to next cross
            self.subTask4(image)

        if self.subTask == 5:   #follow line to next cross
            self.subTask5(image)

        if self.subTask == 6:   #follow line to next cross
            self.subTask6(image)

        if self.subTask == 7:   #turn left
            self.subTask8(image)

        if self.subTask == 8:    #task 2 complete
            super.setActiveTask(4)

        else:
            print('Error in task3. subTaskCount out of bounce')


    def subTask1(self):
        self.cameraServo.down()
        #self.motorControl.rotateLeft(self.const.quartRotationSpeed, self.motionError)
        #sleep(self.const.quartRotationTime)  #TODO funker egentlig dett??? trengs det? eventuelt legg inn 90 deg sving
        self.subTask = 3

    def subTask2(self,image):
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        if lostLine:
            self.motorControl.findLine()        
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos, self.motionError)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.const.lineDistBuffer, self.const.lineDistBuffer):
                self.subTask = 3

    def subTask3(self, image): #cross to hill
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speedHill, lostLine, self.motionError)
        if atCross:
            self.subtask = 4

    def subTask4(self, image): #hill to first bump
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speedHill, lostLine, self.motionError)
        if atCross:
            self.subtask = 5
    
    def subTask5(self, image): #bump to bump
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speedObsticals, lostLine, self.motionError)
        if atCross:
            self.subtask = 6
    
    def subTask6(self, image): #bump to bump
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speedObsticals, lostLine, self.motionError)
        if atCross:
            self.subtask = 7

    def subTask7(self,image): #turn left
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        if lostLine:
            self.motorControl.findLine() #TODO bytt til lost line funk
        else:
            pos = line[2]
            self.motorControl.turnToPos(pos, self.motionError)  #TODO kan være vilket som helst line-punkt, bør testes
            if pos in range(-self.const.lineDistBuffer, self.const.lineDistBuffer):
                self.subTask = 8