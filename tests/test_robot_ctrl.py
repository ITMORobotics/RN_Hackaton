import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.robot.robot_ctrl import RobotControl, MotionCartPose
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

N = 5
bias_random_pose = np.array([0.9, 0.0, 0.5])

def main():
    robot_ctrl = RobotControl("grab ")
    start_time = time.time()
    
    for i in range(0, N):
        random_pose = bias_random_pose + np.random.uniform(low=-0.2, high =0.2, size = 3)
        motion_cp = MotionCartPose.from_array(random_pose[:3])
        # robot_ctrl.toogle_gripper(True)

        print(robot_ctrl.pose)
        notify(robot_ctrl.pose.cart_point)
        line(
            motion_cp.to_robot_type(),
            100, 
            1000,
            0.0,
            'Flange'
        )

if __name__ == "__main__":
    main()