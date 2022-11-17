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


    def analyzeImage(self, image):

        height, width  = image.shape[:2]
        self.middleX = int(width/2)
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

        cupInImage = False
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w ,h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x,y), (x + w, y + h), (0,255,0), 3)
                cv2.drawContours(image, contour, -1, (0,255,0), 3)
                self.xCenter = int(x + w/2)
                self.yCenter = int(y + h/2)
                cv2.circle(image, (self.xCenter, self.yCenter), 3, (255,0,255), thickness=-1)
                cupInImage = True
        
        if not self.isHeadless:
            cv2.imshow('Cup', image)

        cupPosX = self.getCupPos(cupInImage)
        cupIsClose = self.cupIsClose()

        return cupPosX, cupInImage, cupIsClose
        

    def getCupPos(self, cupInImage):
        if cupInImage:
            #xCenter = self.objectInfo[0][1][0] #TODO legg in sort slik at den koppen med høyest sikkerhet er den posisjonen som returneres
            return self.xCenter - self.middleX

    def cupIsClose(self):
        #TODO   enten return yCenter>terskel, eller let etter screenshot i bunn av bildet.
        return self.yCenter > self.const.cupIsClose

    def quit(self):
        self.breakLoop = True
        cv2.destroyAllWindows()




'''
        self.classNames = []
        self.classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
        with open(self.classFile,"rt") as f:
            self.classNames = f.read().rstrip("\n").split("\n")

        self.configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        self.weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

        self.net = cv2.dnn_DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(640, 368)
        self.net.setInputScale(1.0/ 127.5)              #nødvendig?
        self.net.setInputMean((127.5, 127.5, 127.5))    #Nødvendig?
        self.net.setInputSwapRB(True)                   #Nødvendig?
        self.result = None
        self.objectInfo = None
        self.info = None   #TODO lag get info funk
        self.middleX = 0
        self.xCenter = 0
        self.yCenter = 0


    def analyzeImage(self, image):

        height, width  = image.shape[:2]
        self.middleX = int(width/2) #Get X coordenate of the middle point

        img, self.objectInfo = self.getObjects(image,self.const.cupConfidence,0.2, objects=self.const.cupObjects)
        print(self.objectInfo)

        if not self.isHeadless: 
            cv2.imshow('Cup', img)
        #self.rawCapture.truncate(0)   #TODO finn ut om denne skal være her

        cupInImage = self.objectInfo != []
        cupPos = self.getCupPos(cupInImage)
        cupIsClose = self.cupIsClose()

        return cupPos, cupInImage, cupIsClose   


    def getObjects(self, img, thres, nms, draw=True, objects=[]):
        classIds, confs, bbox = self.net.detect(img,confThreshold=thres,nmsThreshold=nms)
        if len(objects) == 0: objects = self.classNames
        objectInfo =[]
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classNames[classId - 1]
                
                if className in objects: 
                    [x1,y1,x2,y2] = box
                    self.xCenter = int(x1+x2/2)
                    self.yCenter = int(y1+y2/2)
                    center = (self.xCenter, self.yCenter)
                    objectInfo.append([box, center, className, confidence])
                    if (draw):
                        cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                        cv2.circle(img, (self.xCenter, self.yCenter), 3, (255,0,255), thickness=-1)
                        cv2.putText(img,self.classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                                
        return img,objectInfo'''