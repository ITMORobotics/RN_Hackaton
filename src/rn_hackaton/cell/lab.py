import copy
import numpy as np
import time
from PIL import Image
from rn_hackaton.db_control.rw_control_database import KernDBControl
from rn_hackaton.stend.analyzer import SerialReader

import numpy as np

class Stelazh:
    def __init__(self):
        self.row_num = 3
        self.col_num = 3
        self.addr = np.array([  [[0,0,0],[1,0,0],[2,0,0]],
                                [[0,0,-1],[1,0,-1],[2,0,-1]],
                                [[0,0,-2],[1,0,-2],[2,0,-2]]])
        self.KK = np.diag([86,0,110])
        self.left_up_point = np.array([0]*3)
        self.kx = 1
        self.ky = 1
        self.kz = 1
        self.phi = -0.1


    def __getitem__(self,idx):
        cth = np.cos(self.phi)
        sth = np.sin(self.phi)
        R = np.array([[cth, -sth,0],[sth,cth,0],[0,0,1]])
        if not type(idx) is tuple:
            temp = []
            for i in range(3):
                temp.append(R@self.KK@self.addr[idx][i])
            return self.left_up_point + np.array(temp)
        else:
            return self.left_up_point + R@self.KK@self.addr[idx]

    def calibrate(self,point_left_up: np.ndarray, point_rigth_up: np.ndarray):
        temp = point_left_up - point_rigth_up
        self.phi = np.atan2(temp[0],temp[1])


class Cell:
    def __init__(self,  db_path: str, serial_port: str, calibrate_points: list):
        self.__db_ctrl = KernDBControl(db_path)
        self.__serial = SerialReader(serial_port)
        self.__stelazh = Stelazh()
        self.__stelazh.calibrate(calibrate_points)
        self.__data_row = [7681, -1, 0, 0]
    
    def save_id(self, id: int):
        self.__data_row[0] = id
    
    def save_mass(self):
        print(self.mass)
        self.__data_row[1] = self.mass
    
    def save_front_photo(self, front_photo: Image):
        self.__data_row[2] = front_photo

    def save_left_photo(self, left_photo: Image):
        self.__data_row[3] = left_photo

    def save_in_db(self):
        self.__db_ctrl.insert_analyze_data(*self.__data_row)

    @property
    def stelazh(self) -> Stelazh:
        return self.__stelazh

    @property
    def mass(self) -> float:
        mass = self.__serial.get_scale()
        return mass

    @property
    def kern_plate_state(self) -> tuple:
        kern_plate_state = self.__serial.get_IRS()
        return kern_plate_state
    
    @property
    def busy_kern_index(self) -> int:
        if 1 in self.kern_plate_state:
            return self.kern_plate_state.index(1)
        return None
