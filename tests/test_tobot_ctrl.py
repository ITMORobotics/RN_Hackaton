import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.robot_ctrl.robot import RobotControl, MotionCartPose
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

N = 5

def main():
    robot_ctrl = RobotControl()
    start_time = time.time()
    
    for i in range(0, N):
        robot_ctrl.move_line

if __name__ == "__main__":
    main()