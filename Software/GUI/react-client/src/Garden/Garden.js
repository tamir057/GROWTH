import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./index.css"
import PlotList from "./plot-list";

function Garden() {
  return (
    <div className="nav-padding bg-grey-c wide row">
      <div class="col-11 bg-secondary-green container mt-4 wide round-10">
        <div class="row">
        <div class="col-6">
            <h3 className="p-2">
                Farm Layout
            </h3>
            </div>
          <div class="col-6 float-end">
            <div className="row">
            <div className="col-2"></div>
            <button class="m-2 col-3 btn button-primary round-15">Calibrate</button>
            <button class="m-2 col-3 btn button-primary round-15">Run</button>
            <button class="m-2 col-3 btn button-primary round-15">Add</button>
            </div>
          </div>
        </div>
        <PlotList/>
      </div>
    </div>
  );
}
export default Garden;
