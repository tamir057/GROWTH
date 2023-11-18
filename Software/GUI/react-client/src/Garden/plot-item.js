import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Garden-index.css";
import Select from './Select'; // Import the AddPlotModal component


const PlotItem = ({ plot, isCheckedAll }) => {
  
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
    // Use the default image based on plot.plant and plot.plant_id
    setImagePath(getImagePath(true));
  };

  // Function to determine the image path based on plot.plant and whether it's an error case
  function getImagePath(isError = false) {
        return "/images/Plant.jpg";
  }
 return(
  <li id="" className="list-group-item bg-secondary-green mt-2 mb-2">
   <div className="row">
     <div className="col-2">
     <input
            type="checkbox"
            id="checkbox"
            checked={isChecked}
            onChange={() => setIsChecked(!isChecked)}
          />        <button class="m-2 col-3  button-square round-15" onClick={openAddPopup}>Plot {plot.plot_number} {plot.plant} </button>
        {showAddPopup && <Select/>}
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
     <Select showModal={showAddPopup} handleClose={closeAddPopup} plotNumber={plot.plot_number} />
   </div>
  </li>
 );
};
export default PlotItem;