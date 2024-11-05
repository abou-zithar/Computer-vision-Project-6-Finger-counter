
import  cv2
import numpy as np

from  HandTrackingmodule import HandTracking
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math



# volume.GetMute()
# volume.GetMasterVolumeLevel()

class VolumeHandControl:
    def __init__(self) -> None:
        self.htm = HandTracking(min_detection_confidence=0.7)
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.Vol_Range = self.volume.GetVolumeRange()
        self.minVol =self.Vol_Range[0]
        self.manVol =self.Vol_Range[1]
        self.vol = 0
        self.vol_bar= 400
        self.vol_num = 0
        

    def Change_Volume(self,img,draw =False):
        img = self.htm.Track_Hands(img)
        lmlist = self.htm.find_postion(img,draw)
            
        if len(lmlist)!=0:
            # print(lmlist[4],lmlist[8])
            x1,y1 = lmlist[4][1],lmlist[4][2]
            x2,y2 = lmlist[8][1],lmlist[8][2]
            cx,cy = (x1+x2)//2,(y1+y2)//2

            cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,0),cv2.FILLED)
            cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            length =  math.sqrt((x2-x1)**2 + (y2-y1)**2)
            # print(length)
            vol = np.interp(length,[20,250],[self.minVol,self.manVol])
            # print(vol)
            self.volume.SetMasterVolumeLevel(vol, None)
            if length < 50:
                
                cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
            
            self.vol_bar = np.interp(length,[20,250],[400,150])
            self.vol_num = np.interp(length,[20,250],[0,100])
        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(self.vol_bar)),(85,400),(255,0,0),cv2.FILLED)

        cv2.putText(img,f'{int(self.vol_num)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        
                
        return img



