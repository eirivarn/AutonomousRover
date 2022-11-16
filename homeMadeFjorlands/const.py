import numpy as np

class Const:
    def __init__(self):
        self.speed = 50
        self.turnSpeed = 80
        self.cupDistBuffer = 2
        self.cupPosBuffer = 10
        self.lineDistBuffer = 2
        self.posDistBuffer = 2
        self.need4speed = 70  #tør me å vinna??

        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15

        self.kp = 0.1
        self.ap = 0.5

        self.n_slices = 4
        self.threshGrey = 65
        self.crossWidth = 300
        self.cupConfidence = 0.55
        self.cupObjects = ['cup','bowl']
        self.cupIsClose = 100

        self.i_line = 2

        self.resolution = (640, 380)


        ## //// Cup colors //// hsv ///
        self.highBlue = np.array([130, 255, 255])
        self.lowBlue =  np.array([90 , 100 , 100 ])
        self.highRed1 = np.array([20 , 255, 255])
        self.lowRed1 =  np.array([0  , 100 , 100 ])
        self.highRed2 = np.array([179, 255, 255])
        self.lowRed2 =  np.array([160, 100 , 100 ])
        self.highWhite =np.array([179, 20 , 255])
        self.lowWhite = np.array([0  , 0  , 225])
        ## ////////////////////////////
