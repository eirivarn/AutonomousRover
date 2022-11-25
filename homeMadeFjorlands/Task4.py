from time import sleep
from Task import Task


class Task4(Task):
    def __init__(self, motorContorl, lineModule, cupModule, const, robot):
        super().__init__(motorContorl, lineModule, cupModule, const, robot)
        self.turnSpeed = const.turnSpeed

    def update(self, image, motionError):
        pass

    def subtask1(self, image, motionError):#kamera ned
        self.cameraServo.down()
        self.gripperServo.openGripper()
        self.subTask=2

    def subtask2(self, image, motionError):#snu venstre
        #TODO eirik 90 deg left
        self.subTask = 3
    def subtask3(self, image, motionError):#kjør forbi 2 kryss
        line, atCross, angle, lateralOffset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, angle, lateralOffset, self.speed, lostLine, self.motionError)
        if atCross:
            sleep(0.1)
            self.motorControl.stop()
            self.subTask=4

    def subtask4(self, image, motionError):#stopp
        line, atCross, angle, lateralOffset, lostLine = self.lineModule.analyzeImage(image)
        self.motorControl.followLine(line, angle, lateralOffset, self.speed, lostLine, self.motionError)
        if atCross:
            self.motorControl.stop()
            sleep(0.8)
            self.subTask=5
    def subtask5(self, image, motionError):#kamera opp
        self.cameraServo.up()
        sleep(0.5)
        self.subTask = 6
    def subtask6(self, image, motionError):#hardkod en liten venstre rotate
        self.motorControl.rotateLeft(self.turnSpeed)
        sleep(0.08)  #TODO
        self.motorControl.stop()
        self,subTask = 7
    def subtask7(self, image, motionError):#turn sakte til høyre til kop er in image, og kopp er in center
        cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
        if int(cupPos) in range(-self.const.cupPosBuffer,self.const.cupPosBuffer)
            self.motorControl.stop()
            sleep(0.5)
            self.subTask = 8
        elif cupInImage:
            self.motorControl.turnToPos(cupPos)


    def subtask8(self, image, motionError):#go to cup, cup is close, stop
        cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
        if cupIsClose:
            self.motorControl.stop()
            sleep(0.5)
            self.subTask = 9
        self.motorControl.goToPos(cupPos, self.speed)

    def subtask9(self, image, motionError):#close gripper
        self.gripperServo.closeGripper()
        self.subTask=9
    def subtask10(self, image, motionError):#180 deg turn left
        self.motorControl.rotateLeft(45)
        sleep()
    def subtask11(self, image, motionError):#kjør et stykke, definert i motion ticks
    def subtask12(self, image, motionError):#slipp kopp
    def subtask13(self, image, motionError):#rygg litt
    def subtask14(self, image, motionError):#snu mot venstre til kopp er i center
    def subtask15(self, image, motionError):#gå til cup, cup is close ,stop
    def subtask16(self, image, motionError):#180 deg 
    def subtask17(self, image, motionError):#kjør litt
    def subtask18(self, image, motionError):#stopp
    def subtask19(self, image, motionError):#slipp
    def subtask20(self, image, motionError):#rygg
