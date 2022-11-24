import cv2

class CupModule:
    def __init__(self, isHedless ,const):
        self.isHeadless = isHedless
        self.const = const
        self.xCenter = 1
        self.yCenter = 1
        self.highBlue = const.highBlue
        self.lowBlue = const.lowBlue
        self.highRed1 = const.highRed1
        self.lowRed1 = const.lowRed1
        self.highRed2 = const.highRed2
        self.lowRed2 = const.lowRed2
        self.highWhite = const.highWhite
        self.lowWhite = const.lowWhite
        self.height, self.width = 0 , 0


    def analyzeImage(self, image, robot):
        self.robot = robot
        self.height, self.width  = image.shape[:2]
        self.middleX = int(self.width/2)
        self.xCenter = 1
        self.yCenter = 1

        blurredImage = cv2.GaussianBlur(image, (5,5), 0)
        hsv = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2HSV)

        maskBlue = cv2.inRange(hsv, self.lowBlue, self.highBlue)
        maskRed1 = cv2.inRange(hsv, self.lowRed1, self.highRed1)
        maskRed2 = cv2.inRange(hsv, self.lowRed2, self.highRed2)
        maskWhite = cv2.inRange(hsv, self.lowWhite, self.highWhite)

        mask = maskBlue | maskRed1 | maskRed2 # | maskWhite
        
        contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contour = None
        greatestArea = 0
        cupInImage = False
        '''
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > greatestArea:
                contour = contours[i]
                greatestArea = area'''

        if len(contours) != 0:
            contour = max(contours, key=cv2.contourArea)    
            if len(contour) != 0:
                
                x, y, w ,h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x,y), (x + w, y + h), (0,255,0), 3)
                cv2.drawContours(image, contour, -1, (0,255,0), 3)
                self.xCenter = int(x + w/2)
                self.yCenter = int(y + h/2)
                cv2.circle(image, (self.xCenter, self.yCenter), 3, (255,0,255), thickness=-1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image,f"{self.height-self.yCenter}",(self.xCenter-20, self.yCenter), font, 0.7,(200,0,200),1)
                cupInImage = True
        
        image = self.drawSpeed(image)
        if not self.isHeadless:
            cv2.imshow('Cup', image)

        cupPosX = self.getCupPos(cupInImage)
        cupIsClose = self.cupIsClose()

        return cupPosX, cupInImage, cupIsClose
        

    def getCupPos(self, cupInImage):
        if cupInImage:
            return self.xCenter - self.middleX

    def cupIsClose(self):
        return self.yCenter > self.height - self.const.cupIsClose

    def quit(self):
        self.breakLoop = True
        cv2.destroyAllWindows()


    def drawSpeed(self, image):
        try:
            lSpeed, rSpeed = self.robot.motor.getSpeed()
            h, w = image.shape[:2]
            lx = 10
            rx = w-10
            y1 = int(h/2)
            ly2 = int(-(lSpeed/100)*(h/2-10) + h/2)
            ry2 = int(-(rSpeed/100)*(h/2-10) + h/2) 

            if lSpeed>0:
                lColor = (0,255,0)
            else:
                lColor = (0,0,255)

            if rSpeed>0:
                rColor = (0,255,0)
            else:
                rColor = (0,0,255)

            cv2.line(image, (lx,y1), (lx,ly2), lColor, 5)
            cv2.line(image, (rx,y1), (rx,ry2), rColor, 5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            cv2.putText(image,f"{int(lSpeed)}",(lx+7,ly2), font, 0.7,lColor,2)
            cv2.putText(image,f"{int(rSpeed)}",(rx-30,ry2), font, 0.7,rColor,2)

        finally:
            return image
