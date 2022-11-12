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

ALONG_Z_ORIENT = np.array((0.0, -np.pi/2, -np.pi))
MAX_SPEED = 100

SIMPLE_COMMAND0 = GripperCommand("grab", False)
SIMPLE_COMMAND1 = CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.65)), np.array((np.pi, 0.0, 0.0))))
SIMPLE_COMMAND2 = CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.55))))
SIMPLE_COMMAND3 = GripperCommand("grab", True)
SIMPLE_COMMAND4 = CartPTPCommand(line, MotionCartPose.from_array(np.array((0.7, -0.14, 0.65))))

def execute_commands(cmd_list: list):
    for c in cmd_list:
        c.execute()

def main():
    execute_commands([SIMPLE_COMMAND0, SIMPLE_COMMAND1, SIMPLE_COMMAND2, SIMPLE_COMMAND3, SIMPLE_COMMAND4])


if __name__ == "__main__":
    main()