// import plotsArray from './plots.json';
import PlotItem from "./plot-item";
import React, { useState, useEffect } from "react";

const PlotList = ({ onCheckAll, isCheckedAll, onPlotCheckboxChange }) => {
  const [plotsArray, setPlotsArray] = useState([]);

  useEffect(() => {
    // Fetch data from the Flask server when the component mounts
    fetch("http://localhost:5000/api/getPlots")
      .then((response) => response.json())
      .then((data) => {
        console.log("Received Data:", data);
        setPlotsArray(data);
        console.log(data);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []); // The empty dependency array ensures the effect runs only once on mount

  const handleSelectAllButtonClick = () => {
    onCheckAll(!isCheckedAll);
    for (let plot of plotsArray) {
      onPlotCheckboxChange(plot.plot_number);
    }
  };

  return (
    <div className="w-100">
      <div>
        <button
          className="m-2 col-3 btn button-primary-2 round-15"
          onClick={handleSelectAllButtonClick}
        >
          Select All
        </button>
      </div>
      <ul className="list-group">
        {plotsArray.map((plot) => (
          <PlotItem
            key={plot._id}
            plot={plot}
            isCheckedAll={isCheckedAll}
            onPlotCheckboxChange={onPlotCheckboxChange}
          />
        ))}
      </ul>
    </div>
  );
};
export default PlotList;
