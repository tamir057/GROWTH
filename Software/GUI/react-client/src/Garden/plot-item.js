import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Garden-index.css";
import Select from './Select';

const PlotItem = ({ plot, isCheckedAll, onPlotCheckboxChange }) => {

  const [showAddPopup, setShowAddPopup] = useState(false);
  const [isChecked, setIsChecked] = useState(isCheckedAll);
  const [imagePath, setImagePath] = useState(`/images/${plot.plant}.jpg`);

  useEffect(() => {
    setIsChecked(isCheckedAll);
  }, [isCheckedAll]);

  const openAddPopup = () => {
    setShowAddPopup(true);
  };

  const closeAddPopup = () => {
    setShowAddPopup(false);
  };

  const handleImageError = () => {
    setImagePath(getImagePath(true));
  };

  function getImagePath(isError = false) {
    return "/images/Plant.jpg";
  }

  return (
    <li id="" className="list-group-item bg-secondary-green mt-2 mb-2">
      <div className="row">
        <div className="col-2">
          <input
            type="checkbox"
            id="checkbox"
            checked={isChecked}
            onChange={() => {
              setIsChecked(!isChecked);
              onPlotCheckboxChange(plot.plot_number);
            }}
          />
          <button
            className="m-2 col-3 button-square round-15"
            onClick={openAddPopup}
          >
            Plot {plot.plot_number} {plot.plant}
          </button>
          {showAddPopup && (
            <Select showModal={showAddPopup} handleClose={closeAddPopup} plotNumber={plot.plot_number} />
          )}
        </div>

        <div className="col-10 mt-2">
          <div>
            <img
              className="float-end"
              src={imagePath}
              alt="Plant"
              onError={handleImageError}
            />
          </div>
        </div>
      </div>
    </li>
  );
};

export default PlotItem;
