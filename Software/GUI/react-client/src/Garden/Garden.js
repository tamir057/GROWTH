import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Garden.css";
import PlotList from "./plot-list";
import AddPlots from "./AddPlots";

function Garden() {
  const [isAddPopupOpen, setIsAddPopupOpen] = useState();
  const [isCheckedAll, setIsCheckedAll] = useState(false);

  const handleAddButtonClick = () => {
    setIsAddPopupOpen(true);
  };

  const handleCalibrateButtonClick = () => {
    fetch("http://localhost:5000/api/calibrate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  };

  const closeAddPopup = () => {
    setIsAddPopupOpen(false);
  };

  return (
    <div>
      <div className="nav-padding bg-grey-c wide row fullHeightDiv">
        <div className="col-11 bg-secondary-green container mt-4 wide round-10">
          <div className="row">
            <div className="col-6">
              <h3 className="p-2">Farm Layout</h3>
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
