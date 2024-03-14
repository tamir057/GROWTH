from flask import Flask, jsonify, request, render_template, request, url_for, redirect
import os, json
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime
import subprocess 
from bson import ObjectId
# import pytz
# from serial_cmd_scripts.scripts import endpoint_comm_calibrate
# from serial_cmd_scripts.scripts import endpoint_comm_run


app = Flask(__name__)

CORS(app)

connection_string = "mongodb+srv://capstone:capstone123@capstone.m5fs3fi.mongodb.net/?retryWrites=true&w=majority"
# Create a MongoClient instance
client = MongoClient(connection_string)
db = client['Capstone']
plants = db.plants
plots = db.plots
users = db.users
sensor_readings = db.sensor_readings

@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

plots_file_path = os.path.join(os.path.dirname(__file__), 'motor-status.json')
print("File Path:", plots_file_path)

def update_steps(steps_dict):
    try:
        # Ensure the received data is a dictionary
        if not isinstance(steps_dict, dict):
            print("ERROR: Steps dictionary is not a dictionary")
            return jsonify({'error': 'Invalid data format. Expected a dictionary.'}), 400

        # Iterate through each plot in the dictionary and update the steps
        for plot_number, steps in steps_dict.items():
            # Update steps for the specified plot_number
            result = plots.update_one({'plot_number': int(plot_number)}, {'$set': {'steps': int(steps)}})
            print("CHECK: Saved stes for plot")
            if result.modified_count == 0:
                return jsonify({'error': f'Plot with plot_number {plot_number} not found'}), 404

        return jsonify({'success': 'Steps updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/getPlots', methods=['GET'])
def get_data():
    try:
        # Read data from MongoDB 'plots' collection and convert it to a list of dictionaries
        plot_cursor = plots.find({}, {'_id': False})
        plot_array = list(plot_cursor)

        return jsonify(plot_array)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/addPlots', methods=['POST'])
def add_data():
    try:
        data = request.json
        plots_number = data.get('plots_number', 0)
        plot_array = list(plots.find())  # Assuming each document in the collection represents a plot

        new_data = []
        size = plots.count_documents({})  # Get the current number of documents in the collection

        for i in range(plots_number):
            new_data.append({
                "plot_number": i + 1 + size,
                "plant_id": "",
                "plant" : "Empty",
                "last_reading": {
                    "time": "",
                    "ph": 0,
                    "ec": 0
                },  
                "steps": 0              
            })

        # Insert the new data into the MongoDB collection
        plots.insert_many(new_data)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/save-plant-profile', methods=['POST'])
def save_plant_profile():
    try:
        data = request.json  # Assuming the request contains JSON data
        plant_name = data.get('name')

        # Check if the plant with the given name already exists
        existing_plant = plants.find_one({"name": plant_name})
        if existing_plant:
            return jsonify({'error': f'A plant with the name {plant_name} already exists'}), 400

        # Insert a new document into the plants collection
        result = plants.insert_one(data)

        if result.inserted_id:
            return jsonify({'success': True, 'message': 'Plant profile created successfully'})
        else:
            return jsonify({'error': 'Failed to create plant profile'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/plants', methods=['GET'])
def get_plants():
    try:

        # Fetch all plants from the collection
        plantsArray = list(plants.find({}, {'_id': 0}))  # Exclude _id field from the response

        # Send the plants as a JSON response
        return jsonify(plantsArray)
    except Exception as e:
        # Handle errors
        print('Error fetching plants:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/api/plots/<int:plot_number>', methods=['GET'])
def get_plot(plot_number):
    try:
        # Find the plot based on plot_number
        plot = plots.find_one({'plot_number': plot_number})
        
        # Check if the plot exists
        if plot:
            return jsonify(json.loads(dumps(plot)))
        else:
            return jsonify({'error': 'Plot not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/assign-plant', methods=['POST'])
def assign_plant():
    try:
        data = request.json  # Assuming the request contains JSON data
        plot_number = data.get('plotNumber')
        selected_plant = data.get('selectedPlant')
        print("Plant: "+ selected_plant)

        # Check if the plot exists
        plot = plots.find_one({"plot_number": plot_number})
        plant = plants.find_one({"name": selected_plant})

        if plant:
            plant_id = str(plant['_id'])  # Convert ObjectId to string
            plant_name = str(plant['name']) 
            # Rest of your code
        else:
            return jsonify({'error': 'Selected plant not found'})
        if plot:
            # Update the plant field of the specified plot
            plots.update_one({"plot_number": plot_number}, {"$set": {"plant_id": plant_id, "plant": plant_name}})

            print("Success")
            return jsonify({'success': True, 'message': 'Plant assigned successfully'})
        else:
            print("Error")
            return jsonify({'error': 'Plot not found'})

    except Exception as e:
        return jsonify({'error': str(e)})
    
def read_status_from_file():
    with open(plots_file_path, 'r') as file:
        data = file.read()
        return data
    
def write_status_to_file(data):
    with open(plots_file_path, 'w') as file:
        file.write(data)

def get_status():
    try:
        # Read data from 'plots.json' file and parse it as JSON
        status_data = json.loads(read_status_from_file())
        return status_data
    except Exception as e:
        return jsonify({'error': str(e)})
    
def save_status(vertical_motor, horizontal_boundary, current_time):
    try:
        # Read existing status from the file
        print("CHECK: in Save status")
        status_data = json.loads(read_status_from_file())
        print("Existing status:", status_data)  # Add this line for debugging

        # Update the specific fields
        status_data["vertical-motor"] = vertical_motor
        status_data["horizontal-boundary"] = horizontal_boundary
        status_data["last-calibration-time"] = current_time
        print("New status", status_data)
        # Convert the updated status back to JSON
        updated_status_json = json.dumps(status_data, indent=2)

        # Write the updated status back to the file
        write_status_to_file(updated_status_json)

        return status_data
    except Exception as e:
        print("Error in save_status:", str(e))  # Add this line for debugging
        return {'error': str(e)}

@app.route('/api/calibrate', methods=['POST'])
def calibrate_endpoint():
    print("CHECK: Hit calibrate endpoint")
    try:
        plot_count = plots.count_documents({})
        print(f"CHECK: this is the plot count: {plot_count}")
        print("CHECK: Before the calibrate script")
        # data = {'vertical-motor': 0, 'horizontal-boundary': '116403', 'steps_array': {'1': '41981', '2': '78288', '3': '113360'}}
        # NOTE: DO NOT uncomment unless robot is connected
        data = endpoint_comm_calibrate(3)
        print("CHECK: Exited the Calibrate file")
        update_steps(data['steps_array'])
        current_time = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
        save_status(data['vertical-motor'], data['horizontal-boundary'], current_time)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Subprocess error: {e}'})
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'})
    
@app.route('/api/get-last-calibration-time', methods=['GET'])
def get_last_calibration_time():
    try:
        calibration_complete = True
        if calibration_complete:
            # Fetch the updated calibration time
            response = get_status()
            time = response["last-calibration-time"]
            print(time)
            return jsonify({"time" : time})
        else:
            # Calibration process is not complete, send a response indicating that
            return jsonify({'message': 'Calibration in progress'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def endpoint_comm_run_mock(vertical_status, steps_array):
    print("CHECK: in the run file")

    ph = [5,6,7]
    ec = [1,2,3]
    temp = [20, 22, 24]
    data = {key: {} for key in steps_array}
    print(f"Before any assignment: {data}")
    for key in steps_array:
        sensor_values = {
        'pH' : 0.0,
        'temperature' : 0.0,
        'ec' : 0.0,
        'nutrients_pumped': False
        }
        print(f'CHECK: plot number {key}')
        sensor_values['temperature'] = temp[key - 1]
        sensor_values['pH'] = ph[key - 1]
        sensor_values['ec'] = ec[key -1]
        print (f'Key: {key} Values: {sensor_values}')
        data[key] = sensor_values
        print(f"CHECK: after assigning {data[key]}")
        print(" ")
    print("Complete Data")
    print(data)

    return data, 0

@app.route('/api/run', methods=['POST'])
def run():
    print("CHECK: Hit run endpoint")
    try:
        data = request.json
        print("CHECK: Data received")
        selected_plots = data.get('checkedPlots')  # Access the checkedPlots key
        print("CHECK: checked plots", selected_plots)
        # selected_plots = [1,2,3]
        print("CHECK: Going into get steps array")
        steps_array = get_steps_array(selected_plots)
        status = get_status()
        data = {}
        # NOTE: DO NOT uncomment unless robot is connected
        data, vertical_status = endpoint_comm_run(status['vertical-motor'], steps_array)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_status(vertical_motor=vertical_status, horizontal_boundary=status["horizontal-boundary"], current_time=status["last-calibration-time"])
        print("Time " + current_time )
        # appending the time
        modified_readings = {
            plot_number: {'time': current_time, **readings}
            for plot_number, readings in data.items()
        }       
        print("CHECK: Appended time")
        save_sensor_readings(modified_readings)
        print("CHECK: Reading saved to database")
        return jsonify({'success': True})
        # TODO: save status
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_steps_array(plot_numbers):
    print("CHECK: In Get steps array")
    try:
        steps_dict = {}
        for plot_number in plot_numbers:
            # Find the plot based on plot_number
            plot = plots.find_one({'plot_number': plot_number})
            # print("Plot found", plot)
            plant_id  = ObjectId(plot.get('plant_id', 0))

            # Check if the plot exists
            if plot:
                # print("CHECK: In If")
                # print("Plant id", plant_id)
                plant = plants.find_one({"_id": plant_id})
                plot_data = {}
                # print("CHECK: Plot's Plant identified", plant)
                plot_data["steps"] = plot.get('steps', 0)
                plot_data["min_pH"] = plant.get('min_pH', 0)
                plot_data["max_pH"] = plant.get('max_pH', 0)
                plot_data["min_ec"] = plant.get('min_ec', 0)
                plot_data["max_ec"] = plant.get('max_ec', 0)
                steps_dict[plot_number] = plot_data
                # print(steps_dict[plot_number])
            else:
                raise ValueError(f'Plot with plot_number {plot_number} not found')
            # print(steps_dict)
        return steps_dict
    except Exception as e:
        raise ValueError(str(e))

def save_sensor_readings(plot_readings):
    print("in save")
    new_data = []
    try:
        for plot_number, readings in plot_readings.items():
            # Find the plot based on plot_number
            plot = plots.find_one({'plot_number': int(plot_number)})
            plot_id = plot["_id"]
            # print(f"CHECK: Readings: {readings}")

            # Check if the plot exists  
            if plot:
                # # Update the "last_reading" field of the specified plot
                plots.update_one(
                    {'plot_number': int(plot_number)},
                    {'$set': {'last_reading': readings}}
                )
                new_data.append({
                    "plot_number": plot_number,
                    **readings          
                })
                print(new_data)
            else:
                print('Plot with plot_number {plot_number} not found')
        sensor_readings.insert_many(new_data)
        print('success')

    except Exception as e:
        print('Exception')

# min max values for gauge chart
@app.route('/api/plants/min-max-values/<int:plot_number>', methods=['GET'])
def get_min_max_values(plot_number):
    # Check if the plot exists
    plot = plots.find_one({"plot_number": plot_number})
    
    if plot:
        # Extract the plant_name from the plot
        plant_name = plot.get("plant")

        if plant_name is not None:
            # Query the plant collection based on the plant_name
            plant = plants.find_one({'name': plant_name})

            if plant:
                # Extract min-max values from the plant document
                min_max_values = {
                    "minPH": plant.get("min_pH", 0),
                    "maxPH": plant.get("max_pH", 14),
                    "minEC": plant.get("min_ec", 0),
                    "maxEC": plant.get("max_ec", 10),
                }
                return json.dumps(min_max_values)
            else:
                return jsonify({"error": "Plant not found"}), 404
        else:
            return jsonify({"error": "Plant name not found in the plot"}), 404
    else:
        return jsonify({"error": "Plot not found"}), 404

    
@app.route('/api/plants/last-sensor-readings/<int:plot_number>', methods=['GET'])
def get_last_sensor_reading(plot_number):
    print(f"Received request for plot number: {plot_number}")
    # Assuming you have a "plots" collection in your MongoDB
    # Query the database for the plot with the specified plot_number
    plot = plots.find_one({"plot_number": plot_number})

    if plot:
        # Extract the last_reading information
        last_reading = plot.get("last_reading", {})
        
        # Return the plot document with the last_reading information
        print(f"Returning sensor reading: {last_reading}")
        return jsonify(last_reading)
    else:
        # Return a 404 Not Found response if the plot is not found
        print("Plot not found")
        return jsonify({"error": "Plot not found"}), 404


    
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.json 
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
        print(data)
        email = data.get('email')
        password = data.get('password')
        firstName = data.get('firstName')
        lastName = data.get('lastName')

        # Check if the email already exists
        existing_user = users.find_one({"email": email})

        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        # Insert a new document into the users collection
        result = users.insert_one({
            "email": email,
            "password": password,
            "firstName": firstName,
            "lastName": lastName,
            "isActive": True  # You can set the initial value for isActive as needed
        })

        if result.inserted_id:
            return jsonify({'success': True, 'message': 'User registered successfully'})
        else:
            # print("lol")
            return jsonify({'error': 'Failed to register user'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json  # Assuming the request contains JSON data
        email = data.get('email')
        password = data.get('password')

        # Find the user based on the provided email and password
        user = users.find_one({"email": email, "password": password})

        if user:
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Implemented in PlantProfile
# @app.route('/api/generate-plant-info')
# def generate_plant_info():
#     try:
#         plantName = request.json
#         generatePlantInfo(plantName)
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'error': str(e)})
    
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    
