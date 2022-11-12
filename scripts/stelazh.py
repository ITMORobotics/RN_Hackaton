import numpy as np

class stelazh:
    def __init__(self):
        self.row_num = 3
        self.col_num = 3
        self.addr = np.array([  [[0,0,0],[1,0,0],[2,0,0]],
                                [[0,0,-1],[1,0,-1],[2,0,-1]],
                                [[0,0,-2],[1,0,-2],[2,0,-2]]])
        self.KK = np.diag([110,0,86])
        self.left_up_point = np.array([0]*3)
        self.kx = 1
        self.ky = 1
        self.kz = 1
        self.phi = 0


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
        temp = point_rigth_up - point_left_up
        self.phi = np.arctan2(temp[1],temp[0])
        self.left_up_point = point_left_up
        

def main():
    st = stelazh()
    st.calibrate(np.array([666.53,204.85,543.56]),np.array([893.01,190.39,543.97]))
    print(st[0][0])
    print(st[0][1])
    print(st[1][0])

if __name__=="__main__":
    main()