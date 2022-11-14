import re
import time
import serial
import threading

class SerialReader:
    def __init__(self, serial_port: str):
        self.__serial_port = serial_port
        self.IRS = [None, None]
        self.irs_time_update = [-1, -1]
        self.scale = None
        self.scale_time_update = -1
        self._thread_alive = True
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.setDaemon(True)
        self.start_thread()
        # Should sleep
        time.sleep(9.0)

    
    def get_IRS(self, index = None):
        if index is None:
            return self.IRS
        return self.IRS[index]

    def get_scale(self):
        if self.scale is None:
            return 52.01
        return self.scale  

    def start_thread(self):
        self._thread_alive = True
        self.update_thread.start()

    def stop_thread(self):
        self._thread_alive = False
        self.update_thread.join()

    def update(self):
        with serial.Serial(self.__serial_port, 9600, timeout=1) as ser:
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


