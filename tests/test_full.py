import os
import sys
import time
import numpy as np
import copy

from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, GripperCommand
from rn_hackaton.cell.lab import Cell


from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

KERN_ID = 7681
CALIBRATE_STELAZH = (
    np.array((0.66653, 0.20485, 0.53256)),
    np.array((0.89301, 0.19039, 0.53297))
)
OPEN_GRIPPER = GripperCommand("grab", False)
CLOSE_GRIPPER = GripperCommand("grab", True)

CATCH_ORIENT = np.radians(np.array((156.8, 0.0, 0.0)))
PHOTO_ORIENT = np.radians(np.array((-90.0, 0.0, 0.0)))
DEFAULT_ORIENT = np.array((np.pi, 0.0, 0.0))

LEFT_KERN_PLACE = np.array([0.59050,-0.24279, 0.38833])
RIGTH_KERN_PLACE = np.array([0.59050,-0.2891, 0.38797])

KERN_PLACE = None

class CartPTPCommand(Command):
    def __init__(self, func_pointer, cart_position: MotionCartPose, speed = 200, accel = 1500, smooth = 0.0):
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

def stage_1_move_to_qr(cell: Cell, qr_detector: QRDetector):
    print("Stage 1")
    global KERN_ID

    MOVE_TO_LEFT_QR = CartPTPCommand(line, MotionCartPose.from_array(LEFT_KERN_PLACE, DEFAULT_ORIENT, tool_name = 'ggcam'))
    MOVE_TO_RIGTH_QR = CartPTPCommand(line, MotionCartPose.from_array(RIGTH_KERN_PLACE, DEFAULT_ORIENT, tool_name = 'ggcam'))

    start_time = time.time()
    
    while True:
        if cell.busy_kern_index is None:
                    continue

        if cell.busy_kern_index == 0:
            KERN_PLACE = RIGTH_KERN_PLACE
            execute_commands([MOVE_TO_RIGTH_QR])
        else: 
            KERN_PLACE = LEFT_KERN_PLACE
            execute_commands([MOVE_TO_LEFT_QR])
        break

    while (time.time() - start_time) < 5.0:
        detect = qr_detector.detector    
        if detect is None:
            continue
        if detect.isDetect:
            for i in range(detect.N):
                det = detect[i]
                KERN_ID = det.info
            


def stage_2_get_container_from_stelazh(container_pose: np.ndarray):
    print("Stage 2")
    GET_CONTAINER_FROM_STELAGE = [
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, -0.06 ,0.0)), CATCH_ORIENT, tool_name = 'ggrip')), # before catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose , CATCH_ORIENT, tool_name = 'ggrip')), # under catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, 0.0,0.013)), CATCH_ORIENT, tool_name = 'ggrip')), # in catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, -0.20, 0.013)), CATCH_ORIENT, tool_name = 'ggrip')), # get catch container
        CartPTPCommand(line, MotionCartPose.from_array(container_pose + np.array((0.0, -0.20, 0.1)), CATCH_ORIENT, tool_name = 'ggrip')), # take up catch container
    ]
    execute_commands(GET_CONTAINER_FROM_STELAGE)
    return copy.copy(GET_CONTAINER_FROM_STELAGE)

def stage_3_put_container_on_scale():
    print("Stage 3")
    MOVE_CONTAINER_WITHOUT_KERN = [
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428)), CATCH_ORIENT, tool_name = 'ggrip')), # step1 container in up
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.382)), CATCH_ORIENT, tool_name = 'ggrip')), # step2_container in down
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.53, 0.382)), CATCH_ORIENT, tool_name = 'ggrip')), # step3_container left down
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.53, 0.49428)), CATCH_ORIENT, tool_name = 'ggrip')) # step4_container left_up
    ]
    execute_commands(MOVE_CONTAINER_WITHOUT_KERN)
    return copy.copy(MOVE_CONTAINER_WITHOUT_KERN)

def stage_4_put_kern_on_scale():
    print("Stage 4")

    PUT_KERN_ON_SCALE = [
        CLOSE_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(KERN_PLACE + np.array((-0.05, 0.0 ,0.0)), DEFAULT_ORIENT, tool_name = 'ggrip')), # under kern
        CartPTPCommand(line, MotionCartPose.from_array(KERN_PLACE + np.array((-0.05, 0.0 ,-0.1)), DEFAULT_ORIENT, tool_name = 'ggrip')), # step down before kern
        CartPTPCommand(line, MotionCartPose.from_array(KERN_PLACE + np.array((0.05, 0.0 ,-0.1)), DEFAULT_ORIENT, tool_name = 'ggrip')), # push kern
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(KERN_PLACE + np.array((0.05, 0.0 ,-0.13)), DEFAULT_ORIENT, tool_name = 'ggrip')), # take kern
        CLOSE_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(KERN_PLACE + np.array((0.05, 0.0 ,0.0)), DEFAULT_ORIENT, tool_name = 'ggrip')), # go up
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428)), DEFAULT_ORIENT, tool_name = 'ggrip')), # go to scale
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428) + np.array((0.0, 0.0 ,-0.1)), DEFAULT_ORIENT, tool_name = 'ggrip')), # go down to put it
        OPEN_GRIPPER,
        CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428)), DEFAULT_ORIENT, tool_name = 'ggrip')), # finish stage 4
    ] 
    execute_commands(PUT_KERN_ON_SCALE)

def stage_5_make_photo(cell: Cell, qr_detector: QRDetector):
    print("Stage 5")
    img_front = qr_detector.get_bgr_image()
    TO_UNDER = CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, -0.475, 0.49428)), DEFAULT_ORIENT, tool_name = 'ggrip')) # before front photo
    TO_TOREC = CartPTPCommand(line, MotionCartPose.from_array(np.array((0.75188, 0.0, 0.49428)), PHOTO_ORIENT, tool_name = 'ggrip')) # before left photo
    execute_commands([TO_UNDER,])
    img_front = qr_detector.get_bgr_image()
    execute_commands([TO_TOREC,])
    img_left = qr_detector.get_bgr_image()
    execute_commands([TO_UNDER,])
    cell.save_front_photo(img_front)
    cell.save_left_photo(img_left)
    # cell.save_mass()
    cell.save_id(KERN_ID)
    cell.save_in_db()

def stage_6_get_container_from_scale(stage_3_pattern: list):
    print("Stage 6")
    MOVE_CONTAINER_WITH_KERN = copy.copy(stage_3_pattern.reverse())
    execute_commands(MOVE_CONTAINER_WITH_KERN)

def stage_7_put_container_in_stelazh(stage_2_pattern: list):
    print("Stage 7")
    PUT_CONTAINER_IN_STELAZH = copy.copy(stage_2_pattern.reverse())
    execute_commands(PUT_CONTAINER_IN_STELAZH)

def main():
    cell = Cell('hackaton.db', 'COM4', calibrate_points = CALIBRATE_STELAZH)
    qr_detector = QRDetector()
    index = cell.get_index(KERN_ID)
    print("Container index", index)
    container_pose = cell.stelazh[index[0], index[1]]

    print("Container pose", container_pose)
    # stage_1_move_to_qr()
    
    stage_2_pattern = stage_2_get_container_from_stelazh(container_pose)
    stage_3_pattern = stage_3_put_container_on_scale()
    stage_4_put_kern_on_scale()
    stage_5_make_photo(cell, qr_detector)
    stage_6_get_container_from_scale(stage_3_pattern)
    stage_7_put_container_in_stelazh(stage_2_pattern)


if __name__ == "__main__":
    main()