
import cv2

from detect import qrDetect

def main():
    cap = cv2.VideoCapture(-1)
    ## Max resolution 1280x720
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # 800
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # 600
    if not cap.isOpened():
        exit("Unable to open camera")
    while True:
        ret, frame = cap.read()
        if ret:
            detecter = qrDetect(frame)
            
            if detecter.isDetect:
                for i in range(detecter.N):
                    det = detecter[i]
                    frame = cv2.circle(frame, det.center,radius=2,color = (100,200,75), thickness = 10)
                    out_frame = cv2.polylines(frame,det.poligon,True, (255,255,255),4)
                    print("Core id: ",det.info)
            else:
                out_frame = frame
            
        cv2.imshow('Example', out_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=="__main__":
    main()