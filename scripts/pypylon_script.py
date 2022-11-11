import cv2
from pypylon import pylon
from detect import qrDetect

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        frame = image.GetArray()

        detecter = qrDetect(frame)
            
        if detecter.isDetect:
            for i in range(detecter.N):
                det = detecter[i]
                frame = cv2.circle(frame, det.center,radius=2,color = (100,200,75), thickness = 10)
                out_frame = cv2.polylines(frame,det.poligon,True, (255,255,255),4)
                print("Core id: ",det.info)
        else:
            out_frame = frame

        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', frame)

    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()