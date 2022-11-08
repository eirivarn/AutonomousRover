from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from Utils import lineAngle, clamp
import numpy as np
import time
import VisionUtils
from motorControl import motorControl

class LineDetector:
    
    def __init__(self, motorControler):    
        #__start filming and setting video dimensions__
        self.camera = PiCamera()
        self.camera.resolution = (640, 360)
        #camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=(640, 360))
        self.motorController = motorControler
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
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)
            image = frame.array

            #self.__findLines(image, (0,0,0), (50,50,50))
            
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
                
                self.motorController.setAngLDist(int(angle), int(lateralOffset))
                
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

    '''# Line Identification Functions
    def __findLines(self, img, hueLow, hueHigh):
        img   = self.camera.read()

        rImg  = VisionUtils.isolateColor(img,   hueLow,  hueHigh)
        rGray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)
        ret, rThresh = cv2.threshold(rGray, 50, 255, cv2.THRESH_BINARY)

        # Make the image small to reduce line-finding processing times
        small = cv2.resize(rThresh, (64, 48), interpolation=cv2.INTER_AREA)




        # lines = cv2.HoughLinesP(edges, 1, np.pi, threshold=25, minLineLength=50, maxLineGap=10)
        lines = cv2.HoughLinesP(small, 1, np.pi/200, threshold=25, minLineLength=20, maxLineGap=10)


        if lines is None: return []

        cv2.imshow('final', rThresh)
        cv2.waitKey(2500)

        # If lines were found, combine them until you have 1 average for each 'direction' of tape in the photo
        lines = [line[0] for line in lines]
        combinedLines = self.__combineLines(lines, img)


        return combinedLines

    def __combineLines(self, unsortedLines, img):
        """ Combines similar lines into one large 'average' line """

        maxAngle = 45
        minLinesForCombo = 5

        def getAngle(line):
            # Turn angle from -180:180 to just 0:180
            angle = lineAngle(line[:2], line[2:])
            if angle < 0: angle += 180
            return angle

        def lineFits(checkLine, combo):
            """ Check if the line fits within this group of combos by checking it's angle """
            checkAngle = getAngle(checkLine)
            for line in combo:
                angle = lineAngle(line[:2], line[2:])
                difference = abs(checkAngle - angle)

                if difference < maxAngle or 180 - difference < maxAngle:
                    return True
                # if difference > maxAngle * 2 or 180 - difference > maxAngle * 2:
                #     return False
            return False

        # Pre-process lines so that lines always point from 0 degrees to 180, and not over
        for i, line in enumerate(unsortedLines):
            angle = lineAngle(line[:2], line[2:])
            if angle < 0:
                line = np.concatenate((line[2:], line[:2]))
                unsortedLines[i] = line


        # Get Line Combos
        lineCombos = []  # Format: [[[l1, l2, l3], [l4, l5, l6]], [[line 1...], [line 2...]]]

        while len(unsortedLines) > 0:
            checkLine = unsortedLines.pop(0)

            isSorted = False
            for i, combo in enumerate(lineCombos):
                if lineFits(checkLine, combo):
                    # Process the line so that the [x1, y1, and x2, y2] are in the same positions as other combos
                    lineCombos[i].append(checkLine.tolist())
                    isSorted = True
                    break

            if not isSorted:
                lineCombos.append([checkLine.tolist()])


        # # Limit each combo to minSamples, keeping only the longest lines
        lineCombos = [sorted(combo, key= lambda c: (c[0] - c[2]) ** 2 + (c[1] - c[3]) ** 2, reverse=True)
                       for combo in lineCombos]
        lineCombos = [combo[:minLinesForCombo] for combo in lineCombos]


        # Filter and Average Combo Groups Format: [[L1], [L2], [L3]]
        averagedCombos = []
        for combo in lineCombos:
            if len(combo) < minLinesForCombo: continue

            avgLine = (np.sum(combo, axis=0) / len(combo)).astype(int)
            avgLine *= 10  # Rescale to screen size
            averagedCombos.append(Line(avgLine[:2], avgLine[2:]))  ##TODO skal det stå line eller Line??


        # # Draw Line Combos and Final Lines
        #img = self.rover.camera.read()
        for i, combo in enumerate(lineCombos):
             for x1, y1, x2, y2 in combo:
                 x1 *= 10
                 y1 *= 10
                 x2 *= 10
                 y2 *= 10
        
                 cv2.line(img, (x1, y1), (x2, y2), (80*i, 80*i, 80*i), 2)
        
        if len(averagedCombos):
             for p1, p2 in averagedCombos:
                 x1 = p1[0]
                 y1 = p1[1]
                 x2 = p2[0]
                 y2 = p2[1]
        
                 cv2.line(img, (x1, y1), (x2, y2), (80, 80, 80), 8)
        
        cv2.imshow('final', img)
        cv2.waitKey(2500)

        return averagedCombos'''


    def quit(self):
        cv2.destroyAllWindows()

