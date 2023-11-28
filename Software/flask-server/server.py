from flask import Flask, jsonify, request, render_template, request, url_for, redirect
import os, json
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime
import subprocess 
from datetime import datetime
app = Flask(__name__)

CORS(app)

connection_string = "mongodb+srv://capstone:capstone123@capstone.m5fs3fi.mongodb.net/?retryWrites=true&w=majority"
# Create a MongoClient instance
client = MongoClient(connection_string)
# client = MongoClient('localhost', 27017, username='', password='')
db = client['Capstone']
plants = db.plants
plots = db.plots

@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

plots_file_path = os.path.join(os.path.dirname(__file__), 'motor-status.json')
print("File Path:", plots_file_path)

#@app.route('/update_steps', methods=['POST'])
def update_steps(steps_array):
    try:
        # data = request.get_json()

        # Ensure the received data is an array
        if not isinstance(steps_array, list):
            print("Steps array is not an array")
            # return jsonify({'error': 'Invalid data format. Expected an array.'}), 400

        # Iterate through each plot in the array and update the steps
        for plot_data in steps_array:
            # Ensure required fields are present in the plot_data
            if 'plot_number' not in plot_data or 'steps' not in plot_data:
                return jsonify({'error': 'Missing required fields in plot data'}), 400

            # Extract plot_number and steps from the plot_data
            plot_number = plot_data['plot_number']
            steps = plot_data['steps']

            # Update steps for the specified plot_number
            result = plots.update_one({'plot_number': plot_number}, {'$set': {'steps': steps}})

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
        # plot_array = json.loads(read_plots_from_file())
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
        status_data = json.loads(read_status_from_file())
        print("Existing status:", status_data)  # Add this line for debugging

        # Update the specific fields
        status_data["vertical-motor"] = vertical_motor
        status_data["horizontal-boundary"] = horizontal_boundary
        status_data["last-calibration-time"] = current_time

        # Convert the updated status back to JSON
        updated_status_json = json.dumps(status_data, indent=2)

        # Write the updated status back to the file
        write_status_to_file(updated_status_json)

        return status_data
    except Exception as e:
        print("Error in save_status:", str(e))  # Add this line for debugging
        return {'error': str(e)}


# @app.route('/api/calibrate', methods=['POST'])
# def calibrate():
#     print("hit calibrate endpoint")
#     try:
#         # TODO: get request number of plants in plot collection to pass in as arg for calibrate.py
#         data = subprocess.check_output(['python', './serial-cmd-scripts/calibrate.py'] + 3)
#         # data = subprocess.check_output(['python'])
#         update_steps(data['steps_array'])
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         save_status(data["vertical-motor"], data["horizontal-boundary"], current_time)
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'error': str(e)})

@app.route('/api/calibrate', methods=['POST'])
def calibrate():
    print("hit calibrate endpoint")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_status(0, 0, current_time)
    try:
        # TODO: get request number of plants in plot collection to pass in as arg for calibrate.py
        plot_count = plots.count_documents({})
        print(f"this is the plot count: {plot_count}")
        command = ["python", "./serial-cmd-scripts/calibrate.py", 3, "--flag"]
        process = subprocess.run(command, capture_output=True, text=True)
        print("Output:", process.stdout)
        print("Error:", process.stderr)
        print("Return code:", process.returncode)
        # subprocess.run(['python', './serial-cmd-scripts/calibrate.py'] + 3)
        # result = subprocess.run(['./serial-cmd-scripts/calibrate.py'], shell=True, capture_output=True, text=True)
        # print(result.stdout)
        # data = subprocess.check_output(['python', './serial-cmd-scripts/calibrate.py'] + 3)
        # update_steps(data['steps_array'])
        # save_status(vertical_motor=data["vertical-motor"],  horizontal_boundary=data["horizontal-boundary"])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})
    
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
    
