import numpy as np

class stelazh:
    def __init__(self):
        self.row_num = 3
        self.col_num = 3
        self.addr = np.array([  [[0,0,0],[1,0,0],[2,0,0]],
                                [[0,0,-1],[1,0,-1],[2,0,-1]],
                                [[0,0,-2],[1,0,-2],[2,0,-2]]])
        self.KK = np.diag([86,0,110])
        self.left_up_point = np.array([0]*3)
        self.kx = 1
        self.ky = 1
        self.kz = 1
        self.phi = -0.1


    def __getitem__(self,idx):
        cth = np.cos(self.phi)
        sth = np.sin(self.phi)
        R = np.array([[cth, -sth,0],[sth,cth,0],[0,0,1]])
        if not type(idx) is tuple:
            temp = []
            for i in range(3):
                temp.append(R@self.KK@self.addr[idx][i])
            return self.left_up_point + np.array(temp)
        else:
            return self.left_up_point + R@self.KK@self.addr[idx]

    def calibrate(self,point_left_up, point_rigth_up):
        temp = point_left_up - point_rigth_up
        self.phi = np.atan2(temp[0],temp[1])
        

def main():
    st = stelazh()
    print(st[2][1])

if __name__=="__main__":
    main()