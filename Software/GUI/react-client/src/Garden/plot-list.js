// import plotsArray from './plots.json';
import PlotItem from "./plot-item";
import React, { useState, useEffect } from 'react';


const PlotList = () => {
  const [plotsArray, setPlotsArray] = useState([]);

  useEffect(() => {
    // Fetch data from the Flask server when the component mounts
    fetch('/api/getPlots')
      .then(response => response.json())
      .then(data => setPlotsArray(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []); // The empty dependency array ensures the effect runs only once on mount

  return (
    <div className="w-100">
      <ul className="list-group">
        {plotsArray.map((plot) => (
          <PlotItem key={plot._id} plot={plot} />
        ))}
      </ul>
    </div>
  );
};
export default PlotList;
