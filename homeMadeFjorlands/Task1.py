from Task import Task
import Main


class Task1(Task):
    speed = 0
    cupDistBuffer = 5

    def update(self, image):
        global speed, cupDistBuffer
        self.image = image
        if self.subTask == 1: #follow line to cross
            line, crossFound = self.lineModule.analyzeImage(image)
            self.motorControl.followLine(line, speed)
            if crossFound:
                self.motorControl.goToCross(speed)
                self.subtask = 2
        
        elif self.subTask == 2:  #turn left untill cup is in center
            cupPos, cupInImage = self.cupModule.analyzeImage(image)
            if not cupInImage:
                self.motorControl.turnLeft()
            else:
                self.motorControl.turnToPos(cupPos)
            if cupPos in range(-cupDistBuffer, cupDistBuffer):
                self.subTask = 3
            
        elif self.subTask == 3:  #turn drive forward to cup
            cupPos, cupInImage, cupIsClose = self.cupModule.analyzeImage(image)
            if cupIsClose:
                self.subTask = 4
                return 
            self.motorControl.goToCup(cupPos)
            
        elif self.subTask == 4: #pick up cup
            self.servo.close()
            self.subTask = 5            

        elif self.subTask == 5: # turn 90 deg to main line
            self.motorControl.turnLeft()
            #TODO
            
        elif self.subTask == 6: #turn 90 deg to side line
            self.motorControl.turnLeft()
            #TODO
            
        elif self.subTask == 7: #drop cup
            self.servo.open()
            

        elif self.subTask == 8: #turn back to main line and task 1 is complete


            Main.setActiveTask(2)






    