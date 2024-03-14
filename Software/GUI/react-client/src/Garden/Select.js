import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import ReactSpeedometer from "react-d3-speedometer";
import "./select_index.css";

const Select = ({ showModal, handleClose, plotNumber }) => {
  const [emptyPlot, setEmptyPlot] = useState(true);
  const [nullSensorReadings, setNullSensorReadings] = useState(true);
  const [sensorReadings, setSensorReadings] = useState({
    pH: 0,
    temperature: 0,
    ec: 0,
    time: "",
    nutrients_pumped: false,
  });

  const [selectedPlant, setSelectedPlant] = useState("");
  const [plantOptions, setPlantOptions] = useState([]);
  const [idealMinPH, setIdealMinPH] = useState(0);
  const [idealMaxPH, setIdealMaxPH] = useState(14);
  const [idealMinEC, setIdealMinEC] = useState(0);
  const [idealMaxEC, setIdealMaxEC] = useState(3);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch plot data
        const plotResponse = await axios.get(
          `http://localhost:5000/api/plots/${plotNumber}`
        );
        const plot = plotResponse.data;
        const isEmptyPlot = plot.plant_id === "";
        setEmptyPlot(isEmptyPlot);

        if (!emptyPlot) {
          // Fetch sensor readings
          const sensorResponse = await axios.get(
            `http://localhost:5000/api/plants/last-sensor-readings/${plotNumber}`
          );
          setSensorReadings(sensorResponse.data);
          const isNullSensorReadings = sensorReadings.time === "";
          setNullSensorReadings(isNullSensorReadings);
          console.log(sensorReadings);
        }

        // Fetch min-max values
        if (!emptyPlot) {
          const minMaxResponse = await axios.get(
            `http://localhost:5000/api/plants/min-max-values/${plotNumber}`
          );
          const minMaxValues = minMaxResponse.data;
          setIdealMinPH(minMaxValues["minPH"]);
          setIdealMaxPH(minMaxValues["maxPH"]);
          setIdealMinEC(minMaxValues["minEC"]);
          setIdealMaxEC(minMaxValues["maxEC"]);
        }
        // Fetch plant options
        const plantsResponse = await axios.get(
          "http://localhost:5000/api/plants"
        );
        setPlantOptions(plantsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // Call the combined fetch function
    fetchData();

    // Log min-max values
    console.log("Min PH: ", idealMinPH);
    console.log("Max PH: ", idealMaxPH);
    console.log("Min EC: ", idealMinEC);
    console.log("Max EC: ", idealMaxEC);
  }, [plotNumber, emptyPlot, idealMinPH, idealMaxPH, idealMinEC, idealMaxEC]);

  const modalStyle = {
    position: "fixed",
    right: 0,
    top: 0,
    bottom: 0,
    width: "400px",
    backgroundColor: "#F7FCFC",
    zIndex: 1050,
    display: showModal ? "block" : "none",
    paddingLeft: "20px",
  };

  const handleSave = async () => {
    try {
      // Make a POST request to your backend endpoint with plot number and selected plant
      const response = await axios.post(
        `http://localhost:5000/api/assign-plant`,
        {
          plotNumber: plotNumber,
          selectedPlant: selectedPlant,
        }
      );

      console.log("Plant assigned successfully:", response.data);
      handleClose();
      window.location.reload();
    } catch (error) {
      console.error("Error assigning plant to plot:", error);
    }
  };

  const contentStyle = {
    flex: 1,
    textAlign: "center",
  };

  const footerStyle = {
    marginTop: "auto",
  };

  return (
    <div>
      {emptyPlot && (
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
                {plantOptions.map((plant) => (
                  <option key={plant._id} value={plant.name}>
                    {plant.name}
                  </option>
                ))}
              </select>
            </div>
            <div className={"subtitle2Container"}>
              <Link to="/PlantProfile"> Create a New Plant Profile</Link>
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
      )}
      {!emptyPlot && !nullSensorReadings && (
        <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body" style={contentStyle}>
              <h5 className="runTimeContainer">pH Level:</h5>
              <div className="m-0 p-0 no-margin">
                {idealMinPH !== 0 &&
                  idealMaxPH !== 14 &&
                  sensorReadings.pH !== undefined && (
                    <ReactSpeedometer
                      style={{
                        marginBottom: "0px",
                        width: "150px",
                        height: "50px",
                      }}
                      value={sensorReadings.pH}
                      minValue={3}
                      maxValue={10}
                      customSegmentStops={[3, idealMinPH, idealMaxPH, 10]}
                      segmentColors={["#FF6961", "#B4D3B2", "#FF6961"]}
                      currentValueText={`pH: ${sensorReadings.pH.toFixed(3)}`}
                    />
                  )}
              </div>
              <div style={{ marginBottom: "10px" }}>
                <p>
                  Ideal Min: {idealMinPH} — Ideal Max: {idealMaxPH}
                </p>
              </div>

              <h5 className="runTimeContainer">Conductivity Level:</h5>
              <div className="m-0 p-0 no-margin">
                {idealMinEC !== 0 &&
                  idealMaxEC !== 3 &&
                  sensorReadings.pH !== undefined && (
                    <ReactSpeedometer
                      style={{
                        marginBottom: "0px",
                        width: "150px",
                        height: "50px",
                      }}
                      value={sensorReadings.ec}
                      minValue={0}
                      maxValue={3}
                      customSegmentStops={[0, idealMinEC, idealMaxEC, 3]}
                      // minMaxValues.minEC
                      segmentColors={["#FF6961", "#B4D3B2", "#FF6961"]}
                      currentValueText={`EC: ${sensorReadings.ec.toFixed(
                        3
                      )} mS/cm`}
                    />
                  )}
              </div>
              <div style={{ marginBottom: "10px" }}>
                <p>
                  Ideal Min: {idealMinEC} mS/cm — Ideal Max: {idealMaxEC} mS/cm
                </p>
              </div>

              {/* Display temperature */}
              <div>
                <p>Temperature: {sensorReadings.temperature.toFixed(3)} °C</p>
              </div>
              <div>
                {sensorReadings.nutrients_pumped && (
                  <p>
                    <strong>Nutrients pumped.</strong>
                  </p>
                )}
                {!sensorReadings.nutrients_pumped && (
                  <p>
                    <strong>Ideal ranges met. No nutrients necessary.</strong>
                  </p>
                )}
              </div>
            </div>
            <div className="modal-footer" style={footerStyle}>
              <div className="topPadding"></div>
            </div>
          </div>
        </div>
      )}
      {!emptyPlot && nullSensorReadings && (
        <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <p>
              <strong>No sensor readings recorded yet.</strong>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Select;
