import re
import time
import serial
import threading

class SerialReader:
    def __init__(self):
        self.IRS = [None, None]
        self.irs_time_update = [-1, -1]
        self.scale = None
        self.scale_time_update = -1
        self._thread_alive = True
        self.update_thread = threading.Thread(target=self.update)
    
    def start_thread(self):
        self._thread_alive = True
        self.update_thread.start()

    def stop_thread(self):
        self._thread_alive = False
        self.update_thread.join()

    def update(self):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            while self._thread_alive:
                line = ser.readline().decode('UTF-8')
                if line != "":
                    if line[0] == 's':
                        self.scale = float(re.compile(r'-?\d+.\d+').findall(line)[0])
                        self.scale_time_update = time.time()
                    if line[0] == 'i':
                        idx = int(line[1])
                        self.IRS[idx] = int(line[2:])
                        self.irs_time_update[idx] = time.time()



        

def main():
    ser = SerialReader()
    try:
        ser.start_thread()
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