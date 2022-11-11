import cv2
import numpy as np
import pandas as pd
from pyzbar.pyzbar import decode

def qr_detect(frame):
    result = decode(frame)
    return result

def main():
    cap = cv2.VideoCapture(-1)
    ## Max resolution 1280x720
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # 800
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # 600
    if not cap.isOpened():
        exit("Unable to open camera")
    while True:
        ret, frame = cap.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detect_result = qr_detect(gray_frame)
            if len(detect_result) > 0:
                for dec in detect_result:
                    qr_center = (   int(dec.rect.left + dec.rect.width/2),
                                    int(dec.rect.top + dec.rect.height/2)
                                )
                    print(qr_center)
                    frame = cv2.circle(frame, qr_center,radius=2,color = (100,200,75), thickness = 10)
                    out_frame = cv2.polylines(frame,np.array([dec.polygon],np.int32),True, (255,255,255),4)
                    print("Core id: ",dec.data.decode('UTF-8'))
            else:
                out_frame = frame
            
        cv2.imshow('Example', out_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=="__main__":
    main()
    