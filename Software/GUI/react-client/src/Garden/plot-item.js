import React, { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Garden-index.css";
import Select from './Select'; // Import the AddPlotModal component



const PlotItem = (
 {
   plot = {
     "plot_number": "1",
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
  <li className="list-group-item bg-secondary-green mt-2 mb-2">
   <div className="row">
     <div className="col-1">
     <input type="checkbox" id="checkbox"></input>
        <button class="m-2 col-3 btn button-square round-15" onClick={openAddPopup}>Plot {plot.plot_number} {plot.plant} </button>
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
     {(plot.plant !== "") && 
     <div>
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
}
{(plot.plant == "") && 
     <div>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={70} className="float-end" src="/images/empty2.jpeg"/>
    </div>
}


     </div>
     <Select showModal={showAddPopup} handleClose={closeAddPopup} />
   </div>
  </li>
 );
};
export default PlotItem;