import cv2
from picamera2 import Picamera2

import time
import serial
import threading

import sys

received_message = ["::"]
vertical_steps = 155000
boundary_offset = 4000
current_position = 0
data = {
    'vertical-motor': 0, 
    'horizontal-boundary': 0,
    'steps_array': {}
}

# Grab images as numpy arrays and leave everything else to OpenCV.
# face_detector = cv2.CascadeClassifier("/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}, controls={"FrameDurationLimits": (50000, 50000)}))
picam2.start()

###########################################################################################################################
# Communication functions

def receive_data(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            received_message[0] = line.decode('utf-8').rstrip()
            print(f"Received message: {received_message[0]}")

try:
    ser = serial.Serial('/dev/ttyACM1', 115200)
except:
    ser = serial.Serial('/dev/ttyACM0', 115200)
receive_thread = threading.Thread(target=receive_data, args=(ser,))
receive_thread.daemon = True
receive_thread.start()


def get_current_position():
    send_serial("RETURN_POS:0")
    wait_for_ack("RETURN_POS")
    current_position = int(received_message[0].split(":")[2])
    return current_position

def wait_for_ack(message):
    
    parsed_message = "::"
    #TODO: what is this message
    print(received_message[0], " from beginning of wait")

    while (parsed_message != message):
        parsed_message = received_message[0].split(":")[1]
        pass
    print(f"ACK received: {parsed_message}") 

def send_serial(command):
    received_message[0] = "::"
    ser.write(command.encode('utf-8')+ b'\n')

###########################################################################################################################
# Fiducial functions

def fiducial_detection():
    while received_message[0].split(":")[1] != "LIMIT_SWITCH_TRIGGERED":
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
                    print("CHECK: Found a fiducial")
                    time.sleep(0.1)
                    return 0
                # draw the ArUco marker ID on the frame
            cv2.putText(im, str(markerID),(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
    return 1

def check_fiducial():
    im = picam2.capture_array()
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
            elif (current_offset > 3):
                return 0, markerID # move to the left
            else:
                return 1, markerID # move to the right 
            
###########################################################################################################################
# Run functions

def run(vertical_status, plots_data_dict):
    # NOTE: Form for plots_data_dict = {1: {'steps': 42043, 'min_pH': 6, 'max_pH': 6.8, 'min_ec': 1.2, 'max_ec': 2}}
    # TODO check if steps array has all zeros
    print("CHECK: beginning run")
    plot_readings= {key: {} for key in plots_data_dict}
    if vertical_status != 0 :
        send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}") 
        wait_for_ack("MOVE_MOTOR_STEPS")

    current_position = get_current_position()
    send_serial(f"MOVE_MOTOR_STEPS:0,0,{current_position}")  
    wait_for_ack("MOVE_MOTOR_STEPS")

    sensor_values = {
    'pH' : 0.0,
    'temperature' : 0.0,
    'ec' : 0.0,
    'nutrients_pumped': False
    }

    for key in plots_data_dict: 
        current_position = get_current_position()
        steps = plots_data_dict[key]["steps"]
        if steps == 0:
            continue
        send_serial(f"MOVE_MOTOR_STEPS:0,1,{(steps - current_position)}")
        wait_for_ack("MOVE_MOTOR_STEPS")

        send_serial(f"LIGHT_ON:{key - 1}")
        wait_for_ack("LIGHT_ON")

        # # TODO: make optional
        # error_direction, fiducial_key = check_fiducial()
        # if (error_direction >= 0): 
        #     # accounts for both directions since left is 0 and right is 1
        #     send_serial(f"MOVE_MOTOR_CONT:0,{error_direction}")
        #     fiducial_detection()
        #     # NOTE: will fiducial have enough time to detect is again

        send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
        wait_for_ack("MOVE_MOTOR_STEPS") 
        time.sleep(30)

        send_serial("READ_SENSOR:0")
        wait_for_ack("READ_SENSOR")
        sensor_values['temperature'] = float(received_message[0].split(":")[2])

        send_serial("READ_SENSOR:1" )
        wait_for_ack("READ_SENSOR")
        sensor_values['pH'] = float(received_message[0].split(":")[2])

        send_serial("ENABLE_EC_SENSOR")
        wait_for_ack("ENABLE_EC_SENSOR")

        time.sleep(30)

        send_serial("READ_SENSOR:2")
        wait_for_ack("READ_SENSOR")
        sensor_values['ec'] = float(received_message[0].split(":")[2])

        send_serial("DISABLE_EC_SENSOR")
        wait_for_ack("DISABLE_EC_SENSOR")

        current_pH = sensor_values['pH']
        current_ec = sensor_values['ec']
        ideal_min_pH = plots_data_dict[key]["min_pH"]
        ideal_max_pH = plots_data_dict[key]["max_pH"]
        ideal_min_ec = plots_data_dict[key]["min_ec"]
        pumps = []

        # Add pumps to pump based on conditions
        if current_pH < ideal_min_ec:
            pumps.append(0) 
        elif current_pH > ideal_max_pH:
            pumps.append(1) 

        if current_ec < ideal_min_ec:
            pumps.append(2) 
            pumps.append(3) 

        # Turn the pumps on
        for pump in pumps:
            send_serial(f"PUMP_ON:{pump}")
            wait_for_ack("PUMP_ON")
            sensor_values['nutrients_pumped'] = True

        # Wait for sufficient pumping
        time.sleep(5)

        # Turn off pumps
        for pump in pumps:
            send_serial(f"PUMP_OFF:{pump}")
            wait_for_ack("PUMP_OFF")

        send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}")
        wait_for_ack("MOVE_MOTOR_STEPS")

        send_serial(f"LIGHT_OFF:{key - 1}")
        wait_for_ack("LIGHT_OFF")

        plot_readings[key] = sensor_values

    send_serial(f"MOVE_MOTOR_STEPS:0,0,{get_current_position()-9000}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial(f"MOVE_MOTOR_STEPS:1,0,{vertical_steps}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial(f"MOVE_MOTOR_STEPS:0,0,9000")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    print("PLOT READINGS")
    print(plot_readings)

    return plot_readings 

def endpoint_comm_run(vertical_status, steps_array):
    data = run(vertical_status, steps_array)
    return data

###########################################################################################################################
# Calibrate functions

def calibrate():
    
    fiducials_detected = 0

    send_serial("MOVE_MOTOR_CONT:1,0")   # send up first 
    wait_for_ack("LIMIT_SWITCH_TRIGGERED") #ack mssg that at limit switch
    print("CHECK: Vertical motor is up")
    if received_message[0].split(":")[2] != 'UP':
        raise ValueError("ERROR: Vertical Motor is moving in wrong direction")
    data["vertical-motor"] = 0
    send_serial(f"MOVE_MOTOR_STEPS:1,1,{8000}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    time.sleep(0.5)

    send_serial("MOVE_MOTOR_CONT:0,0") # send to left  
    wait_for_ack("LIMIT_SWITCH_TRIGGERED")
    if received_message[0].split(":")[2] != 'LEFT':
        raise ValueError("wrong direction!!!!!!! should be left")

    send_serial(f"MOVE_MOTOR_STEPS:0,1,3000")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial("SET_ZERO_POS:0")
    wait_for_ack("SET_ZERO_POS")
    
    while (received_message[0].split(":")[1] != "LIMIT_SWITCH_TRIGGERED"): 
        
        send_serial("MOVE_MOTOR_CONT:0,1")

        fiducial_status = fiducial_detection()
        if fiducial_status == 1:
            break
        

        send_serial("STOP_MOTOR:0")
        wait_for_ack("STOP_MOTOR")  #ack mssg that it moved the stopped the motor
        time.sleep(0.5)

        send_serial("RETURN_POS:0")
        wait_for_ack("RETURN_POS")

        current_position = received_message[0].split(":")[2]
        fiducials_detected += 1
        # NOTE: Might throw an error rn
        data["steps_array"][f"{fiducials_detected}"] = current_position
        time.sleep(1)

    time.sleep(0.5)
    send_serial(f"MOVE_MOTOR_STEPS:0,0,{boundary_offset}") # moving to right 
    wait_for_ack("MOVE_MOTOR_STEPS")

    #time.sleep(0.01)

    send_serial("RETURN_POS:0")
    wait_for_ack("RETURN_POS")

    current_position = received_message[0].split(":")[2]
    data['horizontal-boundary'] = current_position
    print("CHECK: Horizontal boundary set")

    send_serial(f"MOVE_MOTOR_STEPS:0,0,{current_position}")
    wait_for_ack("MOVE_MOTOR_STEPS")

    send_serial(f"MOVE_MOTOR_STEPS:1,1,{vertical_steps}")
    wait_for_ack("MOVE_MOTOR_STEPS")
    data["vertical-motor"] = 1

    print("CHECK: Calibration completed")

    return fiducials_detected

def endpoint_comm_calibrate(fiducial_count):
    total_fiducials = fiducial_count
    fiducials_detected = calibrate() 

    if fiducials_detected < total_fiducials:
        print("CHECK: Missing fiducials. Recalibrating")
        fiducials_detected = calibrate()

    if fiducials_detected == fiducial_count:
        print(data)
        print("CHECK: All fiducials found!")
        return data
    else:
        raise ValueError("Failed to find all fiducials") 


cv2.destroyAllWindows()