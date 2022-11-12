import time
import os
import numpy as np
from rn_hackaton.cell.lab import Cell
from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector
KERN_ID = 7681
CALIBRATE_STELAZH = (
    np.array((0.66653, 0.20485, 0.5456)),
    np.array((0.89301, 0.19039, 0.54397))
)
def main():
    cell = Cell('hackt.db', 'COM4', calibrate_points = CALIBRATE_STELAZH)
    qr_detector = QRDetector()
    cell.save_id(5555)
    cell.save_mass()
    cell.save_left_photo(qr_detector.get_bgr_image())
    cell.save_front_photo(qr_detector.get_bgr_image())
    cell.save_in_db()
    notify(KERN_ID)
    
    print(cell.get_index(KERN_ID))
if __name__ == "__main__":
    main()