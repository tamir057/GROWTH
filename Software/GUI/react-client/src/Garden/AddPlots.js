import React, { useState, useEffect } from "react";
import "./AddPlots.css";

const AddPlots = ({ onClose }) => {
  const [plotNumber, setPlotNumber] = useState(0);

  const decreasePlotNumber = () => {
    if (plotNumber > 0) {
      setPlotNumber(plotNumber - 1);
    }
  };

  const increasePlotNumber = () => {
    setPlotNumber(plotNumber + 1);
  };

  // const handleAddClick = () => {
  //     // Handle adding plots here
  //     console.log(`Adding ${plotNumber} plots.`);
  //     // You can perform your logic here for adding plots
  //     // For example, send an API request to add plots to the database
  //     onClose(); // Close the popup after adding plots
  // };

  const [plotArray, setPlotArray] = useState([]);
  const [newData, setNewData] = useState({ x: 0, y: 0 }); // Change the initial values as needed

  useEffect(() => {
    // Fetch initial data when the component mounts
    fetch("http://localhost:5000/api/getPlots")
      .then((response) => response.json())
      .then((data) => setPlotArray(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleAddClick = () => {
    // Make a POST request to add the number of plots
    fetch("http://localhost:5000/api/addPlots", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ plots_number: plotNumber }),
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.success) {
          // If the addition was successful, fetch updated data
          fetch("http://10.110.203.52:5000/api/getPlots")
            .then((response) => response.json())
            .then((data) => setPlotArray(data))
            .catch((error) =>
              console.error("Error fetching updated data:", error)
            );
          window.location.reload();
        } else {
          console.error("Error adding data:", result.error);
        }
      })
      .catch((error) => console.error("Error adding data:", error));
    onClose(); // Close the popup after adding plots
  };

  return (
    <div className="popup-container">
      <div className="popup">
        <div className="message">How many plots do you want to add?</div>
        <div className="number-container">
          <button className="button_num" onClick={decreasePlotNumber}>
            -
          </button>
          <div className="number">{plotNumber}</div>
          <button className="button_num" onClick={increasePlotNumber}>
            +
          </button>
        </div>
        <div className="button-container">
          <button className="button" onClick={handleAddClick}>
            Add
          </button>
          <button className="button cancel-button" onClick={onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddPlots;
