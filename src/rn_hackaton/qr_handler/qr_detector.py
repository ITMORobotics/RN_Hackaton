import copy
import numpy as np
import time


from .detect import qrDetect
from threading import Thread

from PIL import Image
from abc import abstractmethod, ABC

DETECTOR_PERIOD = 0.05

class QRDetector(Thread, ABC):
    def __init__(self):
        Thread.__init__(self)

        self.__last_detector = None

        self.init()
        self.daemon = True
        self.start()
    
    @abstractmethod
    def init(self)-> bool:
        pass

    @abstractmethod
    def get_bgr_image() -> Image:
        pass
    
    @abstractmethod
    def camera_ok() -> bool:
        pass

    @property
    def detector(self):
        return self.__last_detector
    
    def run(self):
        while self.camera_ok():
            pil_image = self.get_bgr_image()
            if not pil_image is None:
                image = np.asarray(pil_image)
                detecter = qrDetect(image)
                self.__last_detector = copy.deepcopy(detecter)
                time.sleep(DETECTOR_PERIOD)
            else:
                return False
        return True

    def wait_detect(self):
        if self.__last_detector.isDetect:
            return copy.deepcopy(self.__last_detector)

    def __del__(self):
        pass
