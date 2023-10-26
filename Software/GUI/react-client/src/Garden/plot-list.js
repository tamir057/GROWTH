import React from "react";
import plotsArray from './plots.json';
import PlotItem from "./plot-item";

const PlotList = () => {
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
