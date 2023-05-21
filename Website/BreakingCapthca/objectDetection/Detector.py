import cv2
import os
import numpy as np
import time
import pytesseract 
from PIL import Image as IM 


class Detector:
   def __init__(self, videoPath, configPath, modelPath, classesPath):
      self.videoPath = videoPath
      self.configPath = configPath 
      self.modelPath = modelPath 
      self.classesPath = classesPath
   

      self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
      self.net.setInputSize(340,320)
      self.net.setInputScale(1.0/129.5)
      self.net.setInputMean((127.5, 127.5, 127.5)) 
      self.net.setInputSwapRB(True)

      self.readClasses()
    
   def readClasses (self):
      with open(self.classesPath, 'r') as f: 
         self.classesList = f.read().splitlines()
    
      self.classesList.insert(0, '__Background__')

      self.colorList = np.random.uniform(low=0, high=200, size=(len(self.classesList), 3))
 
      print(self.classesList)
   
   def processCaptcha(self, captchaImage): #captcha
    # Convert captcha image to grayscale
    captchaImage = captchaImage.convert('L')
    
    # Apply OCR using pytesseract
    captchaText = pytesseract.image_to_string(captchaImage)
    
    return captchaText

     
   def onVideo(self):
      cap = cv2.VideoCapture(self.videoPath)
      
      if (cap.isOpened()==False):
         print("Error opening file...")
         return
   
      (success, image) = cap.read()


      while success:
         classLabelIDs, confidences, bboxs = self.net.detect (image, confThreshold = 0.5)
         bboxs = list (bboxs)
         confidences = list(np.array(confidences).reshape(1,-1)[0])
         confidences = list(map (float, confidences))
      
         bboxIdx = cv2.dnn.NMSBoxes (bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)
         
         if len(bboxIdx) != 0:
            for i in range(0, len(bboxIdx)):
               bbox = bboxs [np.squeeze (bboxIdx[i])]
               classConfidence = confidences[np.squeeze (bboxIdx[i])]
               classLabelID= np.squeeze (classLabelIDs [np.squeeze (bboxIdx[i])])
               classLabel = self.classesList[classLabelID]
               
               classColor = [int(v) for v in self.colorList[classLabelID]]

               displayText = "{}:{:.1f}".format(classLabel, classConfidence)

               x,y,w,h = bbox
               
               cv2.rectangle(image, (x,y), (x+w, y+h), color=classColor, thickness=1)
               cv2.putText(image, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

               # Extract captcha region and process
               captchaRegion = image[y:y + h, x:x + w]
               captchaImage = IM.fromarray(cv2.cvtColor(captchaRegion, cv2.COLOR_BGR2RGB))
               captchaText = self.processCaptcha(captchaImage)

                # Display captcha text
               cv2.putText(image, captchaText, (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                # Save captcha text to file
               with open("captchas.txt", "a") as f:
                  f.write(captchaText + "\n")

              

         cv2.imshow("Result is", image)
         key= cv2.waitKey(1) & 0xFF 
         if key == ord("q"): 
            break
      
         (success, image) = cap.read() 
      cv2.destroyAllWindows()

def main():
    videoPath = 0 #to use webcam change the above para to 0
    #press 'q' exit webcam

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()

if __name__ == '__main__':
    main()