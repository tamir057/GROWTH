import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Garden-index.css";
import Select from './Select'; // Import the AddPlotModal component



const PlotItem = ({ plot, isCheckedAll }) => {
//  ({
//    plot = {
//     "_id": "654bd730d81fd3dadf6f304c",
//      "plot_number": "1",
//      "plant_id": "2345nhb65432vgf45"
//    }
//  }

// ) => {
  
  const [showAddPopup, setShowAddPopup] = useState(false);
  const [isChecked, setIsChecked] = useState(isCheckedAll);

  useEffect(() => {
    setIsChecked(isCheckedAll);
  }, [isCheckedAll]);
  const openAddPopup = () => {
    setShowAddPopup(true);
  };
  
  const closeAddPopup = () => {
    setShowAddPopup(false);
  };
  

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
     {(plot.plant_id !== "") && 
     <div>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={148} height={80} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={71} height={80} className="float-end" src="/images/garden-plant.jpg"/>

      {/*1255 pixels*/}
      {/* <img width={140} height={80} className="float-end" src="/images/garden-plant.jpg"/> */}
      {/* <img width={140} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={140} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={140} height={70} className="float-end" src="/images/garden-plant.jpg"/> */}
      {/* <img width={70} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={70} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={70} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={70} height={70} className="float-end" src="/images/garden-plant.jpg"/>
      <img width={70} height={70} className="float-end" src="/images/garden-plant.jpg"/> */}
     </div>
}
{(plot.plant_id == "") && 
     <div>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={70} height={80} className="float-end" src="/images/empty2.jpeg"/>
     <img width={65} height={80} className="float-end" src="/images/empty2.jpeg"/>

    </div>
}


     </div>
     <Select showModal={showAddPopup} handleClose={closeAddPopup} plotNumber={plot.plot_number} />
   </div>
  </li>
 );
};
export default PlotItem;