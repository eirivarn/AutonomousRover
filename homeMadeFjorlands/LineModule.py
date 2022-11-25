from Utils import *
import cv2
from Image import Image
import numpy as np

class LineModule:
    def __init__(self, isHeadless, robot, const):
        self.isHeadless = isHeadless
        self.robot = robot
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.N_SLICES = const.n_slices
        self.images = []
        self.const = const
        self.crossPosition = np.zeros(self.N_SLICES)

        self.m = 0
        self.c = 0

        for _ in range(self.N_SLICES):
            self.images.append(Image(const),)        


    def analyzeImage(self, image):
        self.viewImage('clear',image)

        removedBgImg = RemoveBackground(image, True)
        atCross = False
        list = []
        lostPoints = 0
        lostLine = False
        

        if removedBgImg is not None:
            SlicePart(removedBgImg, self.images, self.N_SLICES)
            for i in range(self.N_SLICES):
                list.append(self.images[i].getOffset())
                if i == 0 or i == self.N_SLICES-1:
                    self.robot.updateCrossConf(i)
                elif self.images[i].crossFound():
                    self.robot.updateCrossConf(i) 
                else: 
                    self.crossPosition[i] = 1
            repackedImg = RepackImages(self.images)

        x = []
        y = []
        h, w  = image.shape[:2]

        for i in range(self.N_SLICES):
            offs = list[i]
            if offs != 0:
                x.append(offs)
                y.append(h/(self.N_SLICES*2) + h/self.N_SLICES*i)
            else: 
                lostPoints += 1 
            
        if lostPoints > self.N_SLICES - 3: 
            lostLine = True


        if len(x)==0:
            x.append(0)
            x.append(0)
            y.append(h*(1/3))
            y.append(h*(2/3))
        
        x = np.array(x)
        y = np.array(y)
        #prøver å kun bruke de 3/4 øverste punktene til lin reg. har økt til 8 punkter:
        #x = x[:int(self.N_SLICES * self.const.offsetPosition)]
        #y = y[:int(self.N_SLICES * self.const.offsetPosition)]

        #print(x, '\n', y)
        A = np.vstack([x, np.ones(len(x))]).T

        self.m, self.c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        inversedAngle = np.rad2deg(np.arctan(self.m))
        if inversedAngle >= 0:
            angle = 90 - inversedAngle
        if inversedAngle < 0:
            angle = -90 - inversedAngle

        angle = -angle
        offset = list[-1]
        #offset = self.predict(self.const.resolution[1]/2)

        try:
            y1 = self.const.linRegPlotY1
            x1 = int(self.const.resolution[0]/2 - self.predict(y1))
            y2 = h-1
            x2 = int(self.const.resolution[0]/2 - self.predict(y2))

            cv2.line(repackedImg, (x1,y1), (x2,y2), (0,0,255), 3)
        except:
            print('Could not find line')
            
        repackedImg = self.drawSpeed(repackedImg)
        self.viewImage('slice',repackedImg)

        atCross = self.robot.crossConfirmed()

        wc=0
        hc=0
       
        blackAreas = cv2.inRange(image, (0,0,0), (50,50,50))
        blackAreas = self.improveLine(blackAreas)
        blackContours, hierarchy = cv2.findContours(blackAreas.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(blackContours) > 0:
            c = max(blackContours, key=cv2.contourArea) #biggest black contour area
            if cv2.contourArea(c)>800:
                xb, yb, wb, hb = cv2.boundingRect(c) #bounding box rectangle
                contourbox = cv2.minAreaRect(c) #contour tape rectangle
                (xc, yc), (wc,hc), angle = contourbox
                #determine angle and lateral offset
                angle = -self.preProcessAngle(angle,wc,hc)
                offset = int(320-xb-wb/2)

                cv2.rectangle(image,(xb,yb),(xb+wb,yb+hb),(0,255,0),2) #Bounding box   rgb bgr
                cv2.line(image, (int(xb+wb/2), yb), (int(xb+wb/2), yb+hb),(0,255,0), 2) #bounding box centerline
                cv2.line(image,(int(xb+wb/2), int(yb+hb/2)), (320, int(yb+hb/2)),(0,0,255), 1)# distance line
                cv2.line(image, (320, 10), (320, 350),(0,0,255), 1)#center line
                cv2.drawContours(image, [np.int0(cv2.boxPoints(contourbox))],0,(255,0,0), 2)#draw contourBox
                cv2.putText(image, f"{str(int(angle))}deg", (360,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#text>
                cv2.putText(image, str(offset)+"dist", (360,330),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#te>
                cv2.drawContours(image, blackContours,-1,(0,0,255),1)#draws all black contour lines
            else:
                lostLine=True 

        atCross = atCross and wc*hc >= self.const.minCrossAreaBlue  

        if atCross:
            cv2.putText(image, f"CROSS!!!{wc*hc}", (270, 70), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        image = self.drawSpeed(image)
        self.viewImage('strip', image)
        print(wc*hc)

        ##///////////Printing information
        print ("\n{:<8} {:<15} {:<15} ".format('Angle','Offset', 'Cross'))
        print ("{:<8} {:<15} {:<15} ".format("{0:.3f}".format(angle), "{0:.3f}".format(offset), atCross))   


        return list, atCross, angle, offset, lostLine

    def preProcessAngle(self,ang, w, h):
        if ang > 45 and w>h:
            ang = -(90-ang)
        elif ang <= 45 and h<w:
            ang = -(90-ang)
        return ang

    def improveLine(self,pic):
        kernel = np.ones((3,3),np.uint8)
        pic = cv2.erode(pic, kernel, iterations=4)
        pic = cv2.dilate(pic, kernel, iterations=4)
        return pic
        #return list, atCross, angle, offset, lostLine

    def flipPoint(self, x):
        return int(self.const.resolution[0]/2 - x)

    def predict(self, y):
        f_y = (y - self.c)/self.m
        return f_y

    def getEndOfLinePos(self, image):
        xPos, yPos = 999, 999
        endOfLineInImage = False
        up = 50
        lower = np.array([0, 0, 0], dtype = "uint8")
        upper = np.array([up, up, up], dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            contour = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(contour)
            xPos = int(x+w/2)
            yPos = y
            cv2.circle(image, (xPos, yPos), 3, (0,0,255), -1)
            self.viewImage("Kopp", image)
            if xPos and yPos != 999:
                endOfLineInImage = True
        return xPos, yPos, endOfLineInImage

    def endOfLineIsClose(self, yPos):
        return yPos > (self.const.resolution[0] - self.const.cupDistBuffer - 10)

    def crossAtPosition(self, position):
        return self.crossLocation[position]

    def viewImage(self,name, image):
        if not self.isHeadless:
            cv2.imshow(name, image)

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

    def quit(self):
        cv2.destroyAllWindows()
