import React, { useState, useEffect } from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import "./Garden.css";
import axios from 'axios';
import PlotList from "./plot-list";
import AddPlots from "./AddPlots";
import WarningPopUp from "./WarningPopUp";
import LoadingPopup from './Loading';

function Garden() {
  const [isAddPopupOpen, setIsAddPopupOpen] = useState();
  const [isWarningPopupOpen, setIsWarningPopupOpen] = useState();
  const [isCheckedAll, setIsCheckedAll] = useState(false);
  const [checkedPlots, setCheckedPlots] = useState([]);
  const [currentTime, setCurrentTime] = useState('No calibration yet');
  const [isLoading, setIsLoading] = useState(false);
  const [runType, setRunType] = useState("");


  const handleAddButtonClick = () => {
    setIsAddPopupOpen(true);
  };

  const handleCalibrateButtonClick = async () => {
    try {
      setRunType("Calibrating...")
      setIsLoading(true);
      await fetch("http://129.10.158.17:5000/api/calibrate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      setIsLoading(false);
      // Wait for the calibration to finish before fetching the updated time
      fetchLastCalibrationTime();
    } catch (error) {
      console.error("Error calibrating:", error.message);
    }
  };


  const fetchLastCalibrationTime = async () => {
    try {
      console.log("im in here")
      const response = await fetch("http://129.10.158.17:5000/api/get-last-calibration-time");
      const data = await response.json();
      const lastCalibrationTime = new Date(data.time);
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        // second: 'numeric',
        timeZoneName: 'short',
      };

      // Format the date using the specified options
      const formattedTime = lastCalibrationTime.toLocaleString('en-US', options);
      setCurrentTime(formattedTime);
    } catch (error) {
      console.error("Error fetching last calibration time:", error.message);
    }
  };


  const handleRunButtonClick = () => {
    // Check if checkedPlots is an empty array
    if (checkedPlots.length === 0) {
      // Call the WarningPopUp or handle the empty case as needed
      setIsWarningPopupOpen(true); // You need to implement showWarningPopUp function
      return; // Return early if the array is empty
    }
    setRunType("Reading Sensor Data...")
    setIsLoading(true);
    fetch("http://129.10.158.17:5000/api/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ checkedPlots }), // Pass checked plots to the server
    });
    setIsLoading(false);
  };


  const closeAddPopup = () => {
    setIsAddPopupOpen(false);
  };

  const closeWarningPopup = () => {
    setIsWarningPopupOpen(false);
  };

  const handlePlotCheckboxChange = (plotNumber) => {
    if (checkedPlots.includes(plotNumber)) {
      setCheckedPlots(checkedPlots.filter((plot) => plot !== plotNumber));
    } else {
      setCheckedPlots([...checkedPlots, plotNumber]);
    }
  };

  useEffect(() => {
    fetchLastCalibrationTime();
  });
  
  return (
    <div>
      <div className="nav-padding bg-grey-c wide row fullHeightDiv">
        <div className="col-11 bg-secondary-green container mt-4 wide round-10">
          <div className="row">
            <div className="col-6">
              <h3 className="p-2">Farm Layout</h3>
              <div className="italic-time">Last Calibration Time: {currentTime}</div>
            </div>
            <div className="col-6 float-end">
              <div className="float-end">
                <button 
                className="m-2 btn button-primary-2 round-15 float-end"
                onClick={handleRunButtonClick}
                >
                  Run
                </button>
                <button
                  className="m-2 btn button-primary-2 round-15 float-end"
                  onClick={handleCalibrateButtonClick}
                >
                  Calibrate
                </button>
                <button
                  className="m-2 btn button-primary-2 round-15 float-end"
                  onClick={handleAddButtonClick}
                >
                  Add
                </button>
                {isAddPopupOpen && <AddPlots onClose={closeAddPopup} />}
                {isWarningPopupOpen && <WarningPopUp onClose={closeWarningPopup} />}
                {isLoading && <LoadingPopup runType={runType}/>}
              </div>
            </div>  
          </div>
          <PlotList onCheckAll={setIsCheckedAll} isCheckedAll={isCheckedAll} onPlotCheckboxChange={handlePlotCheckboxChange}
      />        </div>
      </div>
    </div>
  );
}

export default Garden;
