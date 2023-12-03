import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ReactSpeedometer from 'react-d3-speedometer';
import './select_index.css';

const Select = ({ showModal, handleClose, plotNumber }) => {
  const [emptyPlot, setEmptyPlot] = useState(true);
  const [sensorReadings, setSensorReadings] = useState({
    pH: 0,
    temperature: 0,
    ec: 0,
  });

  const [selectedPlant, setSelectedPlant] = useState('');
  const [plantOptions, setPlantOptions] = useState([]);
  const [minMaxValues, setMinMaxValues] = useState({
    minPH: 0,
    maxPH: 14,
    minEC: 0,
    maxEC: 10,
  });

  useEffect(() => {
    const fetchPlot = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/plots/${plotNumber}`);
        const plot = response.data;

        const isEmptyPlot = plot.plant_id === '';
        setEmptyPlot(isEmptyPlot);

        if (!isEmptyPlot) {
          try {
            const sensorResponse = await axios.get(`http://localhost:5000/api/plants/last-sensor-readings/${plotNumber}`);
            setSensorReadings(sensorResponse.data);
          } catch (sensorError) {
            console.error('Error fetching sensor readings:', sensorError);
          }
        }
      } catch (error) {
        console.error('Error fetching plot:', error);
      }
    };


    const fetchMinMaxValues = async () => {
      console.log("plot number: " + plotNumber);
      try {
        const response = await axios.get(`http://localhost:5000/api/plants/min-max-values/${plotNumber}`);
        setMinMaxValues(response.data);
        console.log("min max: ", response.data);
      } catch (error) {
        console.error('Error fetching min-max values:', error);
      }
    };

    const fetchPlants = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/plants');
        setPlantOptions(response.data);
      } catch (error) {
        console.error('Error fetching plant options:', error);
      }
    };

    fetchPlot();
    fetchMinMaxValues();
    fetchPlants();
  }, [plotNumber, emptyPlot]);

  useEffect(() => {
    const fetchSensorReadings = async () => {
      try {
        if (!emptyPlot) {
          const sensorResponse = await axios.get(`http://localhost:5000/api/last-sensor-readings/${plotNumber}`);
          setSensorReadings(sensorResponse.data);
          console.log("sensor: " + sensorResponse.data);
        }
      } catch (error) {
        console.error('Error fetching sensor readings:', error);
      }
    };

    fetchSensorReadings();
  }, [plotNumber, emptyPlot]);

  const modalStyle = {
    position: 'fixed',
    right: 0,
    top: 0,
    bottom: 0,
    width: '400px',
    backgroundColor: '#F7FCFC',
    zIndex: 1050,
    display: showModal ? 'block' : 'none',
    paddingLeft: '20px',
  };
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPlant, setSelectedPlant] = useState('');
  const [plantOptions, setPlantOptions] = useState([]);

  useEffect(() => {
    // Fetch plant options from your endpoint
    const fetchPlants = async () => {
      try {
        const response = await axios.get('http://10.110.203.52:5000/api/plants'); // Replace with your actual endpoint
        setPlantOptions(response.data);
      } catch (error) {
        console.error('Error fetching plant options:', error);
      }
    };

    // Call the fetchPlants function
    fetchPlants();
  }, []);

  const handleSave = async () => {
    try {
      // Make a POST request to your backend endpoint with plot number and selected plant
      const response = await axios.post(`http://10.110.203.52:5000/api/assign-plant`, {
        plotNumber: plotNumber,
        selectedPlant: selectedPlant,
      });

      console.log('Plant assigned successfully:', response.data);
      handleClose();
      window.location.reload();
    } catch (error) {
      console.error('Error assigning plant to plot:', error);
    }
  };

  const contentStyle = {
    flex: 1,
    textAlign: 'center',
  };

  const footerStyle = {
    marginTop: 'auto',
  };

  return (
    <div>
      {emptyPlot &&
        <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <h5 className="subtitle3Container">Select Plant:</h5>
            <div className="modal-body" style={contentStyle}>
              <select
                value={selectedPlant}
                onChange={(e) => setSelectedPlant(e.target.value)}
                className="custom-dropdown"
              >
                {/* Map through the fetched plant options and create options dynamically */}
                {plantOptions.map((plant) => (

                  <option key={plant._id} value={plant.name}>
                    {plant.name}
                  </option>
                ))}
              </select>
            </div>
            <div className={"subtitle2Container"}>
              <Link to='/PlantProfile'> Create a New Plant Profile</Link>
            </div>
            <div className="modal-footer" style={footerStyle}>
              <div className={"saveButton"}>
                <input
                  className={"saveButton"}
                  type="button"
                  value={"Save"}
                  onClick={handleSave}
                />
              </div>
            </div>
          </div>
        </div>
      }
      {!emptyPlot && (
        <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body" style={contentStyle}>
              <h5 className="runTimeContainer">pH Level:</h5>
              <ReactSpeedometer
                value={sensorReadings.pH}
                minValue={Number(minMaxValues.minPH)}
                maxValue={Number(minMaxValues.maxPH)}
                startColor={sensorReadings.pH >= minMaxValues.minPH && sensorReadings.pH <= minMaxValues.maxPH ? '#00FF00' : '#FF0000'}
                endColor={sensorReadings.pH >= minMaxValues.minPH && sensorReadings.pH <= minMaxValues.maxPH ? '#00FF00' : '#FF0000'}
              />

              <p>Min: {minMaxValues.minPH}</p>
              <p>Max: {minMaxValues.maxPH}</p>

              <h5 className="runTimeContainer">EC Level:</h5>
              <ReactSpeedometer
                value={sensorReadings.ec}
                minValue={minMaxValues.minEC}
                maxValue={minMaxValues.maxEC}
                startColor={sensorReadings.ec >= minMaxValues.minEC && sensorReadings.ec <= minMaxValues.maxEC ? '#00FF00' : '#FF0000'}
                endColor={sensorReadings.ec >= minMaxValues.minEC && sensorReadings.ec <= minMaxValues.maxEC ? '#00FF00' : '#FF0000'}
              />
              <p>Min: {minMaxValues.minEC}</p>
              <p>Max: {minMaxValues.maxEC}</p>
            </div>
            <div className="modal-footer" style={footerStyle}>
              <div className="topPadding">
                <div className="saveButton">
                  <input
                    className="saveButton"
                    type="button"
                    value="Save"
                    onClick={handleSave}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Select;