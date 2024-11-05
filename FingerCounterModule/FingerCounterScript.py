import cv2
import os
from HandTrackingmodule import HandTracking

class FingerCounterClass:
    def __init__(self) -> None:
        self.folderPath = "Finger_images"
        self.fingersList  = os.listdir(self.folderPath)
        self.down_width = 200
        self.down_height = 200
        self.down_points = (self.down_width, self.down_height)
        self.htm =HandTracking()
        self.tipIds= [4,8,12,16,20]


    def CountFingers(self,img):
        overlayList= []
        for impath in self.fingersList:
            image=cv2.imread(f'{self.folderPath}/{impath}')
            resized_image= cv2.resize(image, self.down_points, interpolation= cv2.INTER_LINEAR)
            overlayList.append(resized_image)

        
        img = self.htm.Track_Hands(img)
        lmlist = self.htm.find_postion(img,draw=False)
        # print(lmlist)
        fingers=[]
        if len(lmlist) !=0:
            #Thumb
            if lmlist[self.tipIds[0]][1] > lmlist[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # four fingers
            for id in range(1,5):
                if lmlist[self.tipIds[id]][2] < lmlist[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        # print(fingers)

            total_finger= fingers.count(1)
            # print(total_finger)


            h,w,c =overlayList[total_finger].shape
            img[0:h,0:w]=overlayList[total_finger]


            cv2.rectangle(img,(20,255),(170,425),(255,0,0),cv2.FILLED)
            cv2.putText(img,f'{total_finger}',(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,255,255),25)


        




        return img