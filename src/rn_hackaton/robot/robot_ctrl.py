import math
import numpy as np

class MotionCartPose:
    def __init__(self):
        self.__cart_point = None
        self.__cart_orient = None
        self.__is_initialized = False
    
    def to_robot_type(self):
        assert self.__is_initialized, "Pose is not initialized"
        new_cart_pose = get_cartesian_position()
        new_cart_pose.x = self.__cart_point[0]*1e3
        new_cart_pose.y = self.__cart_point[1]*1e3
        new_cart_pose.z = self.__cart_point[2]*1e3

        cp_orient = new_cart_pose.get_rotation()
        if not self.__cart_orient is None:
            deg_orient = np.degrees(self.__cart_orient)
            cp_orient.x = deg_orient[0]
            cp_orient.y = deg_orient[1]
            cp_orient.z = deg_orient[2]
        
        new_cart_pose.set_rotation(cp_orient)

        return new_cart_pose
    
    @staticmethod
    def from_robot_type(robot_pose):
        new_motion_cart_pose = MotionCartPose()
        new_motion_cart_pose.cart_point = np.array(
            (robot_pose.x, robot_pose.y, robot_pose.z)
        )*1e-3
        robot_orient = robot_pose.get_rotation()
        new_motion_cart_pose.cart_orient = np.radians(
            np.array((robot_orient.x, robot_orient.y, robot_orient.z))
        )
        return new_motion_cart_pose
    
    @staticmethod
    def from_array(robot_pose: np.ndarray, robot_orient: np.ndarray = None):
        new_motion_cart_pose = MotionCartPose()
        new_motion_cart_pose.cart_point = robot_pose
        new_motion_cart_pose.cart_orient = robot_orient
        return new_motion_cart_pose

    @property
    def cart_point(self):
        return self.__cart_point
    
    @property
    def cart_orient(self):
        return self.__cart_orient

    @cart_point.setter
    def cart_point(self, cart_point: np.array):
        self.__cart_point = cart_point
        self.__is_initialized = True
    
    @cart_orient.setter
    def cart_orient(self, cart_oriet: np.array):
        self.__cart_orient = cart_oriet
    

class RobotControl:
    def __init__(self, gripper_port: str):
        self.__gripper_port = gripper_port
    
    def toogle_gripper(self, signal = False):
        set_do(self.__gripper_port, signal)
    
    @property
    def pose(self):
        return MotionCartPose.from_robot_type(get_cartesian_position())