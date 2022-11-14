import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, GripperCommand

LEFT_PLACE = np.array([0.59050,-0.24279, 0.38833])
RIGTH_PLACE = np.array([0.59050,-0.2891, 0.38797])
CENTER_PLACE = (LEFT_PLACE + RIGTH_PLACE)/2

class CartPTPCommand(Command):
    def __init__(self, func_pointer, cart_position: MotionCartPose, speed = 100, accel = 1000, smooth = 0.0):
        self.__func = func_pointer

        self.__cart_position  = cart_position
        self.__speed = speed
        self.__accel = accel
        self.__smooth = smooth
        Command.__init__(self)

    def command_func(self):
        self.__func(
            self.__cart_position.to_robot_type(),
            self.__speed, 
            self.__accel,
            self.__smooth,
            self.__cart_position.tool_name
        )

ALONG_Z_ORIENT = np.array((0.0, -np.pi/2, -np.pi))
MAX_SPEED = 100

OPEN_GRIPPER = GripperCommand("grab", False)
MOVE_TO_CHECK_QR = CartPTPCommand(line, MotionCartPose.from_array(CENTER_PLACE[:3], CENTER_PLACE[3:]))
MOVE_TO_LEFT_QR = CartPTPCommand(line, MotionCartPose.from_array(LEFT_PLACE[:3], LEFT_PLACE[3:]))
MOVE_TO_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_PLACE[:3], RIGTH_PLACE[3:]))
TAKE_LEFT_QR    = CartPTPCommand(line, MotionCartPose.from_array(LEFT_PLACE[:3]- np.array([0,0,10]), LEFT_PLACE[3:]))
TAKE_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_PLACE[:3] - np.array([0,0,10]), RIGTH_PLACE[3:]))
CLOSE_GRIPPER = GripperCommand("grab", True)

def execute_commands(cmd_list: list):
    for c in cmd_list:
        c.execute()

def main():
    execute_commands([OPEN_GRIPPER, MOVE_TO_CHECK_QR])
    qr_detector = QRDetector()
    start_time = time.time()
    while (time.time() - start_time) < 5.0:
        detect = qr_detector.detector
        if detect is None:
            continue
        if detect.isDetect:
            for i in range(detect.N):
                det = detect[i]
                if det.center[1] > 640/2:
                    execute_commands([MOVE_TO_RIGTH_QR, TAKE_RIGTH_QR,CLOSE_GRIPPER, MOVE_TO_RIGTH_QR])
                    # rigth
                else:
                    execute_commands([MOVE_TO_LEFT_QR, TAKE_LEFT_QR,CLOSE_GRIPPER, MOVE_TO_LEFT_QR])
                    # left 


if __name__ == "__main__":
    main()