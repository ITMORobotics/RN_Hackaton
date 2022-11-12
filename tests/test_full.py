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
    np.array((0.66653, 0.20485, 0.53256)),
    np.array((0.89301, 0.19039, 0.53297))
)
OPEN_GRIPPER = GripperCommand("Signal", False)
CLOSE_GRIPPER = GripperCommand("Signal", True)

CATCH_ORIENT = np.radians(np.array((156.8, 0.0, 0.0)))
DEFAULT_ORIENT = np.array((np.pi, 0.0, 0.0))

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
    global KERN_ID
    LEFT_KERN_PLACE = np.array([0.59050,-0.24279, 0.38833])
    RIGTH_KERN_PLACE = np.array([0.59050,-0.2891, 0.38797])
    CENTER_KERN_PLACE = (LEFT_KERN_PLACE + RIGTH_KERN_PLACE)/2

    MOVE_TO_CHECK_QR = CartPTPCommand(line, MotionCartPose.from_array(CENTER_KERN_PLACE[:3], CENTER_KERN_PLACE[3:], tool_name = 'ggrip'))
    MOVE_TO_LEFT_QR = CartPTPCommand(line, MotionCartPose.from_array(LEFT_KERN_PLACE[:3], LEFT_KERN_PLACE[3:], tool_name = 'ggrip'))
    MOVE_TO_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_KERN_PLACE[:3], RIGTH_KERN_PLACE[3:], tool_name = 'ggrip'))
    TAKE_LEFT_QR    = CartPTPCommand(line, MotionCartPose.from_array(LEFT_KERN_PLACE[:3]- np.array([0,0,0.010]), LEFT_KERN_PLACE[3:], tool_name = 'ggrip'))
    TAKE_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_KERN_PLACE[:3] - np.array([0,0,0.010]), RIGTH_KERN_PLACE[3:], tool_name = 'ggrip'))

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
                KERN_ID = det.info
                if det.center[1] > 640/2:
                    # rigth
                    execute_commands([MOVE_TO_RIGTH_QR, TAKE_RIGTH_QR,CLOSE_GRIPPER, MOVE_TO_RIGTH_QR])
                else:
                    # left 
                    execute_commands([MOVE_TO_LEFT_QR, TAKE_LEFT_QR,CLOSE_GRIPPER, MOVE_TO_LEFT_QR])

def stage_2_get_container_from_stelazh(container_pose: np.ndarray):
    GET_CONTAINER_FROM_STELAGE = [
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(container_pose , CATCH_ORIENT, tool_name = 'ggrip')), # under catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, 0.0,0.013)), CATCH_ORIENT, tool_name = 'ggrip')), # in catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, -0.20, 0.013)), CATCH_ORIENT, tool_name = 'ggrip')), # get catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, -0.20, 0.1)), CATCH_ORIENT, tool_name = 'ggrip')), # take up catch container
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7518, -0.479, 0.55691)), CATCH_ORIENT, tool_name = 'ggrip')), # take container under vesi
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7518, -0.479, 0.49691)), CATCH_ORIENT, tool_name = 'ggrip')), # take up catch container
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7518, -0.479, 0.55691)), CATCH_ORIENT, tool_name = 'ggrip')), # take container under vesi
    ]
    execute_commands(GET_CONTAINER_FROM_STELAGE)

def stage_3_perform_kern():
    execute_commands(GET_CONTAINER_FROM_STELAGE)

def stage_4_put_container_on_scale():
    MOVE_CONTAINER_WITH_KERN = [
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428)), CATCH_ORIENT, tool_name = 'ggrip')), # under catch container
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.362)), CATCH_ORIENT, tool_name = 'ggrip')), # step1 container left up
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.382)), CATCH_ORIENT, tool_name = 'ggrip')), # step2_container left down
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.5, 0.54428)), CATCH_ORIENT, tool_name = 'ggrip')) # step4_container take up
    ]
    execute_commands(MOVE_CONTAINER_WITH_KERN)



def main():
    #cell = Cell('hackaton.db', 'COM4', calibrate_points = CALIBRATE_STELAZH)
    #index = cell.get_index(KERN_ID)
    #notify(index)
    #container_pose = cell.stelazh[index[0], index[1]]

    # notify(container_pose)
    # # stage_1_move_to_qr()
    
    # stage_2_get_container_from_stelazh(CALIBRATE_STELAZH[0])
    stage_4_put_container_on_scale()


if __name__ == "__main__":
    main()