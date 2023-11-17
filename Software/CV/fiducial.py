#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

#face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}, controls={"FrameDurationLimits": (50000, 50000)}))
#picam2.configure(picam2.create_preview_configuration(main={"size": (960,540)}, lores = {"size": (640,480), "format": 'YUV420'}, display="lores"))
#picam2.configure(picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution},controls={"FrameDurationLimits": (40000, 40000)}))

#picam2.configure(picam2.create_video_configuration(main={"size": (1280,720)}, lores = {"size": (640,480)}, display="lores"))
picam2.start()

while True:
	im = picam2.capture_array()
	#im = imutils.resize(im, width=1000)
	im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
	#height, width = im.shape[:2]
	#print(height) 
	#print(width)
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
				print("In the middle")
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
#vs.stop()


    

 #   cv2.imshow("Camera", grey)
  #  cv2.waitKey(1)

