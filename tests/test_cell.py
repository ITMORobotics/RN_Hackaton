import time
from rn_hackaton.cell.lab import Cell
from rn_hackaton.qr_handler.simple_cam_detector import SimpleQRDetector as QRDetector
# from rn_hackaton.qr_handler.pylon_detector import PylonQRDetector as QRDetector

def main():
    cell = Cell('tests/hackaton.db', 'COM4')
    qr_detector = QRDetector()
    cell.save_id(5555)
    cell.save_mass()
    cell.save_left_photo(qr_detector.get_bgr_image())
    cell.save_front_photo(qr_detector.get_bgr_image())
    cell.save_in_db()
if __name__ == "__main__":
    main()