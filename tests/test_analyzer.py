import re
import time
from rn_hackaton.stend.analyzer import SerialReader

def main():
    ser = SerialReader('COM4')
    try:
        time.sleep(1)
        while True:
            print('-'*50)
            print('time:  ', ser.scale_time_update)
            print("scale: ", ser.scale)
            print("ir   : ", ser.IRS)
            time.sleep(0.1)
    except KeyboardInterrupt:
        ser.stop_thread()


if __name__=="__main__":
    main()