# #!/usr/bin/python3
# # pi side 

# import cv2
# from picamera2 import Picamera2

# import time
# import serial
# import threading

# import sys

# steps_array = {}
# # horizontal_boundary = 0
# # vertical_status = 0
# # current_position = 0
# received_message = ["::"]
# vertical_steps = 159133 # TODO: find out correct one from HW
# # sensor_values = {
# #     'pH' : 0.0,
# #     'temperature' : 0.0,
# #     'ec' : 0.0
# # }

# # Grab images as numpy arrays and leave everything else to OpenCV.
# # face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
# cv2.startWindowThread()

# arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# arucoParams = cv2.aruco.DetectorParameters()
# arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# def receive_data(ser):
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline()
#             received_message[0] = line.decode('utf-8').rstrip()
#             print(received_message[0])

# # ser = serial.Serial('/dev/mydevice', 115200)
# ser = serial.Serial('/dev/ttyACM0', 115200)
# receive_thread = threading.Thread(target=receive_data, args=(ser,))
# receive_thread.daemon = True
# receive_thread.start()
  
    
# def get_current_position():
#     send_serial("RETURN_POS:0")
#     wait_for_ack("RETURN_POS")
#     current_position = int(received_message[0].split(":")[2])
#     return current_position

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

# # Grab images as numpy arrays and leave everything else to OpenCV.

# face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
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

# def check_fiducial():
#     im = picam2.capture_array()
#     #im = imutils.resize(im, width=1000)
#     im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
#     (corners, ids, rejected) = arucoDetector.detectMarkers(im)

#     if len(corners) > 0:
#         # flatten the ArUco IDs list
#         ids = ids.flatten()
#         # loop over the detected ArUCo corners
#         for (markerCorner, markerID) in zip(corners, ids):
#             # extract the marker corners (which are always returned
#             # in top-left, top-right, bottom-right, and bottom-left
#             # order)
#             corners = markerCorner.reshape((4, 2))
#             (topLeft, topRight, bottomRight, bottomLeft) = corners
#             # convert each of the (x, y)-coordinate pairs to integers
#             topRight = (int(topRight[0]), int(topRight[1]))
#             bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
#             bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
#             topLeft = (int(topLeft[0]), int(topLeft[1]))

#             # draw the bounding box of the ArUCo detection
#             cv2.line(im, topLeft, topRight, (0, 255, 0), 2)
#             cv2.line(im, topRight, bottomRight, (0, 255, 0), 2)
#             cv2.line(im, bottomRight, bottomLeft, (0, 255, 0), 2)
#             cv2.line(im, bottomLeft, topLeft, (0, 255, 0), 2)
#             # compute and draw the center (x, y)-coordinates of the
#             # ArUco marker
#             cX = int((topLeft[0] + bottomRight[0]) / 2.0)
#             cY = int((topLeft[1] + bottomRight[1]) / 2.0)
#             cv2.circle(im, (cX, cY), 4, (0, 0, 255), -1) 
#             current_offset = 160 - cX
#             if (current_offset > -3 or current_offset < 3):
#                 return -1, markerID # centered
#             elif (current_offset > 3):
#                 return 0, markerID # move to the left
#             else:
#                 return 1, markerID # move to the right 
            

# def run(vertical_status, steps_array):
#     # TODO check if steps array has all zeros
#     print("in run")
#     # send_serial("SET_ZERO_POS:0")
#     # time.sleep(0.5)
#     # print("after send ser")
#     # wait_for_ack("SET_ZERO_POS")
#     # send_serial(f"MOVE_MOTOR_STEPS:0,0,{boundary_offset}")

#     plot_readings= {key: {} for key in steps_array}
#     if vertical_status != 0 :
#         # send_serial("SET_ZERO_POS:1")
#         # wait_for_ack("SET_ZERO_POS")
#         send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}") 
#         wait_for_ack("MOVE_MOTOR_STEPS")

#     current_position = get_current_position()
#     send_serial(f"MOVE_MOTOR_STEPS:0,0,{current_position}")  
#     wait_for_ack("MOVE_MOTOR_STEPS")
#     print(steps_array)

#     sensor_values = {
#     'pH' : 0.0,
#     'temperature' : 0.0,
#     'ec' : 0.0,
#     'nutrients_pumped': False
#     }

