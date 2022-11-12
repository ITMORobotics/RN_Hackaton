import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, GripperCommand

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


MOVE_CONTAINER_LIST = [
    GripperCommand("grab", False),
    CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.65)), np.array((np.pi, 0.0, 0.0)))), # under catch container
    CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.55)))), # step1 container left up
    CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.55)))), # step2_container left down
    CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.55)))), # step2_container in down
    CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.65))))
]

def execute_commands(cmd_list: list):
    for c in cmd_list:
        c.execute()

def main():
    execute_commands(MOVE_CONTAINER_LIST)


if __name__ == "__main__":
    main()