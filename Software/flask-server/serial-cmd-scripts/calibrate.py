#!/usr/bin/python3
# pi side 

import cv2
from picamera2 import Picamera2

import time
import serial
import threading
import sys

received_message = ["::"]
boundary_offset = 4000
current_position = 0
data = { 
    "1": 0,
    "2" : 0,
    "3" : 0
}

# total_fiducials = sys.argv[1:]
total_fiducials = 3

def receive_data(ser):
    #global received_message
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            received_message[0] = line.decode('utf-8').rstrip()
            print(f"full received message {received_message[0]}", "  from received")
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

fiducials_detected = 0

def fiducial_detection():
    #im = picam2.capture_array()
    #im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
    #cv2.imshow("image", im)
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
                if (cX > 157 and cX < 163) :
                    #cv2.imshow("Middle Frame", im)
                    print("found a fiducial")
                    time.sleep(0.1)
                    return 
                # draw the ArUco marker ID on the frame
            cv2.putText(im, str(markerID),(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        # show the output frame
        #cv2.imshow("Frame", im)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

# helper to wait for acks 
def wait_for_ack(message):
    
    #global received_message
    #if (received_message != "")
    #parsed_message = received_message.split(":")[1]
    parsed_message = "::"
    print(received_message[0], " from beginning of wait")
    #print(parsed_message)
    while (parsed_message != message):
        #global received_message 
        parsed_message = received_message[0].split(":")[1]
        pass
    #print(received_message[0])
    print(parsed_message, "from ack") 


def send_serial(command):
    #global receieved_message
    received_message[0] = "::"
    ser.write(command.encode('utf-8')+ b'\n') 

#TODO: CREATE HELPER FOR ACKS !!! 
def calibrate():
    fiducials_detected = 0
    #global received_message
    message = "MOVE_MOTOR_CONT:1,0"  # send up first 
    send_serial(message)
    #ser.write(message.encode('utf-8')+ b'\n')
    wait_for_ack("LIMIT_SWITCH_TRIGGERED") #ack mssg that at limit switch
    if received_message[0].split(":")[2] != 'UP':
        print(f"this is the direction {received_message[0].split(':')[2]}")
        raise ValueError("wrong direction!!!!!!! should be up")
    print("up completed")
    #received_message = "::"
    # TODO: set state of z motor as 'up' -- store locally? 
    message = "MOVE_MOTOR_CONT:0,1" # send to right  
    send_serial(message)
    #ser.write(message.encode('utf-8')+ b'\n')
    wait_for_ack("LIMIT_SWITCH_TRIGGERED")
    if received_message[0].split(":")[2] != 'RIGHT':
        raise ValueError("wrong direction!!!!!!! should be right")
    # TODO: set state of z motor as 'up' -- store locally? 
    message = f"MOVE_MOTOR_STEPS:0,0,{boundary_offset}" # TODO: verify string formatting
    send_serial(message)
    #ser.write(message.encode('utf-8')+ b'\n')
    wait_for_ack("MOVE_MOTOR_STEPS")
    #if received_message[0].split(":")[2] != 'LEFT':
    #    raise ValueError("wrong direction!!!!!!! should be left")
    message = "SET_ZERO_POS:0" 
    send_serial(message)
    #ser.write(message.encode('utf-8')+ b'\n')
    wait_for_ack("SET_ZERO_POS")
    
    while (received_message[0] != "LIMIT_SWITCH_TRIGGERED"): 
        message = "MOVE_MOTOR_CONT:0,0"
        send_serial(message)
        #ser.write(message.encode('utf-8')+ b'\n')
        fiducial_detection()
        message = "STOP_MOTOR:0"
        send_serial(message)
        #ser.write(message.encode('utf-8')+ b'\n')
        wait_for_ack("STOP_MOTOR")  #ack mssg that it moved the stopped the motor
        send_serial(message)
        wait_for_ack("STOP_MOTOR")
        message = "RETURN_POS:0"
        time.sleep(0.5)
        send_serial(message)
        #ser.write(message.encode('utf-8')+ b'\n')
        # while received message split[0]!= CURRENT_POS
        wait_for_ack("RETURN_POS")
        #while (received_message[0].split(":")[1]!= 'RETURN__POS'): # TODO: ack mssg that it moved the offset val 
        #    pass 
        current_position = received_message[0].split(":")[2]
        fiducials_detected += 1
        data[f"{fiducials_detected}"] = current_position
        time.sleep(1)

    message = f"MOVE_MOTOR_STEPS:0,0,{boundary_offset}"   # moving to left 
    send_serial(message)
    wait_for_ack("MOVE_MOTOR_STEPS")
    #ser.write(message.encode('utf-8')+ b'\n')
    # request current position and store that as outer boundary 
    # create helper for returning current position
    message = "STOP_MOTOR:0"
    send_serial(message)
    wait_for_ack("STOP_MOTOR")

    message = "RETURN_POS:0"
    send_serial(message)
    #ser.write(message.encode('utf-8')+ b'\n')
    # while received message split[0]!= CURRENT_POS
    wait_for_ack("RETURN_POS")
    #while (received_message[0].split(":")[1]!= 'RETURN_POS'): # TODO: ack mssg that it moved the offset val 
    #    pass 
    current_position = received_message.split(":")[1]
    print(data)
    
        
# if __name__ == "__main__":
calibrate() 
if fiducials_detected < total_fiducials:
    fiducials_detected = 0
    calibrate()

if fiducials_detected == total_fiducials:
    print("All fiducials found!")
else:
    raise ValueError("Failed to final all fiducials") 

# do a bit of cleanup
cv2.destroyAllWindows()
