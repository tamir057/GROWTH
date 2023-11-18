

 
# import the opencv library 
#import cv2 
# from picamera.array import PiRGBArray
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview
#from picamera2.array import Pitgbarray2
import time 
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280,720)}, lores = {"size": (640,480)}, display="lores")
picam2.configure(video_config)
encoder=H264Encoder(bitrate=100000000)
output="test.h264"
picam2.start_preview(Preview.QTGL)
picam2.start_recording(encoder, output)
time.sleep(10)
picam2.stop_recording()
picam2.stop_preview()

  

