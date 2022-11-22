import numpy as np

class Const:
    def __init__(self):
        self.isHeadless = False

        self.speed = 16
        self.turnSpeed = 35
        self.cupDistBuffer = 40
        self.cupPosBuffer = 70
        self.lineDistBuffer = 2
        self.posDistBuffer = 30
        self.need4speed = 70  #tør me å vinna??

        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15

        self.kp = 0.05
        self.kd = 0.12
        self.ki = 0.005

        self.n_slices = 6
        self.threshGrey = 65
        self.crossWidth = 300
        self.cupConfidence = 0.55
        self.cupObjects = ['cup','bowl']
        self.cupIsClose = 55

        self.i_line = 2
        self.lineArea = 700

        self.resolution = (640, 380)
        self.offsetPosition = 0,35 
        self.linRegPlotY1 = 1
        #self.linRegPlotY2 = int(self.resolution[1] * self.offsetPosition)
        self.linRegPlotY2 = 379

        ## //// Cup colors //// hsv ///
        self.highBlue = np.array([130, 255, 255])
        self.lowBlue =  np.array([90 , 100 , 100 ])
        self.highRed1 = np.array([5 , 255, 255])
        self.lowRed1 =  np.array([0  , 150 , 100 ])
        self.highRed2 = np.array([179, 255, 255])
        self.lowRed2 =  np.array([160, 150 , 100 ])
        self.highWhite =np.array([179, 15 , 255])
        self.lowWhite = np.array([0  , 0  , 210])
        ## ////////////////////////////

        ##/////////// Servo //////////
        self.open_val = -0.2
        self.close_val = 0.35
        self.up = 1
        self.down = 0.5



