 
# import the opencv library 
import cv2 
# from picamera.array import PiRGBArray
from picamera import PiCamera
import time  
  
camera = PiCamera()
# define a video capture object 
#vid = cv2.VideoCapture('test_vid.mp4') 
vid = cv2.VideoCapture(0) 

if not(vid.isOpened()):
	print("Could not open video device")
while(vid.isOpened()): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    if ret:   
    # Display the resulting frame 
        cv2.imshow('frame', frame)  
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
    else: 
        break
       
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
