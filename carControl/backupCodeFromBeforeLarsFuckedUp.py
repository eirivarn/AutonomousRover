from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import time
from motorControl import motorControl

class LineDetector:
    def __init__(self, controller):    
        #__start filming and setting video dimensions__
        self.camera = PiCamera()
        self.camera.resolution = (640, 360)
        #camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=(640, 360))
        self.controller = controller
        time.sleep(0.1)
    
    def improveLine(self,pic):
        kernel = np.ones((3,3),np.uint8)
        pic = cv2.erode(pic, kernel, iterations=4)
        pic = cv2.dilate(pic, kernel, iterations=4)
        return pic
    
    def preProcessAngle(self,ang, w, h):
        if ang > 45 and w>h:
            ang = -(90-ang)
        elif ang <= 45 and h<w:
            ang = -(90-ang)
        return ang
    
    def analyzeStrip(self):
        c = -1
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            image = frame.array
            #differentiate black black areas
            blackAreas = cv2.inRange(image, (0,0,0), (50,50,50))
            blackAreas = self.improveLine(blackAreas)
            blackContours, hierarchy = cv2.findContours(blackAreas.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(blackContours) > 0:
                c = max(blackContours, key=cv2.contourArea) #biggest black contour area
                xb, yb, wb, hb = cv2.boundingRect(c) #bounding box rectangle
                contourbox = cv2.minAreaRect(c) #contour tape rectangle
                (xc, yc), (wc,hc), angle = contourbox
                #determine angle and lateral offset
                angle = self.preProcessAngle(angle,wc,hc)
                lateralOffset = int(320-xb-wb/2)
                
                self.controller.setAngLDist(int(angle), int(lateralOffset))
                
                #Write boxes and lines to image
                cv2.rectangle(image,(xb,yb),(xb+wb,yb+hb),(0,255,0),2) #Bounding box
                cv2.line(image, (int(xb+wb/2), yb), (int(xb+wb/2), yb+hb),(0,255,0), 2) #bounding box centerline
                cv2.line(image,(int(xb+wb/2), int(yb+hb/2)), (320, int(yb+hb/2)),(0,0,255), 1)# distance line
                cv2.line(image, (320, 10), (320, 350),(0,0,255), 1)#center line
                cv2.drawContours(image, [np.int0(cv2.boxPoints(contourbox))],0,(255,0,0), 2)#draw contourBox
                cv2.putText(image, f"{str(int(angle))}deg", (360,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#text>
                cv2.putText(image, str(lateralOffset)+"dist", (360,330),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)#te>
                cv2.drawContours(image, blackContours,-1,(0,0,255),1)#draws all black contour lines
        
            #display video
            #cv2.imshow("Blackline",blackLine)
            cv2.imshow("Image", image)
            self.rawCapture.truncate(0)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    cv2.destroyAllWindows()

class Driver:
    def __init__(self):
        
        self.motorControl = motorControl()
        self.speed = 25
        self.turnSpeed = 25
        self.curvRateNew = 5
        self.curvRate = 0
        self.curvRateSenitivity = 0
    
    def forward(self):
        self.curvRate = 0
        self.motorControl.forward(self.speed)
 
    def backward(self):
        self.curvRate = 0
        self.motorControl.backward(self.speed)
 
    def left(self):
        #curvRate += curvRateSenitivity
        if self.motorControl.getSpeed() == 0:
            self.motorControl.turnLeft(self.turnSpeed)
        else:
            self.motorControl.curv(-self.curvRateNew)
     
    def right(self):
        #curvRate -= curvRateSenitivity
        if self.motorControl.getSpeed() == 0:
            self.motorControl.turnRight(self.turnSpeed)
        else:
            self.motorControl.curv(self.curvRateNew)
            
    def curv(self, curvRate):
        self.motorControl.curv(curvRate)
            
    def stop(self):
        self.curvRate = 0
        self.motorControl.stop()
        
    def quit(self):
        self.curvRate = 0
        self.motorControl.quit()
    
    def drive(self, speed):
        print(f"set speed to: {speed}")
        motroControl.forward()
        
    
    def turn(self, amount):
        print(f"turning {amount}")
    
    #def stop(self):
    #   print("stopping")

class Controller:
    def __init__(self):
        self.driver = Driver()
        self.detector = LineDetector(self)
        self.prevAngle, self.prevDist = 0, 0
    
    def startCourse(self):
        self.driver.forward()
        self.detector.analyzeStrip()
    
    def setAngLDist(self, angle, dist):
        if angle != self.prevAngle:
            self.prevAngle = angle
            self.driver.curv(angle/10)
        

controller = Controller()
controller.startCourse()
