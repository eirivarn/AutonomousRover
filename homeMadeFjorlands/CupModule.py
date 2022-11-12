import time
import cv2

class CupModule:
    def __init__(self, isHedless):
        self.isHeadless = isHedless
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


    def analyzeImage(self, image):
        img, self.objectInfo = self.getObjects(image,0.6,0.2, objects=['cup','bowl'])
        print(self.objectInfo)

        if not self.isHeadless: 
            cv2.imshow('Cup', img)
        self.rawCapture.truncate(0)

        #TODO cupPos dist from center of cup to center of image
        #TODO cupInImage bool
        #TODO cupIsClose bool
        return self.info   #TODO info


    def getObjects(self, img, thres, nms, draw=True, objects=[]):
        classIds, confs, bbox = self.net.detect(img,confThreshold=thres,nmsThreshold=nms)
        if len(objects) == 0: objects = self.classNames
        objectInfo =[]
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classNames[classId - 1]
                
                if className in objects: 
                    [x1,y1,x2,y2] = box
                    xCenter = int(x1+x2/2)
                    yCenter = int(y1+y2/2)
                    center = (xCenter, yCenter)
                    objectInfo.append([box, center, className, confidence])
                    if (draw):
                        
                        cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                        cv2.circle(img, (xCenter, yCenter), 3, (255,0,255), thickness=-1)
                        cv2.putText(img,self.classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                                
        return img,objectInfo


    def quit(self):
        self.breakLoop = True
        cv2.destroyAllWindows()