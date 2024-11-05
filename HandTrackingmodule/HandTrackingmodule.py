
import cv2
import mediapipe as mp 




class HandTracking:
    def __init__(self,mode=False,
               maxHands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5) -> None:
        
        self.mode = mode
        self.maxHands=maxHands
        self.model_complexity=model_complexity
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.model_complexity,
                                       self.min_detection_confidence,
                                        self.min_tracking_confidence )

        self.mpDraw = mp.solutions.drawing_utils


    def Track_Hands(self,img,draw=True):
        
        

        imgRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
            
        return img               
       
        

    def find_postion (self,img,handNum = 0 ,draw=False):
        lmlist= []

        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNum]
            for id , lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h,w,c = img.shape

                    cx,cy = int(lm.x *w) , int(lm.y*h)

                    # print(id,":",cx,cy)
                    lmlist.append([id,cx,cy])

                    if draw:
                        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        
        
        return lmlist