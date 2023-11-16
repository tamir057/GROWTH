from flask import Flask, jsonify, request, render_template, request, url_for, redirect
import os, json
from pymongo import MongoClient

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

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

client = MongoClient('localhost', 27017, username='', password='')
db = client['Capstone']
plants = db.plants
plots = db.plots


@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

plots_file_path = os.path.join(os.path.dirname(__file__), 'plots.json')

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

# TODO: No need for this after redone
def read_plots_from_file():
    with open(plots_file_path, 'r') as file:
        data = file.read()
        return data
    
# TODO: No need for this after redone
def write_plots_to_file(data):
    with open(plots_file_path, 'w') as file:
        file.write(data)

# # TODO: replace with mongo connection
# @app.route('/api/getPlots', methods=['GET'])
# def get_data():
#     try:
#         # Read data from 'plots.json' file and parse it as JSON
#         plot_array = json.loads(read_plots_from_file())
#         return jsonify(plot_array)
#     except Exception as e:
#         return jsonify({'error': str(e)})

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
        data = request.json  # Assuming the request contains JSON data
        plots_number = data.get('plots_number', 0)  # Extract the number of plots from the JSON data
        plot_array = json.loads(read_plots_from_file())
        size = len(plot_array)
        # plots_number = 5
        # TODO: get the number of plots 
        new_data = []
        for i in range(plots_number):
            # You can add any value or object to the list here
            new_data.append({
                "_id": f"{i + 1 + size}",
                "plot_number": f"{i + 1 + size}",  # Adjust the plot_number as needed
                "plant": ""
            })

        # Extend the existing array with the new data
        plot_array.extend(new_data)

        # Write the updated array back to the file
        write_plots_to_file(json.dumps(plot_array))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
    
# 169.254.59.97s (Raspberry Pi IP)