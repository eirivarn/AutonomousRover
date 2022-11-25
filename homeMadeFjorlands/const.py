import numpy as np

class Const:
    def __init__(self):
        self.isHeadless = False

        self.speed = 10
        self.turnSpeed = 22
        self.cupDistBuffer = 40
        self.cupPosBuffer = 70
        self.lineDistBuffer = 60
        self.posDistBuffer = 60
        self.quartRotationTime= 0.15
        self.quartRotationSpeed= 50

        self.need4speed = 15  #tør me å vinna?? tydelig vis ikkje :((
        self.speedTask3Hill = 10
        self.speedObsticals = 12

        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15

        self.kp = 0.04
        self.kd = 0.095
        self.ki = 0.002

        self.n_slices = 3
        self.threshGrey = 65
        self.crossWidth = 300
        self.cupConfidence = 0.55
        self.cupObjects = ['cup','bowl']
        self.cupIsClose = 100

        self.i_line = 2
        self.lineArea = 1000
        self.minCrossAreaBlue = 110000  #110 000

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
        self.open_val = 0.2
        self.close_val = 0.9
        self.up = 0.9
        self.down = 0.55


        #//////////init Speed/////////
        self.initSleep = 0.08
        self.speedBoozt = 85
        self.minSpeed4init = 1000
        self.deltaError = 0.6
        self.minMotionArea = 2000
        #self.nMotionCount = 4