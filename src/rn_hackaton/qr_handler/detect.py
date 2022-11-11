import cv2
import numpy as np
from pyzbar.pyzbar import decode

class qrDetect:
    def __init__(self, frame = None):
        self.center = []
        self.info = []
        self.isDetect = False
        self.poligon = []
        self.N = 0

        if not frame is None:
            self.detection(frame)

    def __getitem__(self,idx):
        out = qrDetect()
        out.center = self.center[idx]
        out.info = self.info[idx]
        out.poligon = self.poligon[idx]
        out.N = 1
        out.isDetect = True
        return out

    def detection(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detect_result = self.qr_detect(gray_frame)
        self.N = len(detect_result)

        if self.N > 0:
            self.isDetect = True
            for dec in detect_result:
                    self.center.append(
                        (   
                            int(dec.rect.left + dec.rect.width/2),
                            int(dec.rect.top + dec.rect.height/2)
                        )
                    )
                    self.info.append(dec.data.decode('UTF-8'))
                    self.poligon.append(np.array([dec.polygon],np.int32))
        pass

    def qr_detect(self, frame):
        result = decode(frame)
        return result
    