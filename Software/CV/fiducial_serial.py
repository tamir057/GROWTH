#!/usr/bin/python3
# pi side 

import cv2
from picamera2 import Picamera2

import time
import serial
import threading
def receive_data(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            print(line.decode('utf-8').rstrip())
ser = serial.Serial('/dev/ttyACM0', 115200)
receive_thread = threading.Thread(target=receive_data, args=(ser,))
receive_thread.daemon = True
receive_thread.start()
    


# Grab images as numpy arrays and leave everything else to OpenCV.

#face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}, controls={"FrameDurationLimits": (50000, 50000)}))
picam2.start()

while True:
	im = picam2.capture_array()
	#im = imutils.resize(im, width=1000)
	im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
	(corners, ids, rejected) = arucoDetector.detectMarkers(im)

	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()
		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# draw the bounding box of the ArUCo detection
			cv2.line(im, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(im, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(im, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(im, bottomLeft, topLeft, (0, 255, 0), 2)
			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(im, (cX, cY), 4, (0, 0, 255), -1) 
			if (cX > 157 and cX < 163):
				cv2.imshow("Middle Frame", im)
				message = "Toggle"
				ser.write(message.encode('utf-8')+ b'\n')
				time.sleep(0.1)
 			# draw the ArUco marker ID on the frame
		cv2.putText(im, str(markerID),(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
	# show the output frame
	cv2.imshow("Frame", im)
	key = cv2.waitKey(1) & 0xFF
    	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# do a bit of cleanup
cv2.destroyAllWindows()

