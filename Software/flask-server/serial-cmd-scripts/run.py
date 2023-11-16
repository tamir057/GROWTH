#!/usr/bin/python3
# pi side 

import cv2
from picamera2 import Picamera2

import time
import serial
import threading

import sys

steps_array = sys.argv[1:]

received_message = ""
sensor_values = {
    'pH' : 0,
    'temperature' : 0,
    'ec' : 0
}



def receive_data(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            received_message = line.decode('utf-8').rstrip()
            print(received_message)
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

# TODO: determine value
lower_sensor_steps = 0; 
def fiducial_detection():
    
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
                # TODO: message syntax 
                message = "STOP_MOTOR:0"
                ser.write(message.encode('utf-8')+ b'\n')
                message = "READ_STEPS:0,0"
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

def check_fiducial():
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
            current_offset = 160 - cX
            if (current_offset > -3 or current_offset < 3):
                return -1, markerID # centered
            else if (current_offset > 3):
                return 0, markerID # move to the left
            else:
                return 1, markerID # move to the right 
# TODO: Fill in temp message
def run(steps_array):

    plot_readings= {key: {} for key in steps_array}

        message = "MOVE_MOTOR_CONT:1,0"  # send up first 
        message = "MOVE_MOTOR_CONT:0,1"
        ser.write(message.encode('utf-8')+ b'\n')
     for (key in steps_array):
        #TODO: Use get current position cmd after defined 
        message = "GET_CURRENT_POSITION:0,0"
        ser.write(message.encode('utf-8')+ b'\n')
        current_position = received_message
        message = "MOVE_MOTOR_STEPS:0,0," + (steps_array[key] - current_position)
        ser.write(message.encode('utf-8')+ b'\n')

        error_direction, fiducial_key = check_fiducial()
        if (error_direction > 0):
            message = "MOVE_MOTOR_CONT:0," + error_detection 
            ser.write(message.encode('utf-8')+ b'\n')
            fiducial_detection()
        
        # TODO: sensor vals from cheatsheet
        message = "MOVE_MOTOR_STEPS:1,1," + lower_sensor_steps
        ser.write(message.encode('utf-8')+ b'\n')
        message = "READ_SENSOR:0"
        ser.write(message.encode('utf-8')+ b'\n')
        sensor_values['pH'] = receive_message
        message = "READ_SENSOR:1"
        ser.write(message.encode('utf-8')+ b'\n')
        sensor_values['temperature'] = receive_message
        message = "READ_SENSOR:2"
        ser.write(message.encode('utf-8')+ b'\n')
        sensor_values['ec'] = receive_message
        message = "MOVE_MOTOR_STEPS:1,0," + lower_sensor_steps
        ser.write(message.encode('utf-8')+ b'\n')
        plot_readings[key] = sensor_values
    return plot_readings 
        

# do a bit of cleanup
cv2.destroyAllWindows()
