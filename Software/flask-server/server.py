from flask import Flask, jsonify, request, render_template, request, url_for, redirect
import os, json
from pymongo import MongoClient

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

client = MongoClient('localhost', 27017, username='username', password='password')
db = client.flask_db
plants = db.plants
plots = db.plots


@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

plots_file_path = os.path.join(os.path.dirname(__file__), 'plots.json')

def read_plots_from_file():
    with open(plots_file_path, 'r') as file:
        data = file.read()
        return data
    
def write_plots_to_file(data):
    with open(plots_file_path, 'w') as file:
        file.write(data)

@app.route('/api/getPlots', methods=['GET'])
def get_data():
    try:
        # Read data from 'plots.json' file and parse it as JSON
        plot_array = json.loads(read_plots_from_file())
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