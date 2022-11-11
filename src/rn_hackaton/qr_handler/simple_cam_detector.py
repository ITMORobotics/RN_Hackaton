import cv2
from .qr_detector import QRDetector
from PIL import Image

class SimpleQRDetector(QRDetector):
    def __init__(self):
        self.__camera = cv2.VideoCapture(0)
        QRDetector.__init__(self)
    
    def init(self) -> bool:
        return True 
    
    def camera_ok(self) -> bool:
        return not self.__camera is None
    
    def get_bgr_image(self) -> Image:
        ret, frame = self.__camera.read()
        if ret:
            return Image.fromarray(frame)

    def __del__(self): 
        self.__camera.release()