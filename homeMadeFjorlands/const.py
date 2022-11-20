import numpy as np

class Const:
    def __init__(self):
        self.isHeadless = False

        self.speed = 13
        self.turnSpeed = 40
        self.cupDistBuffer = 2
        self.cupPosBuffer = 70
        self.lineDistBuffer = 2
        self.posDistBuffer = 30
        self.need4speed = 70  #tør me å vinna??

        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15

        self.kp = 0.12
        self.kd = 0.3
        self.ki = 0.002

        self.n_slices = 6
        self.threshGrey = 65
        self.crossWidth = 300
        self.cupConfidence = 0.55
        self.cupObjects = ['cup','bowl']
        self.cupIsClose = 50

        self.i_line = 2

        self.resolution = (640, 380)
        self.offsetPosition = 0,35 #regner offset fra litt utenfor skjermen, mot roboten
        self.linRegPlotY1 = 1
        #self.linRegPlotY2 = int(self.resolution[1] * self.offsetPosition)
        self.linRegPlotY2 = 379

        ## //// Cup colors //// hsv ///
        self.highBlue = np.array([130, 255, 255])
        self.lowBlue =  np.array([90 , 100 , 100 ])
        self.highRed1 = np.array([10 , 255, 255])
        self.lowRed1 =  np.array([0  , 150 , 100 ])
        self.highRed2 = np.array([179, 255, 255])
        self.lowRed2 =  np.array([160, 150 , 100 ])
        self.highWhite =np.array([179, 15 , 255])
        self.lowWhite = np.array([0  , 0  , 210])
        ## ////////////////////////////

        ##/////////// Servo //////////
        self.open_val = 0.15
        self.close_val = 0.4
        self.up = 0.6
        self.down = 0.1



