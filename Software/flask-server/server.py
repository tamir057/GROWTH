from flask import Flask, jsonify, request, render_template, request, url_for, redirect
import os, json
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
import subprocess 
app = Flask(__name__)

CORS(app)

client = MongoClient('localhost', 27017, username='', password='')
db = client['Capstone']
plants = db.plants
plots = db.plots

@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

plots_file_path = os.path.join(os.path.dirname(__file__), 'motor-status.json')

@app.route('/update_steps', methods=['POST'])
def update_steps():
    try:
        data = request.get_json()

        # Ensure the received data is an array
        if not isinstance(data, list):
            return jsonify({'error': 'Invalid data format. Expected an array.'}), 400

        # Iterate through each plot in the array and update the steps
        for plot_data in data:
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
    
def save_status(vertical_motor, horizontal_boundary):
    try:
        # Read existing status from the file
        status_data = json.loads(read_status_from_file())

        # Update the specific fields
        status_data["vertical-motor"] = vertical_motor
        status_data["horizontal-boundary"] = horizontal_boundary

        # Convert the updated status back to JSON
        updated_status_json = json.dumps(status_data, indent=2)

        # Write the updated status back to the file
        write_status_to_file(updated_status_json)

        return status_data
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/api/addPlots', methods=['POST'])

# result = subprocess.check_output(['python', 'script2.py', arg1, arg2], text=True).strip()


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

#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'error': str(e)})