#     for key in steps_array:
#     # for i, (key,step_value) in enumerate(steps_array):

#         current_position = get_current_position()
#         send_serial(f"MOVE_MOTOR_STEPS:0,1,{(steps_array[key] - current_position)}")
#         wait_for_ack("MOVE_MOTOR_STEPS")

#         # TODO: make optional
#         error_direction, fiducial_key = check_fiducial()
#         if (error_direction >= 0): 
#             # accounts for both directions since left is 0 and right is 1
#             send_serial(f"MOVE_MOTOR_CONT:0,{error_direction}")
#             fiducial_detection()
#         #     # NOTE: will fiducial have enough time to detect is again

#         send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
#         wait_for_ack("MOVE_MOTOR_STEPS") 
#         time.sleep(0.5)
#         # TODO: add delay for demo

#         # send_serial(f"LIGHT_ON:{i}")
#         # wait_for_ack("LIGHT_ON")

#         send_serial("READ_SENSOR:0")
#         wait_for_ack("READ_SENSOR")
#         sensor_values['pH'] = float(received_message[0].split(":")[2])

#         send_serial("READ_SENSOR:1" )
#         wait_for_ack("READ_SENSOR")
#         sensor_values['temperature'] = float(received_message[0].split(":")[2])

#         send_serial("ENABLE_EC_SENSOR")
#         wait_for_ack("ENABLE_EC_SENSOR")
#         time.sleep(2)

#         send_serial("READ_SENSOR:2")
#         wait_for_ack("READ_SENSOR")
#         sensor_values['ec'] = float(received_message[0].split(":")[2])

#         send_serial("DISABLE_EC_SENSOR")
#         wait_for_ack("DISABLE_EC_SENSOR")

#         # {'1': {
#         #     'steps' : 41981,
#         #     'pH': 6,
#         #     'ec' : 7
#         #  },
#         # }

#         # Compare values
#         # send_serial("PUMP_ON:[]")
#         # wait for ack
#         # time.sleep(5)
#         # send_serial("PUMP_OFF:[]")
#         # wait for ack
#         # Change 'nutrients pumped' to true

#         # EC is only done when its too low
#         for pump in range(3):
#             send_serial(f"PUMP_ON:{pump}")
#             wait_for_ack("PUMP_ON")

#         time.sleep(5)

#         for pump in range(3):
#             send_serial(f"PUMP_OFF:{pump}")
#             wait_for_ack("PUMP_OFF")

#         # TODO: If ph is too low or too high, pump nutrients and change sensor_values['nutrients_pumped'] to True
#         # TODO: If ec is too low or too high, pump nutrients and change sensor_values['nutrients_pumped'] to True

#         send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}")
#         wait_for_ack("MOVE_MOTOR_STEPS")

#         # send_serial(f"LIGHT_OFF:{i}")
#         # wait_for_ack("LIGHT_OFF")

#         plot_readings[key] = sensor_values

#     send_serial(f"MOVE_MOTOR_STEPS:0,0,{get_current_position()-9000}")
#     wait_for_ack("MOVE_MOTOR_STEPS")

#     # send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
#     # wait_for_ack("MOVE_MOTOR_STEPS")

#     # send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}")
#     # wait_for_ack("MOVE_MOTOR_STEPS")

#     send_serial(f"MOVE_MOTOR_STEPS:0,0,9000")
#     wait_for_ack("MOVE_MOTOR_STEPS")

#     return plot_readings 

# def endpoint_comm_run(vertical_status, steps_array):

#     # global picam2
#     # picam2 = Picamera2()
#     # picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}, controls={"FrameDurationLimits": (50000, 50000)}))
#     # picam2.start()

#     # global ser
#     # global receive_thread

#     # ser = serial.Serial('/dev/ttyACM1', 115200)
#     # receive_thread = threading.Thread(target=receive_data, args=(ser,))
#     # receive_thread.daemon = True
#     # receive_thread.start()

#     print("CHECK: in the run file")
#     data = run(vertical_status, steps_array)
#     sensor_values = {
#         'pH' : 5.0,
#         'temperature' : 6.0,
#         'ec' : 7.0
#     }

#     data = {key: {} for key in steps_array}
#     for key in steps_array:
#         data[key] = sensor_values

#     return data


# # do a bit of cleanup
# cv2.destroyAllWindows()