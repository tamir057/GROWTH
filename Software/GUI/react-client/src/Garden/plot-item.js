import React, { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./garden_index.css";
import PlotList from "./plot-list";
import Select from './Select'; // Import the AddPlotModal component



const PlotItem = (
 {
   plot = {
     "plotNumber": "1",
     "plant": "Spinach"
   }
 }

) => {
  
  const [showAddPopup, setShowAddPopup] = useState(false);
  const openAddPopup = () => {
    setShowAddPopup(true);
  };
  
  const closeAddPopup = () => {
    setShowAddPopup(false);
  };
  
 return(
  <li className="list-group-item bg-secondary-green">
   <div className="row">
     <div className="col-1">
     <input type="checkbox" id="checkbox"></input>
        <button class="m-2 col-3 btn button-square round-15" onClick={openAddPopup}>Plot {plot.plotNumber} {plot.plant} </button>
        {showAddPopup && <Select/>}
     </div>
     <div className="col-10 mt-2 ml-0 pl-0">
     {/* <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/> */}


     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>

     </div>
     <Select showModal={showAddPopup} handleClose={closeAddPopup} />
   </div>
  </li>
 );
};
export default PlotItem;