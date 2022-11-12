import copy
import numpy as np
import time
from rn_hackaton.robot.robot_ctrl import MotionCartPose
from rn_hackaton.db_control.rw_control_database import KernDBControl


from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

class Stend:
    def __init__(self,  db_path: str, positions_map = {}):
        self.__db_ctrl = KernDBControl(db_path)
        self.__positions_map = positions_map

    def get_pose(self, name: str) -> MotionCartPose:
        return self.__positions_map[name]
    
    def set_pose(self, name: str, position: MotionCartPose):
        self.__positions_map[name] = position

    @property
    def mass(self) -> float:
        mass = 0
        return mass

    @property
    def kern_plate_state(self) -> tuple:
        kern_plate_state = (False, False)
        return kern_plate_state
    
    @property
    def busy_kern_index(self) -> int:
        if True in self.kern_plate_state:
            return self.kern_plate_state.index(True)
        return None

    @property
    def positions_map(self):
        return self.__positions_map
