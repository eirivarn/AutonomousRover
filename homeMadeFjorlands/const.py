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


        ## //// Cup colors //// hsv
        self.highBlue = (130,255,255)
        self.lowBlue = (90,120,150)
        self.highRed = (20, 255,  255)
        self.lowRed = (160, 175, 175)
        self.highWhite = (180,25,255)
        self.lowWhite = (0, 0, 225)
        ## ////////////////////
