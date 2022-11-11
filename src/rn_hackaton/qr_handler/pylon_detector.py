from pypylon import pylon
from qr_detector import QRDetector
from PIL import Image

class PylonQRDetector(QRDetector):
    def __init__(self):
        self.__camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.__converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.__converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.__converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.__last_detecter = None
        QRDetector.__init__(self)
    
    def init(self) -> bool:
        self.__camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        return True 
    
    def camera_ok(self) -> bool:
        return self.__camera.IsGrabbing()
    
    def get_bgr_image(self) -> Image:
        grabResult = self.__camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = self.__converter.Convert(grabResult)
            frame = image.GetArray()
        grabResult.Release()
        return Image.fromarray(frame)

    def __del__(self): 
        self.__camera.StopGrabbing()
