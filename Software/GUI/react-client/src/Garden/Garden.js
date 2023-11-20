import React, { useState, useEffect } from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import "./Garden.css";
import axios from 'axios';
import PlotList from "./plot-list";
import AddPlots from "./AddPlots";

function Garden() {
  const [isAddPopupOpen, setIsAddPopupOpen] = useState();
  const [isCheckedAll, setIsCheckedAll] = useState(false);
  const [currentTime, setCurrentTime] = useState('No calibration yet');

  const handleAddButtonClick = () => {
    setIsAddPopupOpen(true);
  };

  const handleCalibrateButtonClick = async () => {
    try {
      await fetch("http://localhost:5000/api/calibrate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      fetchLastCalibrationTime();
    } catch (error) {
      console.error("Error calibrating:", error.message);
    }
  };

  const fetchLastCalibrationTime = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/get-last-calibration-time");
      const data = await response.json();

      // Parse the datetime string
      const dateTime = new Date(data.time);

      // Format the date
      const formattedDate = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        timeZoneName: 'short',
      }).format(dateTime);

      // Set the formatted date to state
      setCurrentTime(formattedDate);
    } catch (error) {
      console.error("Error fetching last calibration time:", error.message);
    }
  };


  const closeAddPopup = () => {
    setIsAddPopupOpen(false);
  };

  // useEffect(() => {
  //   console.log('Time of Calibration:', currentTime);
  // }, [currentTime]);

  // useEffect(() => {
  //   fetchLastCalibrationTime();
  // });

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
                <button className="m-2 btn button-primary-2 round-15 float-end">
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
              </div>
            </div>
          </div>
          <PlotList onCheckAll={setIsCheckedAll} isCheckedAll={isCheckedAll} />
        </div>
      </div>
    </div>
  );
}

export default Garden;