@app.route('/api/run', methods=['POST'])
def run():
    print("hit run endpoint")
    try:
        data = request.json
        selected_plots = data.get('checkedPlots')  # Access the checkedPlots key
        # selected_plant = data.get('selectedPlant')
        print("Plots:", selected_plots)

        steps_array = get_steps_array(selected_plots)
        readings = subprocess.check_output(['python', './serial-cmd-scripts/run.py'] + steps_array, text=True)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # appending the time
        modified_readings = {
            plot_number: {'time': current_time, **readings}
            for plot_number, readings in readings.items()
        }       
        save_sensor_readings(modified_readings)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_steps_array(plot_numbers):
    try:
        steps_dict = {}

        # Iterate through each plot number and fetch the corresponding steps
        for plot_number in plot_numbers:
            # Find the plot based on plot_number
            plot = plots.find_one({'plot_number': plot_number})

            # Check if the plot exists
            if plot:
                steps_dict[plot_number] = plot.get('steps', 0)
            else:
                raise ValueError(f'Plot with plot_number {plot_number} not found')

        return steps_dict

    except Exception as e:
        raise ValueError(str(e))

def save_sensor_readings(plot_readings):
    try:
        for plot_number, readings in plot_readings.items():
            # Find the plot based on plot_number
            plot = plots.find_one({'plot_number': plot_number})
            print(plot_number)

            # Check if the plot exists
            if plot:
                # Update the "last_reading" field of the specified plot
                plots.update_one(
                    {'plot_number': plot_number},
                    {'$set': {'last_reading': readings}}
                )
            else:
                print('Plot with plot_number {plot_number} not found')

        print('success')

    except Exception as e:
        print('Exception')

# TODO: Update run endpoint to include 

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/api/addPlots', methods=['POST'])

# result = subprocess.check_output(['python', 'script2.py', arg1, arg2], text=True).strip()


    # print(plots.count_documents({}))
    # plot_reading = {
    #     1: {
    #         'time': '12:00',
    #         'pH': 6.5,
    #         'temperature': 25.0,
    #         'ec': 1.8
    #     },
    #     2: {
    #         'time': '12:00',
    #         'pH': 7.2,
    #         'temperature': 24.5,
    #         'ec': 2.0
    #     },
    #     3: {
    #         'time': '12:00',
    #         'pH': 6.8,
    #         'temperature': 26.0,
    #         'ec': 1.5
    #     }
    # }
    # save_sensor_readings(plot_reading)
    # print(get_steps_array([1,2,3,4]))

# try:
#     # Attempt to create a MongoDB client instance
#     client = MongoClient('localhost', 27017, username='', password='')
#     db = client['Capstone']
#     plants = db.plants 
#     plots = db.plots

#     # Check the connection by accessing a database
#     client.admin.command('ismaster')
#     print(f'MongoDB connection all set')
#     print(list(plots.find({}, {})))

# except Exception as e:
#     # Log or handle the connection error
#     print(f'MongoDB connection error: {str(e)}')
#     # You may want to exit the application or take other appropriate action here




# # TODO: replace with mongo connection
# @app.route('/api/getPlots', methods=['GET'])
# def get_data():
#     try:
#         # Read data from 'plots.json' file and parse it as JSON
#         plot_array = json.loads(read_plots_from_file())
#         return jsonify(plot_array)
#     except Exception as e:
#         return jsonify({'error': str(e)})

# TODO: Redo with Mongo
# @app.route('/api/addPlots', methods=['POST'])
# def add_data():
#     try:
#         data = request.json  # Assuming the request contains JSON data
#         plots_number = data.get('plots_number', 0)  # Extract the number of plots from the JSON data
#         plot_array = json.loads(read_plots_from_file())
#         size = len(plot_array)
#         # plots_number = 5
#         # TODO: get the number of plots 
#         new_data = []
#         for i in range(plots_number):
#             # You can add any value or object to the list here
#             new_data.append({
#                 "_id": f"{i + 1 + size}",
#                 "plot_number": f"{i + 1 + size}",  # Adjust the plot_number as needed
#                 "plant": ""
#             })

#         # Extend the existing array with the new data
#         plot_array.extend(new_data)
 
#         # Write the updated array back to the file
#         write_plots_to_file(json.dumps(plot_array)) 

