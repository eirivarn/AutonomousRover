from time import sleep
from Task import Task


class Task3(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const, robot):
        super().__init__(motorContorl, lineModule, cupModule, const ,robot)
        self.speedHill = self.const.speedTask3Hill  #sett en safe og trygg speed gjennom hinderløpa
        self.speedObsticals = self.const.speedObsticals
        self.turnSpeed = self.const.turnSpeed
        self.motionError = 1
        self.subTask = 1
        self.ticks = 0


    def update(self, image, motionError=1):
        self.motionError = motionError
        print(self.subTask)
        if self.subTask == 1: # turn left
            self.subTask1()
        
        elif self.subTask == 2:   #follow line
            self.subTask2(image)

        elif self.subTask == 3:   #turn left
            self.subTask3(image)

        elif self.subTask == 4:    #task 2 complete
            self.robot.setActiveTask(4)

        else:
            print(f"Error in task3. subTaskCount out of bounce, subtask is: {self.subTask} ")


    def subTask1(self):
        self.cameraServo.down()
        self.motorControl.rotateLeft(self.const.quartRotationSpeed, self.motionError)
        sleep(self.const.quartRotationTime)  
        self.motorControl.stop()
        self.subTask = 2

    def subTask2(self, image): #cross to next cross
        line, atCross, angle, offset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine( line, angle, offset ,self.speedHill, lostLine, self.motionError)
        if atCross:
            self.subTask = 3

    def subTask3(self,image): #turn left
        self.motorControl.rotateLeft(self.const.quartRotationSpeed, self.motionError)
        sleep(self.const.quartRotationTime) 
        self.motorControl.stop()
        self.subTask = 4
        