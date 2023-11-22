# #!/usr/bin/python3
# # pi side 

# import cv2
# from picamera2 import Picamera2

# import time
# import serial
# import threading
import sys

# received_message = ["::"]
# boundary_offset = 4000
# current_position = 0
# data = {
#     'vertical-motor': 0, 
#     'horizontal-boundary': 0,
#     'steps_array': { 
#         "1": 0,
#         "2" : 0,
#         "3" : 0
#     }
# }

# # total_fiducials = sys.argv[1:]
# total_fiducials = 3

# total_fiducials = sys.argv[1:]

# def receive_data(ser):
#     #global received_message
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline()
#             received_message[0] = line.decode('utf-8').rstrip()
#             print(f"full received message {received_message[0]}", "  from received")
# ser = serial.Serial('/dev/ttyACM0', 115200)
# receive_thread = threading.Thread(target=receive_data, args=(ser,))
# receive_thread.daemon = True
# receive_thread.start()
    


# # Grab images as numpy arrays and leave everything else to OpenCV.

# #face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
# cv2.startWindowThread()

# arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# arucoParams = cv2.aruco.DetectorParameters()
# arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}, controls={"FrameDurationLimits": (50000, 50000)}))
# picam2.start()

# def fiducial_detection():
#     while received_message[0].split(":")[1] != "LIMIT_SWITCH_TRIGGERED":
#         im = picam2.capture_array()
#         #im = imutils.resize(im, width=1000)
#         im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
#         (corners, ids, rejected) = arucoDetector.detectMarkers(im)

#         if len(corners) > 0:
#             # flatten the ArUco IDs list
#             ids = ids.flatten()
#             # loop over the detected ArUCo corners
#             for (markerCorner, markerID) in zip(corners, ids):
#                 # extract the marker corners (which are always returned
#                 # in top-left, top-right, bottom-right, and bottom-left
#                 # order)
#                 corners = markerCorner.reshape((4, 2))
#                 (topLeft, topRight, bottomRight, bottomLeft) = corners
#                 # convert each of the (x, y)-coordinate pairs to integers
#                 topRight = (int(topRight[0]), int(topRight[1]))
#                 bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
#                 bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
#                 topLeft = (int(topLeft[0]), int(topLeft[1]))

#                 # draw the bounding box of the ArUCo detection
#                 cv2.line(im, topLeft, topRight, (0, 255, 0), 2)
#                 cv2.line(im, topRight, bottomRight, (0, 255, 0), 2)
#                 cv2.line(im, bottomRight, bottomLeft, (0, 255, 0), 2)
#                 cv2.line(im, bottomLeft, topLeft, (0, 255, 0), 2)
#                 # compute and draw the center (x, y)-coordinates of the
#                 # ArUco marker
#                 cX = int((topLeft[0] + bottomRight[0]) / 2.0)
#                 cY = int((topLeft[1] + bottomRight[1]) / 2.0)
#                 cv2.circle(im, (cX, cY), 4, (0, 0, 255), -1) 
#                 if (cX > 157 and cX < 163) :
#                     #cv2.imshow("Middle Frame", im)
#                     print("found a fiducial")
#                     time.sleep(0.1)
#                     return 0
#                 # draw the ArUco marker ID on the frame
#             cv2.putText(im, str(markerID),(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
#         # show the output frame
#         #cv2.imshow("Frame", im)
#         # key = cv2.waitKey(1) & 0xFF
#         # if key == ord('q'):
#         #     break

#     return 1

# # helper to wait for acks 
# def wait_for_ack(message):
    
#     parsed_message = "::"
#     print(received_message[0], " from beginning of wait")

#     while (parsed_message != message):
#         parsed_message = received_message[0].split(":")[1]
#         pass
#     print(parsed_message, "from ack") 


# def send_serial(command):
#     received_message[0] = "::"
#     ser.write(command.encode('utf-8')+ b'\n') 

# #TODO: CREATE HELPER FOR ACKS !!! 
# def calibrate():
    
#     fiducials_detected = 0

#     send_serial("MOVE_MOTOR_CONT:1,0")   # send up first 
#     wait_for_ack("LIMIT_SWITCH_TRIGGERED") #ack mssg that at limit switch
#     if received_message[0].split(":")[2] != 'UP':
#         raise ValueError("wrong direction!!!!!!! should be up")
#     data["vertical-motor"] = 0

#     send_serial(f"MOVE_MOTOR_STEPS:1,1,{2*boundary_offset}")
#     wait_for_ack("MOVE_MOTOR_STEPS")

#     # TODO: set state of z motor as 'up' -- store locally? 
#     send_serial("MOVE_MOTOR_CONT:0,1") # send to right  
#     wait_for_ack("LIMIT_SWITCH_TRIGGERED")
#     if received_message[0].split(":")[2] != 'RIGHT':
#         raise ValueError("wrong direction!!!!!!! should be right")

#     send_serial(f"MOVE_MOTOR_STEPS:0,0,{boundary_offset}")
#     wait_for_ack("MOVE_MOTOR_STEPS")

#     send_serial("SET_ZERO_POS:0" )
#     wait_for_ack("SET_ZERO_POS")
    
#     while (received_message[0].split(":")[1] != "LIMIT_SWITCH_TRIGGERED"): 
#         send_serial("MOVE_MOTOR_CONT:0,0")

#         fiducial_status = fiducial_detection()
#         if fiducial_status == 1:
#             break
        

#         send_serial("STOP_MOTOR:0")
#         wait_for_ack("STOP_MOTOR")  #ack mssg that it moved the stopped the motor
#         time.sleep(0.5)

#         send_serial("RETURN_POS:0")
#         wait_for_ack("RETURN_POS")

#         current_position = received_message[0].split(":")[2]
#         fiducials_detected += 1
#         data[f"{fiducials_detected}"] = current_position
#         time.sleep(1)

#     time.sleep(0.5)
#     send_serial(f"MOVE_MOTOR_STEPS:0,1,{boundary_offset}") # moving to right 
#     wait_for_ack("MOVE_MOTOR_STEPS")

#     #time.sleep(0.01)

#     # request current position and store that as outer boundary 
#     # TODO: current position helper
#     send_serial("RETURN_POS:0")
#     wait_for_ack("RETURN_POS")
#     current_position = received_message[0].split(":")[2]
#     data['horizontal-boundary'] = current_position
#     print(current_position)

#     return fiducials_detected

    
        
if __name__ == "__main__":
    print("CHECK: In the calibrate script")
    total_fiducials = sys.argv[1:]
    print("CHECK: Total fiducials: " + total_fiducials[0])
    # print("CHECK: Exiting the calibrate script")
    # fiducials_detected = calibrate() 
    # if fiducials_detected < total_fiducials:
    #     fiducials_detected = calibrate()

    # if fiducials_detected == total_fiducials:
    #     print(data)
    #     print("All fiducials found!")

    # else:
    #     raise ValueError("Failed to final all fiducials") 

    # # do a bit of cleanup
    # cv2.destroyAllWindows()
