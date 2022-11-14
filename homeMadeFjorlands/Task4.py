from Task import Task


class Task4(Task):

    def __init__(self, motorContorl, lineModule, cupModule):
        super().__init__(motorContorl, lineModule, cupModule)
        self.subTask = 1

    def update(self, image):
        if self.subTask == 1:       #tilt camera up
            self.subTask1(image)
        
        elif self.subTask == 2:     #go to cup
            self.subTask2(image)
            
        elif self.subTask == 3:     #pick up cup
            self.subTask3(image)
            
        elif self.subTask == 4:     #return to line
            self.subTask4()
                       
        elif self.subTask == 5:     # turn 90 deg to main line
            self.subTask5(image)


    def subTask1(self, image):
        pass
    def subTask2(self, image):
        pass
    def subTask3(self, image):
        pass
    def subTask4(self, image):
        pass
    def subTask5(self, image):
        pass
    def subTask6(self, image):
        pass
    def subTask7(self, image):
        pass
    def subTask8(self, image):
        pass
    
    