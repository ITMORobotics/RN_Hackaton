import os
import sys
import time
import cv2
import numpy as np
from PIL import Image

from rn_hackaton.stend.lab import Stend
from rn_hackaton.robot.robot_ctrl import Command, MotionCartPose, LinePTPCommand, GripperCommand

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

SIMPLE_COMMAND = LinePTPCommand(MotionCartPose.from_array(np.array((0.9, 0.3, 0.6))))
SIMPLE_COMMAND2 = LinePTPCommand(MotionCartPose.from_array(np.array((0.9, 0.3, 0.5))))
SIMPLE_COMMAND3 = GripperCommand("grab", True)

def execute_command(self, cmd: Command):
    cmd.execute()

def main():
    # stend = Stend('tests/hackaton.db', POSITION_MAP)
    



if __name__ == "__main__":
    main()