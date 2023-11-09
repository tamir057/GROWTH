import React, { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./garden_index.css";
import PlotList from "./plot-list";
import Select from './Select'; // Import the AddPlotModal component


function Garden() {
  const [showAddPopup, setShowAddPopup] = useState(false);

  const openAddPopup = () => {
    setShowAddPopup(true);
  };

  const closeAddPopup = () => {
    setShowAddPopup(false);
  };

  console.log("test: " + showAddPopup); 

  return (
    <div>
      <div className="nav-padding bg-grey-c wide row">
        <div className="col-11 bg-secondary-green container mt-4 wide round-10">
          <div className="row">
            <div className="col-6">
              <h3 className="p-2">Farm Layout</h3>
            </div>
            <div className="col-6 float-end">
              <div className="row">
                <div className="col-2"></div>
                <button className="m-2 col-3 btn button-primary round-15">Calibrate</button>
                <button className="m-2 col-3 btn button-primary round-15">Run</button>
                <button className="m-2 col-3 btn button-primary round-15" onClick={openAddPopup}>Add</button>
                {showAddPopup && <Select/>}
              </div>
            </div>
          </div>
          <PlotList />
        </div>
      </div>
      <Select showModal={showAddPopup} handleClose={closeAddPopup} />
    </div>
  );
}

export default Garden;
