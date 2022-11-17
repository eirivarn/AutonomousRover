import numpy as np

class Const:
    def __init__(self):
        self.isHeadless = False

        self.speed = 20
        self.turnSpeed = 20
        self.cupDistBuffer = 2
        self.cupPosBuffer = 70
        self.lineDistBuffer = 2
        self.posDistBuffer = 30
        self.need4speed = 70  #tør me å vinna??

        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15

        self.kp = 0.13
        self.ap = 0.2

        self.n_slices = 8
        self.threshGrey = 65
        self.crossWidth = 300
        self.cupConfidence = 0.55
        self.cupObjects = ['cup','bowl']
        self.cupIsClose = 100

        self.i_line = 2

        self.resolution = (640, 380)
        self.offsetPosition = 7/8   #regner offset fra 3/4 ned på skjermen
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
