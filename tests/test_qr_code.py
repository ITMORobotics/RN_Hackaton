import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

def main():
    qr_detector = QRDetector()
    start_time = time.time()
    while (time.time() - start_time) < 5.0:
        detect = qr_detector.detector
        if detect is None:
            continue
        if detect.isDetect:
            for i in range(detect.N):
                det = detect[i]
                # frame = cv2.circle(frame, det.center,radius=2,color = (100,200,75), thickness = 10)
                # out_frame = cv2.polylines(frame,det.poligon,True, (255,255,255),4)
                print("Core id: ",det.info)
            
            # else:
            #     out_frame = frame

            # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            # cv2.imshow('title', frame)

if __name__ == "__main__":
    main()