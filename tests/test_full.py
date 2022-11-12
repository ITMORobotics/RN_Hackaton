import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, GripperCommand
from rn_hackaton.cell.lab import Cell


from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

KERN_ID = 7681
CALIBRATE_STELAZH = (
    np.array((0.66653, 0.20485, 0.5456)),
    np.array((0.89301, 0.19039, 0.54397))
)
OPEN_GRIPPER = GripperCommand("grab", False)
CLOSE_GRIPPER = GripperCommand("grab", True)

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

def execute_commands(cmd_list: list):
    for c in cmd_list:
        c.execute()

def stage_1_move_to_qr():
    LEFT_KERN_PLACE = np.array([0.59050,-0.24279, 0.38833])
    RIGTH_KERN_PLACE = np.array([0.59050,-0.2891, 0.38797])
    CENTER_KERN_PLACE = (LEFT_KERN_PLACE + RIGTH_KERN_PLACE)/2

    MOVE_TO_CHECK_QR = CartPTPCommand(line, MotionCartPose.from_array(CENTER_PLACE[:3], CENTER_KERN_PLACE[3:]))
    MOVE_TO_LEFT_QR = CartPTPCommand(line, MotionCartPose.from_array(LEFT_KERN_PLACE[:3], LEFT_KERN_PLACE[3:]))
    MOVE_TO_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_KERN_PLACE[:3], RIGTH_KERN_PLACE[3:]))
    TAKE_LEFT_QR    = CartPTPCommand(line, MotionCartPose.from_array(LEFT_KERN_PLACE[:3]- np.array([0,0,0.010]), LEFT_KERN_PLACE[3:]))
    TAKE_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_KERN_PLACE[:3] - np.array([0,0,0.010]), RIGTH_KERN_PLACE[3:]))

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

def stage_2_move_container_with_kern():
    MOVE_CONTAINER_WITH_KERN = [
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.486, 0.622)), np.array((np.pi, 0.0, 0.0)), tool_name = 'ggrip')), # under catch container
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.486, 0.422)), np.array((np.pi, 0.0, 0.0)), tool_name = 'ggrip')), # step1 container left up
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.45673, 0.422)), np.array((np.pi, 0.0, 0.0)), tool_name = 'ggrip')), # step2_container left down
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7518, -0.479, 0.49691)), np.radians(np.array((156.8, 0.0, 0.0))), tool_name = 'ggrip')), # step3_container in down
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.6680, -0.46, 0.5573)), np.radians(np.array((156.8, 0.0, 0.0))), tool_name = 'ggrip')) # step4_container take up
    ]
    execute_commands(MOVE_CONTAINER_WITH_KERN)


def main():
    cell = Cell('tests/hackaton.db', 'COM4', calibrate_points = CALIBRATE_STELAZH)
    index = cell.get_index(KERN_ID)
    stelazh_pose = cell.stelazh[index[0], index[1]]

    stage_1_move_to_qr()
    stage_2_move_container_with_kern()


if __name__ == "__main__":
    main()