import os
import sys
import unittest
import numpy as np
from PIL import Image
from rn_hackaton.db_control.rw_control_database import KernDBControl

# 7681 - id for kern 1
KERN_1 = 7681
# 7697 - id for kern 2
KERN_2 = 7697

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class testUtils(unittest.TestCase):
    def setUp(self):
        self.__db_ctrl = KernDBControl('tests/hackaton.db')

    def test_read_kern_table_by_id(self):
        data = self.__db_ctrl.read_kern_table_by_id(KERN_1)
        self.assertIsNotNone(data)
        print(data)

    def test_insert_analize_data(self):
        image_1 = Image.open('tests/kern.png')
        ok = self.__db_ctrl.insert_analyze_data(KERN_1, 0.55, image_1, image_1)
        self.assertTrue(ok)
        check_data = self.__db_ctrl.read_last_analize_data(KERN_1)
        self.assertIsNotNone(check_data)
        print(check_data)

        res_imgref = np.asarray(image_1)
        res_img_test = np.asarray(check_data[2])
        # Calculate the absolute difference on each channel separately
        diff = np.sum(np.fabs(np.subtract(res_imgref[:, :], res_img_test[:, :])))
        self.assertAlmostEqual(diff, 0.0)

    
def main():
    unittest.main(exit=False)

if __name__ == "__main__":
    main()