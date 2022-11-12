import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.stend.lab import Stend
from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, GripperCommand


class LinePTPCommand(Command):
    def __init__(self, func_pointer, cart_position: MotionCartPose, speed = 100.0, accel = 1000.0, smooth = 0.0):
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
# POSITION_MAP = {
#     'before_kern_0': (np.array((0.9, 0.3, 0.6)), ALONG_Z_ORIENT, "GCam", ptp),
#     'kern_0': (np.array((0.9, 0.3, 0.5)), ALONG_Z_ORIENT, "GCam"),
#     'before_kern_1': (np.array((0.9, 0.4, 0.6)), ALONG_Z_ORIENT, "GGripper"),
#     'kern_1': (np.array((0.9, 0.4, 0.5)), ALONG_Z_ORIENT, "GCam"),

#     'before_take_kern_on_stend': (np.array((0.9, 0.0, 0.6)), ALONG_Z_ORIENT, "GGripper"),
#     'take_kern_on_stend': (np.array((0.9, 0.0, 0.5)), ALONG_Z_ORIENT, "GGripper"),
#     'after_take_kern_on_stend': (np.array((0.9, 0.0, 0.6)), ALONG_Z_ORIENT, "GGripper"),

#     'take_box_0': (np.array((0.9, 0.1, 0.6)), ALONG_Z_ORIENT, "GKruk"),
#     'take_box_1': (np.array((0.9, 0.1, 0.5)), ALONG_Z_ORIENT, "GKruk"),
#     'take_box_1': (np.array((0.9, 0.05, 0.5)), ALONG_Z_ORIENT, "GKruk"),


# }

SIMPLE_COMMAND0 = GripperCommand("grab", False)
SIMPLE_COMMAND1 = LinePTPCommand(line, MotionCartPose.from_array(np.array((0.9, 0.3, 0.6))))
SIMPLE_COMMAND2 = LinePTPCommand(line, MotionCartPose.from_array(np.array((0.9, 0.3, 0.5))))
SIMPLE_COMMAND3 = GripperCommand("grab", True)
SIMPLE_COMMAND4 = LinePTPCommand(line, MotionCartPose.from_array(np.array((0.9, 0.3, 0.6))))

def execute_commands(cmd_list: list):
    for c in cmd_list:
        c.execute()

def main():
    # stend = Stend('tests/hackaton.db', POSITION_MAP)
    execute_commands([SIMPLE_COMMAND0, SIMPLE_COMMAND1, SIMPLE_COMMAND2, SIMPLE_COMMAND3, SIMPLE_COMMAND4])



if __name__ == "__main__":
    main()