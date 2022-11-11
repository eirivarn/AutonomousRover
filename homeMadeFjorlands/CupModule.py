import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

class CupModule:
    def __init__(self, isHedless):
        self.isHeadless = isHedless

        self.camera = PiCamera()
        self.camera.resolution = (640, 368)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        time.sleep(0.1)

        self.breakLoop = False
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


    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)

            image = frame.array
            
            self.result, self.objectInfo = self.getObjects(image,0.45,0.2, objects=['cup','bowl'])
            print(self.objectInfo)

            if not self.isHeadless and self.result != None:
                cv2.imshow('Image', self.result)
            self.rawCapture.truncate(0)
           
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            
            if self.breakLoop:
                self.breakLoop = False
                break



    def getObjects(self, img, thres, nms, draw=True, objects=[]):
        classIds, confs, bbox = self.net.detect(img,confThreshold=thres,nmsThreshold=nms)
        if len(objects) == 0: objects = self.classNames
        objectInfo =[]
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classNames[classId - 1]
                print(box)
                (x1, y1) ,(x2, y2) = box
                xCenter = (x1+x2)/2
                yCenter = (y1+y2)/2
                center = (xCenter, yCenter)
                if className in objects: 
                    objectInfo.append([box, center, className])
                    if (draw):
                        cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                        cv2.circle(img, (xCenter, yCenter), 3, (255,0,255), thickness=-1)
                        cv2.putText(img,self.classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        
                        time.sleep = 2
        
        return img,objectInfo


    def quit(self):
        self.breakLoop = True
        cv2.destroyAllWindows()